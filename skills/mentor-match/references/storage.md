# Local storage and data control

Mentor Match supports multiple applicant profiles and multiple application cases per profile. The default root is `~/.mentor-match/`. A user may override it with the `MENTOR_MATCH_HOME` environment variable or the script's `--root` option.

## First-write consent

Before the first write, show:

- the resolved absolute data root;
- that complete resumes, preferences, reports, structured candidate data, and run history may be stored there;
- that files are local plain files and rely on the user's device and directory security;
- how to list, export, archive, and permanently delete data.

Require explicit one-time consent. Record only the consent version and timestamp in `config.json`. Do not treat installation alone as consent.

## Directory layout

```text
~/.mentor-match/
├── config.json
├── profiles/
│   └── <profile-id>/
│       ├── profile.json
│       ├── source/
│       └── cases/
│           └── <case-id>/
│               ├── case.json
│               └── runs/
│                   └── <timestamp>/
│                       ├── run.json
│                       ├── report.md
│                       ├── candidates.csv
│                       ├── candidates.json
│                       ├── search-log.md
│                       └── application/
├── archives/
└── exports/
```

Use stable, filesystem-safe lowercase IDs. Keep display names in JSON rather than filenames.

## Script workflow

When available, run `scripts/mentor_match.py --help` and use its commands:

- `init --accept-storage`
- `create-profile`
- `create-case`
- `snapshot`
- `list`
- `export`
- `archive`
- `delete`

Do not claim a write succeeded without checking the command result and resulting path.

## Automatic persistence

After recorded consent:

- save new resumes and supporting files under the profile's `source/` directory;
- save normalized preferences and relevant profile facts in `profile.json`;
- save each search or refresh as a new immutable timestamped run;
- never overwrite an earlier run;
- keep monitoring baselines in the most recent successful run;
- do not store API keys, passwords, access tokens, session cookies, or private messages.

## Export, archive, and delete

- Export produces a ZIP containing the requested profile or case.
- Archive moves a profile or case into the root `archives/` directory and preserves recovery information.
- Permanent delete requires the exact profile and optional case ID as confirmation. Resolve the path and verify it remains under the configured root before deletion.
- Explain what was removed and whether it is recoverable.

If the host cannot run the script, reproduce the layout carefully using native file tools. Ask for authorization immediately before a permanent delete.

## Portability and degradation

Core research works without persistence. If the host cannot write to the user directory, ask for an alternative writable directory and record it for that session. Do not silently fall back to a public repository, synced drive, or temporary directory.

