# Regenerating the original NFL officiating analysis

## 1. Install
```bash
python -m pip install -r requirements.txt
```

## 2. Download candidate raw source (optional)
```bash
python scripts/download_candidate_pbp.py --start 2021 --end 2025
```
This downloads nflverse play-by-play candidate CSVs into ignored `data/raw/nflverse/`. **Do not treat penalty flags as verified accepted penalty counts.** nflverse field definitions and source availability may change; verify license and official gamebook totals. This step does not produce normalized analysis input.

## 3. Build and audit accepted team-game input
Create `data/processed/team_game_penalties.csv` from an authoritative penalty dataset or audited official gamebooks, following [the data dictionary](DATA_DICTIONARY.md). Two reciprocal rows per game; 2021–2025 regular season only. Validate all teams, game coverage, accepted status, assessed yards, and source provenance. This transformation remains to be implemented after selecting and auditing a trustworthy source.

## 4. Generate tables and charts
```bash
python scripts/officiating_report.py --input data/processed/team_game_penalties.csv --output outputs/officiating
```

## 5. Recreate Excel workbook
```bash
python scripts/export_workbook.py --input-dir outputs/officiating --output outputs/nfl_penalty_analysis_2021_2025_regenerated.xlsx
```
Creates sheets for all-team, conference, Dallas, NFC East and rankings. PNG charts are generated in `outputs/officiating/`. The original historical workbook's exact formatting and any unverified results are not guaranteed to match.

## Current limitation
The pipeline is **not yet end-to-end**. The download stage gathers candidate raw plays, but accepted penalty extraction and official-gamebook verification are pending. No real data or verified findings have been committed.
