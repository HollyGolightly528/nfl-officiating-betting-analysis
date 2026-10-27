# Research methodology

## Design
Exploratory observational study of the 2021–2025 NFL regular seasons. Use one row per team per game (two rows per game). Playoffs are excluded from the primary analysis.

## Outcomes
- Unfavorable: accepted penalties assessed against a team.
- Favorable: accepted penalties assessed against the opposing team.
- Net differential: unfavorable minus favorable; positive is worse for the focal team.
- Yards differential: assessed penalty yards against minus assessed yards on opponent.
- Declined and offsetting flags: track separately, not as accepted penalties.

## Analysis plan
1. Audit game coverage, team identifiers, duplicate keys, penalty status and data provenance.
2. Summarize penalties per game, yards and net differential by season, conference, team and Dallas specifically.
3. Compare Dallas with the NFC East, NFC and league; report sample sizes and uncertainty.
4. Stratify by home/away, season, opponent, penalty type and officiating crew when available.
5. Consider play volume, score state, game situation, team tendencies and opponent strength as confounders.
6. Join verified closing betting odds by stable game identifier and kickoff date. Define spread convention and ATS pushes explicitly.
7. Explore associations with closing spread, ATS result and penalties; use appropriate covariates, sensitivity analyses and multiple-testing correction.

## Inference
More assessed penalties do not establish erroneous officiating or discrimination. Correlation with betting does not establish causation or manipulation. Testing actual call correctness would require independent blinded film review of called and uncalled fouls, coding consistency and inter-rater agreement.

## Reproducibility
Record data source, license, download date, schema version, cleaning steps, missingness, game coverage and model assumptions. Report negative and null results. Do not publish unverified numbers as findings.
