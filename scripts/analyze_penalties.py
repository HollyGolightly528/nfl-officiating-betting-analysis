#!/usr/bin/env python3
"""Validate and summarize accepted penalties by team and conference."""
import argparse
from pathlib import Path
import pandas as pd

REQUIRED = ["season", "game_id", "team", "opponent", "conference",
            "penalties_against", "penalties_for"]

def analyze(source: Path, output: Path) -> None:
    if not source.exists():
        raise SystemExit(f"Input not found: {source}. Ingest verified data first.")
    df = pd.read_csv(source)
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")
    if df.empty or df[REQUIRED].isna().any().any():
        raise SystemExit("Empty input or missing required values.")
    if df.duplicated(["game_id", "team"]).any():
        raise SystemExit("Duplicate game/team rows.")
    if not df.conference.isin(["AFC", "NFC"]).all():
        raise SystemExit("Invalid conference values.")
    if not df.season.isin(range(2021, 2026)).all():
        raise SystemExit("Expected completed seasons 2021–2025.")
    for col in ("penalties_against", "penalties_for"):
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any() or (values < 0).any() or (values % 1 != 0).any():
            raise SystemExit(f"Invalid penalty counts in {col}")
        df[col] = values.astype(int)
    if not df.groupby("game_id").size().eq(2).all():
        raise SystemExit("Expected two team rows per game.")
    for game_id, pair in df.groupby("game_id"):
        a, b = pair.iloc[0], pair.iloc[1]
        if (a.team != b.opponent or b.team != a.opponent or
            a.penalties_against != b.penalties_for or
            b.penalties_against != a.penalties_for):
            raise SystemExit(f"Nonreciprocal records in game {game_id}")
    df["net_against"] = df.penalties_against - df.penalties_for
    team = df.groupby(["conference", "team"], as_index=False).agg(
        games=("game_id", "size"),
        against=("penalties_against", "sum"),
        favorable=("penalties_for", "sum"),
        net_against=("net_against", "sum"))
    team["against_per_game"] = team.against / team.games
    team["net_per_game"] = team.net_against / team.games
    team = team.sort_values(["conference", "against_per_game"], ascending=[True, False])
    conference = df.groupby("conference", as_index=False).agg(
        team_games=("game_id", "size"),
        against=("penalties_against", "sum"),
        favorable=("penalties_for", "sum"))
    conference["against_per_team_game"] = conference.against / conference.team_games
    output.mkdir(parents=True, exist_ok=True)
    team.to_csv(output / "team_summary.csv", index=False)
    conference.to_csv(output / "conference_summary.csv", index=False)
    print("Dallas:")
    print(team.loc[team.team.eq("DAL")].to_string(index=False))
    print(f"Outputs saved to {output}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", default=Path("outputs"), type=Path)
    args = p.parse_args()
    analyze(args.input, args.output)
