# Monitoring and refresh

Monitoring is configured per application case. Ask the user for cadence, time zone, start time if relevant, and an end date or stopping condition.

## Baseline

Use the latest successful `candidates.json` as the baseline. Before monitoring, ensure candidate IDs, source URLs, status, current affiliation, and last-verified dates are present.

## Refresh targets

Check for material changes in:

- current affiliation, role, or laboratory membership;
- application route or supervisor-contact rule;
- admissions or hiring status;
- open positions, deadlines, and funding;
- research themes and recent activity;
- official contact page;
- significant, corroborated culture or reputation signals.

Do not alert merely because a page's formatting, ordering, tracking parameters, or retrieval timestamp changed.

## Scheduler behavior

If the host supports scheduled tasks or thread heartbeats:

1. Show the proposed cadence and scope.
2. Obtain confirmation before creating the schedule.
3. Tell the scheduled task to remain quiet while nothing meaningful changes.
4. Notify on a material change, completion, failure, or required user action.
5. Stop at the configured end date, after the application cycle, or when the user cancels it.

If scheduling is unavailable, save a refresh prompt containing the case ID, scope, and comparison instructions. Do not pretend monitoring is active.

## Refresh output

Create a new immutable run with:

- updated Markdown, CSV, and JSON;
- a `changes.md` summary;
- added, removed, and materially changed candidates;
- old and new evidence links and dates;
- an explanation for score changes.

Keep earlier runs. Never rewrite history to make sources appear current.

## Notification threshold

Notify for changes likely to affect the applicant's decision or timing. For uncertain changes, state what was observed and what still needs verification. Do not turn an unavailable page into a claim that an opportunity closed.

