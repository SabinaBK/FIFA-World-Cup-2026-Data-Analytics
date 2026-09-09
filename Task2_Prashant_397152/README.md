Project title:
FIFA World Cup 2026: Fouls and Match Outcome

Analytical Question: Is there a significant difference in average fouls committed per match between winning and losing teams? 

Note: The primary source contained 103 records. The official third-place
play-off was missing and was added as one verified supplementary record
from FBref, producing a final dataset of 104 matches.

Data Sources: 
The Stats Don't Lie: https://www.thestatsdontlie.com/football/world-cup-2026/
FB Ref: https://fbref.com/en/

Here, I have extracted embedded file from the site The Stats Don't Lie and got this google sheets endpoint which is used by that website and I used python for the futher data extratction. And in that website there was only 103 games foul data and I took one missing data from the other approved site FBREF and made the data of 104 games and done the data wrangling and proceed with the analysis. I have attached the endpoint link below:

Published Google Sheets endpoint: https://docs.google.com/spreadsheets/d/e/2PACX-1vSWZFlaUHTBK09v4I1Kv7ZQ0ophhlpsCr7VPFW5dkbdG0Zpl8mRkXrTZezZMr1Ia9V9cpwmq7BKPQ03/pubhtml/sheet?headers=false&gid=995472238

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

And supporting output:
outputs/fouls_descriptive_statistics.csv
outputs/fouls_confidence_intervals.csv
utputs/fouls_hypothesis_test_results.csv
outputs/fouls_histograms_winning_vs_losing.png

Final result:
Welch independent-samples t-test:

Null Hypothesis (H0): mu_win = mu_loss (No difference in average fouls)
Alternative Hypothesis (H1) : mu_win != mu_loss (Difference in average fouls exists)
Mean difference (winner - loser): -1.1548
t-statistic: -1.8490
Degrees of freedom: 164.5776
Two-tailed p-value: 0.0662
Significance level: 0.05
Decision: Fail to reject H0