# Normalized team-game input schema

Required CSV fields:
- `season`: integer 2021–2025
- `game_id`: stable game identifier
- `team`: team abbreviation
- `opponent`: opposing team abbreviation
- `conference`: AFC or NFC
- `penalties_against`: nonnegative integer, accepted penalties against this team
- `penalties_for`: nonnegative integer, accepted penalties against opponent

Optional: `yards_against`, `yards_for`, `home_away`, `referee`, `closing_spread_team`, `ats_margin_team`, `source_id`.

Every game must have two reciprocal rows. `penalties_against` in one must equal `penalties_for` in the other. Missing values are not zeros. For betting, document the sign convention: `ats_margin_team = team_score - opponent_score + closing_spread_team`.
