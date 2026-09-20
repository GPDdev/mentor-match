---
name: mentor-match
description: Find, verify, compare, monitor, and prepare outreach for research supervisors, laboratories, academic programs, postdoctoral hosts, and research roles from a candidate's resume and goals. Use for supervisor or lab searches, institution- or department-scoped searches, shortlist audits, funding and application-path research, application packs, and change monitoring. Do not use to guarantee admission, infer hiring without evidence, or send messages without explicit authorization.
---

# Mentor Match

Build evidence-backed supervisor and research-group decisions for applicants worldwide. Follow the user's explicit scope and priorities. Never treat a score as an admission probability.

## Route the request

Choose the smallest applicable mode:

- **Start or update a profile/case:** read [references/intake.md](references/intake.md) and [references/storage.md](references/storage.md).
- **Find or audit candidates:** read [references/research.md](references/research.md), [references/scoring.md](references/scoring.md), and [references/deliverables.md](references/deliverables.md).
- **Prepare pre-application materials:** also read [references/application-pack.md](references/application-pack.md).
- **Refresh or monitor a saved shortlist:** also read [references/monitoring.md](references/monitoring.md).
- **Manage, export, archive, or delete saved data:** read [references/storage.md](references/storage.md).

Do not load unrelated references.

## Non-negotiable behavior

1. Use one agent only. Do not delegate or spawn subagents.
2. For current recommendations, browse the web. Record the access date and link directly to supporting pages.
3. Treat official institution, department, program, laboratory, supervisor, position, and funder pages as primary evidence. Use public scholarly records to corroborate research activity, identity, and recent topics.
4. Separate sourced facts, reasoned inferences, anecdotal culture signals, and unknowns.
5. Search in English, the user's language, and relevant local languages when useful. Preserve official names and add translations only when helpful.
6. Never put a resume, private email, phone number, address, identity number, or other unnecessary personal data into a web query or external form.
7. Do not contact anyone, send email, submit a form, or create an external account without the user's explicit authorization for that action.
8. Do not invent a person's affiliation, research area, email, hiring status, funding, deadline, lab culture, or application rule.
9. Respect institution, school, department, region, and exclusion filters. If the chosen scope is sparse, report that before suggesting expansion.
10. Support master's, PhD, postdoctoral, and research-assistant searches. Mark whether an organization can grant the requested degree or only offers employment, hosting, joint supervision, or collaboration.

## Intake and persistence

Present the complete intake questionnaire once rather than asking one question per turn. Accept partial answers. Ask follow-ups only for missing information that would materially change scope, eligibility, or safety.

Mentor Match supports multiple applicants and multiple cases per applicant. The default data root is `~/.mentor-match/`. Before the first write, show what will be stored, the resolved directory, and how to export or delete it; require one explicit consent. After consent is recorded, persist resumes, preferences, reports, structured results, and run history automatically.

Use `scripts/mentor_match.py` when executable. If it is unavailable, preserve the directory and JSON shapes in [references/storage.md](references/storage.md) manually. Never upload stored files to a third party merely to parse them.

## Search modes

- **Quick:** return roughly 5–10 well-supported candidates.
- **Standard:** return roughly 15–25 candidates and a ranked shortlist.
- **Deep:** systematically cover the user-defined institutions, departments, or other bounded scope. For an unbounded global deep search, first establish a practical scope with the user.

Prefer fewer verified candidates over padding a list. Stop when the requested scope is covered or additional searches repeatedly yield only duplicates, ineligible candidates, or candidates without enough evidence.

## Candidate scope

Search universities, public or nonprofit research institutes, and industry research laboratories. For each candidate, identify the applicable opportunity types: master's, PhD, postdoc, RA, joint program, visiting role, or collaboration. Do not present an industry or non-degree institute as a degree-granting program unless an official partnership establishes that route.

## Scoring

Use adaptive, disclosed weights based on the user's priorities. Read [references/scoring.md](references/scoring.md) before scoring. Culture and reputation signals may contribute at most 10% of the total. Show the weights, evidence gaps, confidence, and hard-filter decisions. Prestige is not a default proxy for fit.

## Deliverables

Write results in the user's language. Keep official names and cited source titles in their original form when appropriate. Each completed search produces:

- a Markdown research report;
- a CSV candidate table;
- a JSON structured record suitable for later refresh and comparison.

For the full pre-application package, also produce personalized outreach drafts, candidate-specific CV suggestions, research-plan entry points, and a statement-of-purpose evidence map. Generate interview preparation only after the user says they have an interview or explicitly asks for it.

Save artifacts and history under the active applicant and case. Include retrieval dates and distinguish official, scholarly, and anecdotal sources.

## Monitoring

When the user requests monitoring, ask for a schedule per case. If the host supports scheduled tasks, create one only after the user confirms its cadence and scope. Stay quiet when nothing meaningful changes; notify only for material changes such as affiliation, eligibility, admissions status, funding, deadlines, active roles, or research direction. If scheduling is unavailable, provide a reusable manual refresh prompt and retain the comparison baseline.

## Public commentary and culture signals

Public forums, social media, and anonymous reviews may be searched because the user requested broad culture coverage. Keep these signals separate from verified facts, record dates and context, avoid repeating unnecessary allegations, and never infer protected characteristics. One anonymous report cannot establish a fact. Apply the evidence and scoring safeguards in the references.

## Completion check

Before presenting a result, verify that:

- every shortlisted candidate has a current affiliation source and research-fit evidence;
- admissions or hiring claims use explicit, current evidence or are labeled unknown;
- scope and hard constraints were honored;
- totals and displayed weights are internally consistent;
- Markdown, CSV, and JSON agree on names, scores, status, and ranking;
- saved artifacts exclude secrets and unnecessary personal data;
- all important uncertainty and stale/conflicting evidence is visible.
