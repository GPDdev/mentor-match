# Behavioral evaluation

Run each entry in `cases.jsonl` in a fresh conversation with the plugin installed. Use synthetic resumes and fictional institutions when testing structure; use real public institutions only when evaluating web-research quality.

For each case, record:

- whether the Skill triggered correctly;
- whether the requested mode and scope were followed;
- whether every listed invariant held;
- whether source links directly supported claims;
- whether Markdown, CSV, and JSON agreed;
- any unnecessary question, unsupported claim, privacy leak, or external mutation.

A release candidate passes when all positive cases satisfy every invariant and negative cases do not activate Mentor Match. Web-dependent cases must be rerun close to release because source availability changes.

Do not score exact prose or heading names. Evaluate observable behavior and artifacts.

