# Deliverables and data contract

Every completed search produces matching Markdown, CSV, and JSON artifacts. Use UTF-8.

## Markdown report

Use this order:

1. Applicant fit profile, limited to decision-relevant facts.
2. Search scope, mode, access date, languages, and exclusions.
3. Active scoring weights and hard constraints.
4. Ranked candidate table.
5. Top-five analysis: strongest fit, largest risk, and recommended next action.
6. Application routes, deadlines, funding, and external scholarship findings.
7. Excluded candidates and reasons.
8. Unknowns, stale/conflicting evidence, and coverage limitations.
9. Source list with direct links.

The candidate table includes at least:

| Rank | Candidate / group | Organization and unit | Applicable routes | Score | Confidence | Status | Main fit | Main risk | Sources |
|---:|---|---|---|---:|---|---|---|---|---|

Place citations immediately next to the claims they support. Link to the relevant page rather than a search-results page or generic homepage.

## CSV

Use one row per candidate with these headers:

`rank,candidate_id,name,group,organization,unit,country,institution_type,applicable_routes,score,confidence,status,primary_fit,primary_risk,official_url,research_url,admissions_url,last_verified`

Use semicolon-separated values inside multi-value cells. Do not put raw newlines inside cells.

## JSON

Use this top-level shape:

```json
{
  "schema_version": 1,
  "generated_at": "ISO-8601 timestamp",
  "profile_id": "stable-local-id",
  "case_id": "stable-local-id",
  "mode": "quick|standard|deep|refresh",
  "language": "BCP-47 tag or language name",
  "scope": {},
  "weights": {},
  "candidates": []
}
```

Each candidate contains:

```json
{
  "candidate_id": "stable-slug",
  "name": "Official name",
  "group": "Official group name or empty string",
  "organization": "Official organization name",
  "unit": "School, department, center, or unit",
  "country": "Country or region",
  "institution_type": "university|research-institute|industry-lab",
  "applicable_routes": ["masters", "phd", "postdoc", "ra"],
  "score": 0,
  "confidence": "high|medium|low",
  "status": "open-confirmed|open-continuous|program-route|unknown|closed|stale-or-conflicting",
  "dimension_scores": {},
  "primary_fit": "",
  "primary_risk": "",
  "facts": [],
  "inferences": [],
  "culture_signals": [],
  "sources": []
}
```

Every source object includes `url`, `title`, `source_type`, `published_or_updated` when known, `accessed_at`, and a short `supports` list. Do not embed page contents or long quotations.

## File names

For a normal run, use:

- `report.md`
- `candidates.csv`
- `candidates.json`
- `search-log.md`

The search log records query families, coverage, inaccessible sources, and stop reasons without exposing unnecessary resume details.

## Consistency check

Before saving, confirm that ranks, names, scores, statuses, routes, and source URLs match across all three artifacts. A later refresh compares candidate IDs first, then normalized name plus organization when IDs changed.

