#!/usr/bin/env python3
"""Export verified descriptive officiating CSV summaries to an Excel workbook."""
import argparse
from pathlib import Path
import pandas as pd

TABLES = [
    ("Team Seasons", "team_by_season.csv"),
    ("Team Five Year", "team_five_year.csv"),
    ("League Rankings", "team_league_rankings.csv"),
    ("Conference Seasons", "conference_by_season.csv"),
    ("Conference Five Year", "conference_five_year.csv"),
    ("Dallas Seasons", "dallas_by_season.csv"),
    ("NFC East", "nfc_east_comparison.csv"),
]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", type=Path, default=Path("outputs/officiating"))
    p.add_argument("--output", type=Path, default=Path("outputs/nfl_penalty_analysis_2021_2025_regenerated.xlsx"))
    args = p.parse_args()
    absent = [str(args.input_dir / name) for _, name in TABLES if not (args.input_dir / name).exists()]
    if absent:
        raise SystemExit("Missing report tables. Run officiating_report.py first: " + ", ".join(absent))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
        for sheet, filename in TABLES:
            frame = pd.read_csv(args.input_dir / filename)
            frame.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for col in ws.columns:
                letter = col[0].column_letter
                ws.column_dimensions[letter].width = min(36, max(12, max(len(str(c.value or "")) for c in col) + 2))
        notes = pd.DataFrame({"Caution": [
            "Descriptive counts are not proof of officiating errors or bias.",
            "Data must be independently sourced and validated against official gamebooks.",
            "This workbook is not a betting analysis.",
            "Verify complete 2021–2025 season coverage before interpreting rankings.",
        ]})
        notes.to_excel(writer, sheet_name="Read Me", index=False)
    print(f"Workbook created: {args.output}")

if __name__ == "__main__":
    main()
