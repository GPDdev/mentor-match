#!/usr/bin/env python3
"""Portable local storage helper for Mentor Match. Uses only the Python standard library."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONSENT_VERSION = 1
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
STATUSES = {
    "open-confirmed",
    "open-continuous",
    "program-route",
    "unknown",
    "closed",
    "stale-or-conflicting",
}
CONFIDENCE = {"high", "medium", "low"}
MODES = {"quick", "standard", "deep", "refresh"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def data_root(raw: str | None) -> Path:
    configured = raw or os.environ.get("MENTOR_MATCH_HOME")
    return Path(configured).expanduser().resolve() if configured else (Path.home() / ".mentor-match").resolve()


def validate_id(value: str, label: str) -> str:
    if not ID_PATTERN.fullmatch(value):
        raise ValueError(f"{label} must match {ID_PATTERN.pattern}: {value!r}")
    return value


def ensure_within(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    if os.path.commonpath([str(resolved), str(root)]) != str(root):
        raise ValueError(f"Refusing path outside data root: {resolved}")
    if resolved == root:
        raise ValueError("Refusing operation on the data root itself")
    return resolved


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def require_consent(root: Path) -> dict[str, Any]:
    config_path = root / "config.json"
    if not config_path.exists():
        raise PermissionError(
            f"Storage consent is not recorded. Run: mentor_match.py --root {root} init --accept-storage"
        )
    config = read_json(config_path)
    consent = config.get("storage_consent", {})
    if consent.get("version") != CONSENT_VERSION or not consent.get("accepted_at"):
        raise PermissionError("Stored consent is missing or uses an unsupported version")
    return config


def profile_path(root: Path, profile_id: str) -> Path:
    return root / "profiles" / validate_id(profile_id, "profile ID")


def case_path(root: Path, profile_id: str, case_id: str) -> Path:
    return profile_path(root, profile_id) / "cases" / validate_id(case_id, "case ID")


def load_optional_object(path_value: str | None, label: str) -> dict[str, Any]:
    if not path_value:
        return {}
    path = Path(path_value).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"{label} JSON not found: {path}")
    return read_json(path)


def validate_candidates(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top = {"schema_version", "generated_at", "profile_id", "case_id", "mode", "weights", "candidates"}
    missing_top = sorted(required_top - data.keys())
    if missing_top:
        errors.append(f"missing top-level fields: {', '.join(missing_top)}")
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("mode") not in MODES:
        errors.append(f"mode must be one of: {', '.join(sorted(MODES))}")

    weights = data.get("weights")
    if not isinstance(weights, dict) or not weights:
        errors.append("weights must be a non-empty object")
    else:
        numeric_weights = [value for value in weights.values() if isinstance(value, (int, float)) and not isinstance(value, bool)]
        if len(numeric_weights) != len(weights):
            errors.append("all weights must be numeric")
        elif abs(sum(numeric_weights) - 100) > 0.01:
            errors.append(f"weights must sum to 100, got {sum(numeric_weights):.4g}")
        culture = weights.get("advising_and_culture", weights.get("culture", 0))
        if isinstance(culture, (int, float)) and culture > 10:
            errors.append("culture weight may not exceed 10")

    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        errors.append("candidates must be an array")
        return errors

    required_candidate = {
        "candidate_id",
        "name",
        "organization",
        "institution_type",
        "applicable_routes",
        "score",
        "confidence",
        "status",
        "sources",
    }
    seen_ids: set[str] = set()
    for index, candidate in enumerate(candidates):
        prefix = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(required_candidate - candidate.keys())
        if missing:
            errors.append(f"{prefix} missing: {', '.join(missing)}")
        candidate_id = candidate.get("candidate_id")
        if not isinstance(candidate_id, str) or not ID_PATTERN.fullmatch(candidate_id):
            errors.append(f"{prefix}.candidate_id is invalid")
        elif candidate_id in seen_ids:
            errors.append(f"duplicate candidate_id: {candidate_id}")
        else:
            seen_ids.add(candidate_id)
        score = candidate.get("score")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 100:
            errors.append(f"{prefix}.score must be between 0 and 100")
        if candidate.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}.confidence must be high, medium, or low")
        if candidate.get("status") not in STATUSES:
            errors.append(f"{prefix}.status is invalid")
        if not isinstance(candidate.get("applicable_routes"), list):
            errors.append(f"{prefix}.applicable_routes must be an array")
        sources = candidate.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}.sources must contain at least one source")
        else:
            for source_index, source in enumerate(sources):
                if not isinstance(source, dict) or not source.get("url") or not source.get("title"):
                    errors.append(f"{prefix}.sources[{source_index}] needs url and title")
    return errors


def cmd_init(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    if not args.accept_storage:
        print(f"Mentor Match would store full resumes, preferences, reports, and history in: {root}")
        print("Files are local plain files protected by your device and directory permissions.")
        print("Re-run with --accept-storage after reviewing this location.")
        return 2
    root.mkdir(parents=True, exist_ok=True)
    for name in ("profiles", "archives", "exports"):
        (root / name).mkdir(exist_ok=True)
    config_path = root / "config.json"
    config = read_json(config_path) if config_path.exists() else {"schema_version": 1, "created_at": utc_now()}
    config["storage_consent"] = {"version": CONSENT_VERSION, "accepted_at": utc_now()}
    config["data_root"] = str(root)
    atomic_write_json(config_path, config)
    print(root)
    return 0


def cmd_create_profile(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    path = profile_path(root, args.profile)
    path.mkdir(parents=True, exist_ok=True)
    source_dir = path / "source"
    source_dir.mkdir(exist_ok=True)
    profile_file = path / "profile.json"
    profile = read_json(profile_file) if profile_file.exists() else {
        "schema_version": 1,
        "profile_id": args.profile,
        "created_at": utc_now(),
    }
    profile["display_name"] = args.display_name
    profile["updated_at"] = utc_now()
    if args.preferences:
        profile["preferences"] = load_optional_object(args.preferences, "preferences")
    copied: list[str] = list(profile.get("source_files", []))
    for resume_value in args.resume or []:
        resume = Path(resume_value).expanduser().resolve()
        if not resume.is_file():
            raise FileNotFoundError(f"Resume or source file not found: {resume}")
        destination = source_dir / resume.name
        if destination.exists() and destination.read_bytes() != resume.read_bytes():
            destination = source_dir / f"{resume.stem}-{timestamp_slug()}{resume.suffix}"
        shutil.copy2(resume, destination)
        relative = str(destination.relative_to(path))
        if relative not in copied:
            copied.append(relative)
    profile["source_files"] = copied
    atomic_write_json(profile_file, profile)
    print(path)
    return 0


def cmd_create_case(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    profile = profile_path(root, args.profile)
    if not (profile / "profile.json").is_file():
        raise FileNotFoundError(f"Profile does not exist: {args.profile}")
    path = case_path(root, args.profile, args.case)
    path.mkdir(parents=True, exist_ok=True)
    (path / "runs").mkdir(exist_ok=True)
    case_file = path / "case.json"
    case = read_json(case_file) if case_file.exists() else {
        "schema_version": 1,
        "case_id": args.case,
        "profile_id": args.profile,
        "created_at": utc_now(),
    }
    case["title"] = args.title
    case["updated_at"] = utc_now()
    if args.intent:
        case["intent"] = load_optional_object(args.intent, "intent")
    atomic_write_json(case_file, case)
    print(path)
    return 0


def unique_run_path(runs: Path) -> Path:
    base = timestamp_slug()
    candidate = runs / base
    counter = 2
    while candidate.exists():
        candidate = runs / f"{base}-{counter}"
        counter += 1
    return candidate


def cmd_snapshot(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    case = case_path(root, args.profile, args.case)
    case_file = case / "case.json"
    if not case_file.is_file():
        raise FileNotFoundError(f"Case does not exist: {args.profile}/{args.case}")
    inputs = {
        "report.md": args.report,
        "candidates.csv": args.candidates_csv,
        "candidates.json": args.candidates_json,
        "search-log.md": args.search_log,
    }
    resolved_inputs: dict[str, Path] = {}
    for output_name, raw in inputs.items():
        source = Path(raw).expanduser().resolve()
        if not source.is_file():
            raise FileNotFoundError(f"Required artifact not found: {source}")
        resolved_inputs[output_name] = source
    candidates = read_json(resolved_inputs["candidates.json"])
    errors = validate_candidates(candidates)
    if errors:
        raise ValueError("Invalid candidates JSON:\n- " + "\n- ".join(errors))
    if candidates.get("profile_id") != args.profile or candidates.get("case_id") != args.case:
        raise ValueError("candidates.json profile_id/case_id do not match snapshot target")
    if candidates.get("mode") != args.mode:
        raise ValueError("candidates.json mode does not match --mode")

    runs = case / "runs"
    runs.mkdir(exist_ok=True)
    run = unique_run_path(runs)
    staging = Path(tempfile.mkdtemp(prefix=".snapshot-", dir=runs))
    try:
        for output_name, source in resolved_inputs.items():
            shutil.copy2(source, staging / output_name)
        if args.application_dir:
            application = Path(args.application_dir).expanduser().resolve()
            if not application.is_dir():
                raise FileNotFoundError(f"Application directory not found: {application}")
            shutil.copytree(application, staging / "application")
        run_metadata = {
            "schema_version": 1,
            "profile_id": args.profile,
            "case_id": args.case,
            "mode": args.mode,
            "created_at": utc_now(),
            "artifacts": sorted(item.name for item in staging.iterdir()),
        }
        atomic_write_json(staging / "run.json", run_metadata)
        staging.replace(run)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    case_data = read_json(case_file)
    case_data["latest_run"] = run.name
    case_data["updated_at"] = utc_now()
    atomic_write_json(case_file, case_data)
    print(run)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    result: list[dict[str, Any]] = []
    profiles = root / "profiles"
    for profile_dir in sorted(profiles.iterdir()) if profiles.exists() else []:
        profile_file = profile_dir / "profile.json"
        if not profile_file.is_file():
            continue
        profile = read_json(profile_file)
        cases: list[dict[str, Any]] = []
        cases_dir = profile_dir / "cases"
        for current_case in sorted(cases_dir.iterdir()) if cases_dir.exists() else []:
            case_file = current_case / "case.json"
            if case_file.is_file():
                case_data = read_json(case_file)
                cases.append({
                    "case_id": case_data.get("case_id"),
                    "title": case_data.get("title"),
                    "latest_run": case_data.get("latest_run"),
                })
        result.append({
            "profile_id": profile.get("profile_id"),
            "display_name": profile.get("display_name"),
            "cases": cases,
        })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def selected_path(root: Path, profile_id: str, case_id: str | None) -> Path:
    path = case_path(root, profile_id, case_id) if case_id else profile_path(root, profile_id)
    path = ensure_within(path, root)
    if not path.exists():
        raise FileNotFoundError(f"Stored item not found: {path}")
    return path


def cmd_export(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    source = selected_path(root, args.profile, args.case)
    default_name = f"{args.profile}-{args.case or 'profile'}-{timestamp_slug()}.zip"
    destination = Path(args.output).expanduser().resolve() if args.output else root / "exports" / default_name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.suffix.lower() != ".zip":
        raise ValueError("Export output must end in .zip")
    archive_base = destination.with_suffix("")
    created = Path(shutil.make_archive(str(archive_base), "zip", root_dir=source.parent, base_dir=source.name))
    if created != destination:
        if destination.exists():
            raise FileExistsError(f"Export target already exists: {destination}")
        created.replace(destination)
    print(destination)
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    source = selected_path(root, args.profile, args.case)
    confirmation = f"{args.profile}/{args.case}" if args.case else args.profile
    if args.confirm != confirmation:
        raise PermissionError(f"Archive requires --confirm {confirmation}")
    kind = "cases" if args.case else "profiles"
    destination = root / "archives" / kind / f"{source.name}-{timestamp_slug()}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), destination)
    print(destination)
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    root = data_root(args.root)
    require_consent(root)
    source = selected_path(root, args.profile, args.case)
    confirmation = f"{args.profile}/{args.case}" if args.case else args.profile
    if args.confirm != confirmation:
        raise PermissionError(f"Permanent deletion requires --confirm {confirmation}")
    shutil.rmtree(source)
    print(f"Permanently deleted: {source}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.candidates_json).expanduser().resolve()
    data = read_json(path)
    errors = validate_candidates(data)
    if errors:
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("Candidates JSON is valid")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local Mentor Match profiles, cases, and run artifacts.")
    parser.add_argument("--root", help="Override ~/.mentor-match (or MENTOR_MATCH_HOME).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Initialize storage after one-time informed consent.")
    init.add_argument("--accept-storage", action="store_true")
    init.set_defaults(func=cmd_init)

    profile = subparsers.add_parser("create-profile", help="Create or update an applicant profile.")
    profile.add_argument("--profile", required=True)
    profile.add_argument("--display-name", required=True)
    profile.add_argument("--resume", action="append", help="Resume or source file to copy; repeatable.")
    profile.add_argument("--preferences", help="Path to a JSON object with normalized preferences.")
    profile.set_defaults(func=cmd_create_profile)

    case = subparsers.add_parser("create-case", help="Create or update an application case.")
    case.add_argument("--profile", required=True)
    case.add_argument("--case", required=True)
    case.add_argument("--title", required=True)
    case.add_argument("--intent", help="Path to a JSON object with case intent and scope.")
    case.set_defaults(func=cmd_create_case)

    snapshot = subparsers.add_parser("snapshot", help="Validate and save one immutable research run.")
    snapshot.add_argument("--profile", required=True)
    snapshot.add_argument("--case", required=True)
    snapshot.add_argument("--mode", choices=sorted(MODES), required=True)
    snapshot.add_argument("--report", required=True)
    snapshot.add_argument("--candidates-csv", required=True)
    snapshot.add_argument("--candidates-json", required=True)
    snapshot.add_argument("--search-log", required=True)
    snapshot.add_argument("--application-dir")
    snapshot.set_defaults(func=cmd_snapshot)

    listing = subparsers.add_parser("list", help="List profiles and cases as JSON.")
    listing.set_defaults(func=cmd_list)

    export = subparsers.add_parser("export", help="Export a profile or case as ZIP.")
    export.add_argument("--profile", required=True)
    export.add_argument("--case")
    export.add_argument("--output")
    export.set_defaults(func=cmd_export)

    archive = subparsers.add_parser("archive", help="Move a profile or case to recoverable archives.")
    archive.add_argument("--profile", required=True)
    archive.add_argument("--case")
    archive.add_argument("--confirm", required=True)
    archive.set_defaults(func=cmd_archive)

    delete = subparsers.add_parser("delete", help="Permanently delete a profile or case.")
    delete.add_argument("--profile", required=True)
    delete.add_argument("--case")
    delete.add_argument("--confirm", required=True)
    delete.set_defaults(func=cmd_delete)

    validate = subparsers.add_parser("validate", help="Validate candidates.json.")
    validate.add_argument("candidates_json")
    validate.set_defaults(func=cmd_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (FileExistsError, FileNotFoundError, PermissionError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
