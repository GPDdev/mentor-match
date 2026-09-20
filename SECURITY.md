# Security Policy

## Supported version

Security fixes are applied to the latest release on the `main` branch.

## Reporting a vulnerability

Please report suspected vulnerabilities privately to `hejiale@outlook.com`. Include the affected version, reproduction steps, impact, and any suggested mitigation. Do not include real resumes, credentials, private contact details, or other sensitive applicant data in the report.

For non-sensitive defects and feature requests, use [GitHub Issues](https://github.com/GPDdev/mentor-match/issues).

## Security model

Mentor Match is a local-first instruction package with a standard-library storage helper. It has no bundled server, analytics, or background telemetry. Its default data directory, `~/.mentor-match/`, contains plain files and therefore relies on the host account, filesystem permissions, backups, and disk encryption for confidentiality.

The Skill instructs the host Agent to:

- avoid placing full resume text or unnecessary personal data in search queries;
- never store secrets, passwords, session cookies, or API keys in case artifacts;
- require explicit authorization before sending messages or submitting forms;
- separate verified facts from inferences and anecdotal signals;
- validate paths and require exact confirmation for permanent deletion.

Users should review generated outreach and application material before use and should keep the data directory out of public repositories and shared folders.
