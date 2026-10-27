#!/usr/bin/env python3
"""Download nflverse play-by-play files for auditing, NOT accepted penalty totals.

Source: nflverse/nflverse-data releases, pbp CSV assets. Public availability,
schema and license should be checked before use. This downloader does not claim
that play-by-play penalty flags equal official accepted team penalties.
"""
import argparse
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{season}.csv"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, default=2021)
    p.add_argument("--end", type=int, default=2025)
    p.add_argument("--output", type=Path, default=Path("data/raw/nflverse"))
    a = p.parse_args()
    if a.start < 1999 or a.end > 2025 or a.start > a.end:
        raise SystemExit("Invalid season range for this study")
    a.output.mkdir(parents=True, exist_ok=True)
    for season in range(a.start, a.end + 1):
        url = URL.format(season=season)
        destination = a.output / f"play_by_play_{season}.csv"
        if destination.exists():
            print(f"Already exists: {destination}")
            continue
        print(f"Downloading candidate source {url}")
        try:
            req = Request(url, headers={"User-Agent": "nfl-officiating-research/0.1"})
            with urlopen(req, timeout=120) as response, destination.open("wb") as out:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    out.write(block)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        print(f"Saved {destination}; verify schema, coverage, licensing and official totals.")
    print("Candidate files are NOT validated penalty counts. Do not run statistical conclusions from them.")

if __name__ == "__main__":
    main()
