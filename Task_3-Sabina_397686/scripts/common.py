"""
common.py — Shared paths, data loading, and analysis helpers for the
FIFA World Cup 2026 corners analysis project (Task 3).
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt
import statistics as stats_mod


# PATHS
DATA_DIR = Path("../data")
RAW_DIR = DATA_DIR / "raw data"
PROCESSED_DIR = DATA_DIR / "processed data"
SAMPLE_DIR = DATA_DIR / "sample data"
OUTPUT_FOLDER = Path("../output")

RAW_PATH = RAW_DIR / "fifaworldcup2026_matches_raw.csv"
PROCESSED_PATH = PROCESSED_DIR / "fifaworldcup2026_team_match_corners_prepared.csv"
GROUP_SAMPLE_PATH = SAMPLE_DIR / "sample_group_corners.csv"
KNOCKOUT_SAMPLE_PATH = SAMPLE_DIR / "sample_knockout_corners.csv"

for folder in (RAW_DIR, PROCESSED_DIR, SAMPLE_DIR, OUTPUT_FOLDER):
    folder.mkdir(parents=True, exist_ok=True)

SAMPLE_SIZE_GROUP = 50
SAMPLE_SIZE_KNOCKOUT = 50
RANDOM_STATE = 42


# DATA EXTRACTION
def extract_raw_matches():
    """Builds the raw list of FIFA World Cup 2026 matches with corner counts
    for each team, and returns it as a DataFrame (wide format: one row per
    match, corners_t1/corners_t2 side by side)."""

    matches = []
    matches.append({
        "date": "2026-06-11",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Mexico",
        "team2": "South Africa",
        "corners_t1": 3, # Number of corners for team 1
        "corners_t2": 1 # Number of corners for team 2
    })
    matches.append({
        "date": "2026-06-12",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "South Korea",
        "team2": "Czech Republic",
        "corners_t1": 4,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-12",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Canada",
        "team2": "Bosnia & Herzegovina",
        "corners_t1": 9,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-13",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "USA",
        "team2": "Paraguay",
        "corners_t1": 3,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-13",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Qatar",
        "team2": "Switzerland",
        "corners_t1": 3,
        "corners_t2": 10
    })
    matches.append({
        "date": "2026-06-13",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Brazil",
        "team2": "Morocco",
        "corners_t1": 6,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-14",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Haiti",
        "team2": "Scotland",
        "corners_t1": 4,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-14",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Australia",
        "team2": "Turkey",
        "corners_t1": 5,
        "corners_t2": 8
    })
    matches.append({
        "date": "2026-06-14",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Germany",
        "team2": "Curacao",
        "corners_t1": 8,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-14",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Netherlands",
        "team2": "Japan",
        "corners_t1": 5,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-15",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Ivory Coast",
        "team2": "Ecuador",
        "corners_t1": 3,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-15",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Sweden",
        "team2": "Tunisia",
        "corners_t1": 4,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-15",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Spain",
        "team2": "Cape Verde",
        "corners_t1": 11,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-15",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Belgium",
        "team2": "Egypt",
        "corners_t1": 2,
        "corners_t2": 7
    })
    matches.append({
        "date": "2026-06-15",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Saudi Arabia",
        "team2": "Uruguay",
        "corners_t1": 4,
        "corners_t2": 14
    })
    matches.append({
        "date": "2026-06-16",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Iran",
        "team2": "New Zealand",
        "corners_t1": 4,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-16",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "France",
        "team2": "Senegal",
        "corners_t1": 6,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-16",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Iraq",
        "team2": "Norway",
        "corners_t1": 2,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-17",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Argentina",
        "team2": "Algeria",
        "corners_t1": 2,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-17",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Austria",
        "team2": "Jordan",
        "corners_t1": 4,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-17",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Portugal",
        "team2": "D.R. Congo",
        "corners_t1": 5,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-17",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "England",
        "team2": "Croatia",
        "corners_t1": 8,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-18",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Ghana",
        "team2": "Panama",
        "corners_t1": 2,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-18",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Uzbekistan",
        "team2": "Colombia",
        "corners_t1": 3,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-18",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Czech Republic",
        "team2": "South Africa",
        "corners_t1": 5,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-18",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Switzerland",
        "team2": "Bosnia & Herzegovina",
        "corners_t1": 7,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-18",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Canada",
        "team2": "Qatar",
        "corners_t1": 19,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-19",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Mexico",
        "team2": "South Korea",
        "corners_t1": 0,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-19",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "USA",
        "team2": "Australia",
        "corners_t1": 7,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-19",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Scotland",
        "team2": "Morocco",
        "corners_t1": 2,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-20",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Brazil",
        "team2": "Haiti",
        "corners_t1": 4,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-20",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Turkey",
        "team2": "Paraguay",
        "corners_t1": 12,
        "corners_t2": 0
    })
    matches.append({
        "date": "2026-06-20",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Netherlands",
        "team2": "Sweden",
        "corners_t1": 2,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-20",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Germany",
        "team2": "Ivory Coast",
        "corners_t1": 8,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-21",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Ecuador",
        "team2": "Curacao",
        "corners_t1": 9,
        "corners_t2": 0
    })
    matches.append({
        "date": "2026-06-21",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Tunisia",
        "team2": "Japan",
        "corners_t1": 3,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-21",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Spain",
        "team2": "Saudi Arabia",
        "corners_t1": 6,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-21",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Belgium",
        "team2": "Iran",
        "corners_t1": 4,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-21",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Uruguay",
        "team2": "Cape Verde",
        "corners_t1": 11,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-22",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "New Zealand",
        "team2": "Egypt",
        "corners_t1": 4,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-22",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Argentina",
        "team2": "Austria",
        "corners_t1": 1,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-22",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "France",
        "team2": "Iraq",
        "corners_t1": 4,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-23",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Norway",
        "team2": "Senegal",
        "corners_t1": 5,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-23",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Jordan",
        "team2": "Algeria",
        "corners_t1": 1,
        "corners_t2": 10
    })
    matches.append({
        "date": "2026-06-23",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Portugal",
        "team2": "Uzbekistan",
        "corners_t1": 3,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-23",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "England",
        "team2": "Ghana",
        "corners_t1": 9,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-24",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Panama",
        "team2": "Croatia",
        "corners_t1": 7,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-24",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Colombia",
        "team2": "D.R. Congo",
        "corners_t1": 5,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-24",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Bosnia & Herzegovina",
        "team2": "Qatar",
        "corners_t1": 5,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-24",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Switzerland",
        "team2": "Canada",
        "corners_t1": 2,
        "corners_t2": 7
    })
    matches.append({
        "date": "2026-06-24",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Morocco",
        "team2": "Haiti",
        "corners_t1": 9,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-24",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Scotland",
        "team2": "Brazil",
        "corners_t1": 7,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-25",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Czech Republic",
        "team2": "Mexico",
        "corners_t1": 5,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-25",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "South Africa",
        "team2": "South Korea",
        "corners_t1": 4,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-25",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Curacao",
        "team2": "Ivory Coast",
        "corners_t1": 4,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-25",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Ecuador",
        "team2": "Germany",
        "corners_t1": 3,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-26",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Japan",
        "team2": "Sweden",
        "corners_t1": 2,
        "corners_t2": 8
    })
    matches.append({
        "date": "2026-06-26",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Tunisia",
        "team2": "Netherlands",
        "corners_t1": 4,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-26",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Paraguay",
        "team2": "Australia",
        "corners_t1": 1,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-26",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Turkey",
        "team2": "USA",
        "corners_t1": 2,
        "corners_t2": 9
    })
    matches.append({
        "date": "2026-06-26",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Norway",
        "team2": "France",
        "corners_t1": 4,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-06-26",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Senegal",
        "team2": "Iraq",
        "corners_t1": 12,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-27",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Cape Verde",
        "team2": "Saudi Arabia",
        "corners_t1": 4,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-27",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Uruguay",
        "team2": "Spain",
        "corners_t1": 1,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-27",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Egypt",
        "team2": "Iran",
        "corners_t1": 8,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-27",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "New Zealand",
        "team2": "Belgium",
        "corners_t1": 5,
        "corners_t2": 8
    })
    matches.append({
        "date": "2026-06-27",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Croatia",
        "team2": "Ghana",
        "corners_t1": 3,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-27",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Panama",
        "team2": "England",
        "corners_t1": 3,
        "corners_t2": 7
    })
    matches.append({
        "date": "2026-06-28",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Colombia",
        "team2": "Portugal",
        "corners_t1": 5,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-28",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "D.R. Congo",
        "team2": "Uzbekistan",
        "corners_t1": 2,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-28",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Algeria",
        "team2": "Austria",
        "corners_t1": 0,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-28",
        "stage": "Group",
        "round": "Group Stage",
        "team1": "Jordan",
        "team2": "Argentina",
        "corners_t1": 2,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-28",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "South Africa",
        "team2": "Canada",
        "corners_t1": 1,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-06-29",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Brazil",
        "team2": "Japan",
        "corners_t1": 6,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-06-29",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Germany",
        "team2": "Paraguay",
        "corners_t1": 16,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-06-29",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Netherlands",
        "team2": "Morocco",
        "corners_t1": 5,
        "corners_t2": 8
    })
    matches.append({
        "date": "2026-06-30",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Ivory Coast",
        "team2": "Norway",
        "corners_t1": 14,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-06-30",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "France",
        "team2": "Sweden",
        "corners_t1": 9,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-06-30",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Mexico",
        "team2": "Ecuador",
        "corners_t1": 3,
        "corners_t2": 8
    })
    matches.append({
        "date": "2026-07-01",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "England",
        "team2": "D.R. Congo",
        "corners_t1": 5,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-07-01",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Belgium",
        "team2": "Senegal",
        "corners_t1": 4,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-07-01",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "USA",
        "team2": "Bosnia & Herzegovina",
        "corners_t1": 4,
        "corners_t2": 3
    })
    matches.append({
        "date": "2026-07-02",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Spain",
        "team2": "Austria",
        "corners_t1": 9,
        "corners_t2": 0
    })
    matches.append({
        "date": "2026-07-02",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Portugal",
        "team2": "Croatia",
        "corners_t1": 9,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-07-02",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Switzerland",
        "team2": "Algeria",
        "corners_t1": 4,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-07-03",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Australia",
        "team2": "Egypt",
        "corners_t1": 4,
        "corners_t2": 7
    })
    matches.append({
        "date": "2026-07-03",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Argentina",
        "team2": "Cape Verde",
        "corners_t1": 8,
        "corners_t2": 8
    })
    matches.append({
        "date": "2026-07-03",
        "stage": "Knockout",
        "round": "Round of 32",
        "team1": "Colombia",
        "team2": "Ghana",
        "corners_t1": 3,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-07-04",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Canada",
        "team2": "Morocco",
        "corners_t1": 11,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-07-04",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Paraguay",
        "team2": "France",
        "corners_t1": 2,
        "corners_t2": 12
    })
    matches.append({
        "date": "2026-07-05",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Brazil",
        "team2": "Norway",
        "corners_t1": 5,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-07-05",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Mexico",
        "team2": "England",
        "corners_t1": 12,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-07-06",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Portugal",
        "team2": "Spain",
        "corners_t1": 3,
        "corners_t2": 7
    })
    matches.append({
        "date": "2026-07-06",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "USA",
        "team2": "Belgium",
        "corners_t1": 3,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-07-07",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Argentina",
        "team2": "Egypt",
        "corners_t1": 6,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-07-07",
        "stage": "Knockout",
        "round": "Round of 16",
        "team1": "Switzerland",
        "team2": "Colombia",
        "corners_t1": 3,
        "corners_t2": 7
    })
    matches.append({
        "date": "2026-07-09",
        "stage": "Knockout",
        "round": "Quarter Finals",
        "team1": "France",
        "team2": "Morocco",
        "corners_t1": 5,
        "corners_t2": 5
    })
    matches.append({
        "date": "2026-07-10",
        "stage": "Knockout",
        "round": "Quarter Finals",
        "team1": "Spain",
        "team2": "Belgium",
        "corners_t1": 5,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-07-11",
        "stage": "Knockout",
        "round": "Quarter Finals",
        "team1": "Norway",
        "team2": "England",
        "corners_t1": 7,
        "corners_t2": 4
    })
    matches.append({
        "date": "2026-07-11",
        "stage": "Knockout",
        "round": "Quarter Finals",
        "team1": "Argentina",
        "team2": "Switzerland",
        "corners_t1": 8,
        "corners_t2": 2
    })
    matches.append({
        "date": "2026-07-14",
        "stage": "Knockout",
        "round": "Semi Finals",
        "team1": "France",
        "team2": "Spain",
        "corners_t1": 7,
        "corners_t2": 1
    })
    matches.append({
        "date": "2026-07-15",
        "stage": "Knockout",
        "round": "Semi Finals",
        "team1": "England",
        "team2": "Argentina",
        "corners_t1": 1,
        "corners_t2": 6
    })
    matches.append({
        "date": "2026-07-19",
        "stage": "Knockout",
        "round": "Final",
        "team1": "Spain",
        "team2": "Argentina",
        "corners_t1": 9,
        "corners_t2": 4
    })

    return pd.DataFrame(matches)



# DATA WRANGLING
def load_and_wrangle_data():
    """Extracts raw match data, saves it to CSV (if not already saved), 
    reshapes it into long format (one row per team per match), and saves
    that too. Returns (df_long, original_rows, original_columns) so
    callers can report on the raw data's shape as well."""

    df_matches = extract_raw_matches()
    original_rows = df_matches.shape[0]
    original_columns = list(df_matches.columns)

    if not RAW_PATH.exists():
        df_matches.to_csv(RAW_PATH, index=False)

    df_team1 = df_matches[["date", "stage", "round", "team1", "corners_t1"]].rename(
        columns={"team1": "team", "corners_t1": "corners"}
    )
    df_team2 = df_matches[["date", "stage", "round", "team2", "corners_t2"]].rename(
        columns={"team2": "team", "corners_t2": "corners"}
    )
    df_long = pd.concat([df_team1, df_team2], ignore_index=True)

    if not PROCESSED_PATH.exists():
        df_long.to_csv(PROCESSED_PATH, index=False)

    return df_long, original_rows, original_columns


# DATA SAMPLING
def generate_samples():
    """Loads the processed long-format data, separates it by stage, draws
    a fixed random sample from each, and saves the samples to CSV (only if
    they don't already exist). Returns the full populations and the samples."""

    df_long = pd.read_csv(PROCESSED_PATH)

    group_corners = df_long[df_long["stage"] == "Group"]["corners"]
    knockout_corners = df_long[df_long["stage"] == "Knockout"]["corners"]

    group_sample = group_corners.sample(n=SAMPLE_SIZE_GROUP, random_state=RANDOM_STATE)
    knockout_sample = knockout_corners.sample(n=SAMPLE_SIZE_KNOCKOUT, random_state=RANDOM_STATE)

    if not GROUP_SAMPLE_PATH.exists() and not KNOCKOUT_SAMPLE_PATH.exists():
        group_sample.to_csv(GROUP_SAMPLE_PATH, index=False, header=["corners"])
        knockout_sample.to_csv(KNOCKOUT_SAMPLE_PATH, index=False, header=["corners"])

    return group_corners, knockout_corners, group_sample, knockout_sample


def load_samples():
    """Loads the two saved sample CSVs. Used by every script downstream of
    sampling (descriptive stats, confidence interval, t-test), so they all
    read from the exact same fixed samples rather than resampling."""

    group_corners = pd.read_csv(GROUP_SAMPLE_PATH)["corners"]
    knockout_corners = pd.read_csv(KNOCKOUT_SAMPLE_PATH)["corners"]
    return group_corners, knockout_corners



# DESCRIPTIVE STATISTICS
def describe(sample, label):
    """Returns a formatted block of descriptive statistics (mean, median,
    mode, range, variance, standard deviation, IQR) for one sample."""

    sample = list(sample)
    sample_arr = np.array(sample)

    x_bar = stats_mod.mean(sample)
    median = stats_mod.median(sample)
    mode = stats_mod.mode(sample)
    the_range = np.max(sample) - np.min(sample)
    s_square = sample_arr.var(ddof=1)
    sigma_square = sample_arr.var()
    s = sample_arr.std(ddof=1)
    sigma = sample_arr.std()
    pct25 = np.percentile(sample, 25)
    pct75 = np.percentile(sample, 75)
    iqr = pct75 - pct25

    return f"""
{label}
Mean: {x_bar}
Median: {median:.2f}
Mode value: {mode}
Range: {the_range}
Sample variance: {s_square:.2f}. Population variance: {sigma_square:.2f}.
Sample std. dev.: {s:.2f}. Population std. dev.: {sigma:.2f}.
IQR: {iqr:.0f}. 25th percentile: {pct25:.0f}. 75th percentile: {pct75:.0f}
"""



# CONFIDENCE INTERVAL
def confidence_interval(data, label, confidence=0.95):
    """Returns a formatted block reporting the mean, standard deviation,
    and z-based confidence interval for one sample."""

    x_bar = data.mean()
    s = data.std(ddof=1)
    n = len(data)

    alpha = 1 - confidence
    z_score = st.norm.ppf(q=1 - alpha / 2)
    std_err = s / math.sqrt(n)
    mrg_err = z_score * std_err
    ci_low = x_bar - mrg_err
    ci_upp = x_bar + mrg_err

    return f"""
{label}
Mean: {x_bar:.2f}. Standard deviation: {s:.2f}. Size: {n}.
Z-statistic: {z_score:.2f}
Standard error: {std_err:.2f}
Margin of error: {mrg_err:.2f}
Confidence Interval of the mean: {ci_low:.2f} to {ci_upp:.2f}
"""


# HYPOTHESIS TESTING
def plot_histograms(group_corners, knockout_corners, save_path=None):
    """Plots side-by-side histograms of Group Stage and Knockout Stage
    corners (visual normality check). If save_path is given, saves the
    figure as a PNG there (only if it doesn't already exist)."""

    fig = plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.hist(group_corners, bins=10, edgecolor='black')
    plt.title("Group Stage Corners")
    plt.xlabel("Corners")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.hist(knockout_corners, bins=10, edgecolor='black')
    plt.title("Knockout Stage Corners")
    plt.xlabel("Corners")
    plt.ylabel("Frequency")

    plt.tight_layout()

    if save_path is not None and not Path(save_path).exists():
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()


def two_sample_ttest(group_corners, knockout_corners, alpha=0.05):
    """Runs Welch's two-sample t-test (unequal variance assumed) comparing
    Group Stage vs. Knockout Stage corners, using summary statistics.
    Returns a dict with every value needed for reporting."""

    x_bar1, s1, n1 = group_corners.mean(), group_corners.std(ddof=1), len(group_corners)
    x_bar2, s2, n2 = knockout_corners.mean(), knockout_corners.std(ddof=1), len(knockout_corners)

    t_stats, p_val = st.ttest_ind_from_stats(
        x_bar1, s1, n1, x_bar2, s2, n2,
        equal_var=False, alternative='two-sided'
    )

    conclusion = "We reject the null hypothesis." if p_val < alpha else "We accept the null hypothesis."

    return {
        "x_bar1": x_bar1, "s1": s1, "n1": n1,
        "x_bar2": x_bar2, "s2": s2, "n2": n2,
        "t_stats": t_stats, "p_val": p_val,
        "alpha": alpha, "conclusion": conclusion,
    }