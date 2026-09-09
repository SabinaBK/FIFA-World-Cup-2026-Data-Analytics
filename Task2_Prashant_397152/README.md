Project title:
FIFA World Cup 2026: Fouls and Match Outcome

Note: The primary source contained 103 records. The official third-place
play-off was missing and was added as one verified supplementary record
from FBref, producing a final dataset of 104 matches.

Run order:
1. scripts/01_extract_match_fouls.py
2. scripts/02_prepare_team_match_fouls.py
3. scripts/03_statistical_analysis.py

Input:
data/raw/world_cup_2026_match_fouls_raw.csv

Prepared dataset:
data/processed/team_match_fouls_prepared.csv

Main output:
outputs/fouls_statistical_summary.txt

Final result:
Welch independent-samples t-test:
t(164.58) = −1.85, p = 0.066
Decision: Fail to reject H0 at α = 0.05