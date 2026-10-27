# Candidate data sources and provenance

- **Penalty records:** evaluate official NFL gamebooks, NFL play-by-play data and public aggregators. Confirm accepted, declined and offsetting status, attribution and assessed yards. Validate play-level aggregates against official gamebooks.
- **Game metadata:** stable game ID, date, week, season, home/away, opponent, final score and team conference.
- **Officiating:** verified crew assignments and substitutions, with source references.
- **Betting:** documented historical closing spread, totals and moneylines, sportsbook/consensus definition, timestamps and licensing. Do not infer lines from scores.

Maintain a provenance ledger for source URL, retrieval date, license, version, coverage, transformation, join key and missingness. Do not commit licensed restricted data, secrets or personal tokens.

**Current state:** no datasets have been ingested or verified.
