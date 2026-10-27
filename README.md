# NFL Officiating and Betting Analysis

Reproducible research investigating whether the Dallas Cowboys experience more **unfavorable accepted penalties** than comparable NFL teams, and whether game-level penalty differentials are associated with historical betting markets.

**Status: research scaffold. No empirical results verified yet.** Do not interpret hypotheses as findings.

## Scope
Five completed regular seasons (2021–2025), all 32 teams, NFC/AFC comparisons, team rankings, Dallas versus NFC East and league, penalties against and for, assessed yards where available, and historical closing spread/ATS outcomes when verified data can be obtained.

## Run
```bash
pip install -r requirements.txt
python scripts/analyze_penalties.py --input data/processed/team_game_penalties.csv --output outputs
```
The input file must be sourced and validated first. This repository contains **no fabricated penalty or betting data**.

## Documents
- [Methodology](docs/METHODOLOGY.md)
- [Hypotheses and unverified findings](docs/FINDINGS_STATUS.md)
- [Sources and provenance](docs/DATA_SOURCES.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)

## Important limitation
Penalty frequency is not a measure of officiating accuracy. Playing style, opponents, situation, home field, and crew assignments may confound comparisons. Betting correlations cannot establish manipulation or intentional bias. An assessment of wrong or missed calls requires independent review of called **and uncalled** infractions.
