# Adaptive scoring

Apply hard constraints before scoring. State every exclusion and its reason. Scoring ranks plausible candidates; it does not estimate admission probability.

## Default dimensions

Start from these weights, then adapt them to the intake. Weights must sum to 100.

| Dimension | Default | Evidence |
|---|---:|---|
| Research-question fit | 30 | Current problems and themes |
| Method and skill fit | 15 | Applicant capabilities versus group methods |
| Opportunity and eligibility fit | 15 | Degree/role route and formal requirements |
| Current opening and application evidence | 10 | Current official recruitment or program evidence |
| Funding fit | 10 | Confirmed or competitive funding evidence |
| Research activity and trajectory | 10 | Recent work, projects, team activity, and direction |
| Location and practical constraints | 5 | User-defined constraints |
| Advising and culture signals | 5 | Public, contextualized signals |

Culture signals may never exceed 10%. Prestige has zero default weight; add it only when the user explicitly requests it, and take weight from dimensions the user ranks lower.

## Adaptation rules

- Translate the user's ranked priorities or prose into weights and show the result before or alongside scores.
- Preserve a meaningful research-fit component; if the user requests a ranking unrelated to research fit, label it as a different ranking objective.
- For master's and PhD searches, emphasize degree eligibility and the actual admissions route.
- For postdoc and RA searches, emphasize explicit role fit, methods, timing, funding, and employment eligibility.
- For industry research labs, do not award degree-route points without an official academic partnership.
- Missing evidence lowers confidence and the affected dimension; it is not evidence of a positive or negative fact.

## Per-dimension score

Score each dimension from 0 to 5, then compute:

`weighted points = dimension weight × dimension score / 5`

Use anchors:

- `5`: direct, current, strong evidence;
- `4`: strong fit with a minor gap;
- `3`: plausible fit with meaningful uncertainty;
- `2`: weak or indirect fit;
- `1`: minimal connection;
- `0`: contradiction, ineligibility, or no basis for points.

Round the total to one decimal place. Preserve the unrounded value in JSON if calculated programmatically.

## Confidence

Assign confidence separately from fit:

- `high`: identity, current affiliation, research fit, and opportunity route are supported by current primary sources;
- `medium`: core facts are supported but one important area is indirect, stale, or missing;
- `low`: identity or fit relies mainly on secondary sources, or application status is materially uncertain.

A high fit score with low confidence must be displayed as such and should not outrank a slightly lower, well-supported candidate without explanation.

## Culture signals

Culture scoring may use broad public commentary, but:

- a single anonymous item receives no more than 1/5 for confidence;
- repeated accounts are not independent if they copy the same original claim;
- positive marketing and negative anonymous claims both require context;
- absence of commentary is `unknown`, not positive;
- allegations affecting safety or reputation are summarized cautiously and linked, not amplified as facts.

## Ranking output

Show:

1. the active weights;
2. each candidate's total and confidence;
3. hard-filter exclusions in a separate section;
4. the strongest supporting evidence and largest uncertainty;
5. any manual tie-break rule.

