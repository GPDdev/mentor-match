# Mentor Match

[English](README.md) | [简体中文](README.zh-CN.md)

Mentor Match is an evidence-backed Agent Skill for finding, verifying, comparing, and monitoring research supervisors, laboratories, academic programs, postdoctoral hosts, research-assistant roles, and funding opportunities.

It is designed for applicants worldwide and supports universities, public or nonprofit research institutes, and industry research labs. The core skill follows the open Agent Skills layout and is packaged as a ChatGPT/Codex plugin.

## What it does

- Reads a resume and a one-time application questionnaire.
- Searches the live web instead of shipping a stale supervisor database.
- Restricts searches to named universities, schools, departments, institutes, or companies when requested.
- Supports master's, PhD, postdoc, and RA searches.
- Separates verified facts, inferences, anecdotal culture signals, and unknowns.
- Uses visible, adaptive scoring; culture signals can contribute at most 10%.
- Produces matching Markdown, CSV, and JSON results.
- Builds optional pre-application packs with outreach drafts, CV suggestions, research-plan entry points, and statement evidence maps.
- Monitors saved shortlists when the host supports scheduling and notifies only on meaningful changes.
- Keeps multiple applicant profiles, cases, and immutable run histories locally.

Mentor Match never guarantees admission, funding, hiring, or a reply. It does not send messages or submit forms without explicit user authorization.

## Package layout

```text
mentor-match/
├── .codex-plugin/plugin.json
├── skills/mentor-match/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   ├── scripts/mentor_match.py
│   └── references/
├── scripts/mentor_match.py  # repository convenience entry point
├── tests/
├── evals/
├── submission/
├── PRIVACY.md
├── SECURITY.md
├── TERMS.md
└── LICENSE
```

## Use

After installing the plugin, invoke it explicitly or ask naturally:

```text
$mentor-match Match my CV with PhD supervisors in computational biology.
```

```text
Search these three universities for suitable robotics labs and build a full pre-application pack.
```

```text
Refresh my saved 2027 postdoc shortlist and report only meaningful changes.
```

The first new profile receives a complete questionnaire. Before any persistent write, Mentor Match shows the local storage path and requests one-time informed consent.

## Local data

The default data root is `~/.mentor-match/`. It can be overridden with `MENTOR_MATCH_HOME` or `--root`.

The helper uses only the Python standard library:

```bash
python scripts/mentor_match.py --help
python scripts/mentor_match.py init
python scripts/mentor_match.py init --accept-storage
python scripts/mentor_match.py list
```

The first `init` command only explains storage and exits without writing. The second records consent and creates the local structure. Export, archive, and permanent-delete commands are documented in `--help`; destructive commands require the exact profile or case ID as confirmation.

## Research sources

Official institution, program, department, laboratory, supervisor, position, and funder pages are primary evidence. Scholarly records such as DOI pages, Crossref, public ORCID profiles, and OpenAlex records may corroborate identity and current research. Forums, social media, and anonymous reviews are treated as lower-confidence culture signals rather than facts.

No API key is required by the plugin. Optional sources that require credentials or impose changing limits must degrade gracefully to public pages or other evidence.

## Development

Run the deterministic checks:

```bash
python -m unittest discover -s tests -v
python scripts/mentor_match.py validate path/to/candidates.json
```

Validate the Skill and plugin before packaging:

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/mentor-match
python /path/to/plugin-creator/scripts/validate_plugin.py .
```

Behavioral evaluation prompts and invariants live under `evals/`.

Submission-ready listing copy, review cases, and release notes live under `submission/`. Identity verification, portal permissions, final country selection, and publication remain publisher-controlled actions.

## Privacy and terms

See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md). Issues and support requests may be filed at [GitHub Issues](https://github.com/GPDdev/mentor-match/issues) or sent to `hejiale@outlook.com`.

## License

Apache License 2.0. See [LICENSE](LICENSE).
