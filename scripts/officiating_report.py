#!/usr/bin/env python3
"""Create season/team/conference summaries and charts from verified team-game CSV.

Does not fetch or invent data. Requires the normalized columns described in
docs/DATA_DICTIONARY.md. Charts are descriptive, not proof of officiating bias.
"""
import argparse
from pathlib import Path
import pandas as pd

REQ = ["season", "game_id", "team", "opponent", "conference", "penalties_against", "penalties_for"]
YEARS = set(range(2021, 2026))

def run(source: Path, out: Path):
    if not source.exists():
        raise SystemExit(f"Missing input {source}. Import and audit historical data first.")
    d = pd.read_csv(source)
    absent = set(REQ) - set(d)
    if absent or d.empty or d[REQ].isna().any().any():
        raise SystemExit(f"Missing columns {sorted(absent)} or missing required data")
    if d.duplicated(["game_id", "team"]).any() or not d.season.isin(YEARS).all():
        raise SystemExit("Duplicate team-game keys or invalid season")
    if not d.conference.isin(["AFC", "NFC"]).all():
        raise SystemExit("Invalid conference")
    for c in ["penalties_against", "penalties_for"]:
        v = pd.to_numeric(d[c], errors="coerce")
        if v.isna().any() or (v < 0).any() or (v % 1 != 0).any():
            raise SystemExit(f"Invalid counts in {c}")
        d[c] = v.astype(int)
    if not d.groupby("game_id").size().eq(2).all():
        raise SystemExit("Each game must have two team records")
    for gid, p in d.groupby("game_id"):
        a, b = p.iloc[0], p.iloc[1]
        if a.team != b.opponent or b.team != a.opponent or a.penalties_against != b.penalties_for or b.penalties_against != a.penalties_for:
            raise SystemExit(f"Nonreciprocal records in {gid}")
    d["net_against"] = d.penalties_against - d.penalties_for
    dims = {
        "team_by_season": ["season", "conference", "team"],
        "team_five_year": ["conference", "team"],
        "conference_by_season": ["season", "conference"],
        "conference_five_year": ["conference"],
    }
    out.mkdir(parents=True, exist_ok=True)
    tables = {}
    for name, keys in dims.items():
        t = d.groupby(keys, as_index=False).agg(games=("game_id", "size"), against=("penalties_against", "sum"), favorable=("penalties_for", "sum"), net_against=("net_against", "sum"))
        t["against_per_game"] = t.against / t.games
        t["net_per_game"] = t.net_against / t.games
        t.to_csv(out / (name + ".csv"), index=False)
        tables[name] = t
    team = tables["team_five_year"]
    team["league_rank_against_per_game"] = team.against_per_game.rank(method="min", ascending=False).astype(int)
    team.sort_values("league_rank_against_per_game").to_csv(out / "team_league_rankings.csv", index=False)
    dal = tables["team_by_season"].query("team == 'DAL'").sort_values("season")
    dal.to_csv(out / "dallas_by_season.csv", index=False)
    east = team[team.team.isin(["DAL", "NYG", "PHI", "WAS"])]
    east.to_csv(out / "nfc_east_comparison.csv", index=False)
    print(f"Created {len(tables)+3} descriptive CSV summaries in {out}")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Install matplotlib to generate charts.")
        return
    ranking = team.sort_values("against_per_game")
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.barh(ranking.team, ranking.against_per_game)
    ax.set(xlabel="Accepted penalties against per team-game", title="NFL team penalty rates (2021–2025; observed data)")
    fig.tight_layout(); fig.savefig(out / "team_ranking.png", dpi=160); plt.close(fig)
    if not dal.empty:
        fig, ax = plt.subplots()
        ax.plot(dal.season, dal.net_per_game, marker="o")
        ax.axhline(0, linewidth=1)
        ax.set(xlabel="Season", ylabel="Net accepted penalties against per game", title="Dallas penalty differential")
        ax.set_xticks(dal.season)
        fig.tight_layout(); fig.savefig(out / "dallas_trend.png", dpi=160); plt.close(fig)
    conf = tables["conference_five_year"]
    fig, ax = plt.subplots()
    ax.bar(conf.conference, conf.against_per_game)
    ax.set(ylabel="Accepted penalties against per team-game", title="AFC vs NFC (observed data)")
    fig.tight_layout(); fig.savefig(out / "conference_comparison.png", dpi=160); plt.close(fig)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("outputs/officiating"))
    a = p.parse_args()
    run(a.input, a.output)
