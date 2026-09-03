from pathlib import Path

import pandas as pd
import numpy as np
from scipy import stats


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_FOLDER = PROJECT_ROOT / "outputs"

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# CSV file location
CSV_FILE = (
    PROJECT_ROOT /
    "rawdata" /
    "fifa_world_cup_2026_player_shooting.csv"
)

# ============================================================
# RESEARCH SETTINGS
# ============================================================

QUESTION = (
    "Is the average number of shots on target per 90 minutes different "
    "between forwards from progressed teams and forwards from eliminated "
    "teams in the FIFA World Cup 2026?"
)

ALPHA = 0.05

RANDOM_SEED = 140

N_PER_GROUP = 30


# ============================================================
# PROGRESSED TEAMS
# ============================================================

PROGRESSED_TEAMS = {

    "Canada",
    "South Africa",
    "Brazil",
    "Japan",
    "Paraguay",
    "Germany",
    "Morocco",
    "Netherlands",
    "Norway",
    "Côte d'Ivoire",
    "France",
    "Sweden",
    "Mexico",
    "Ecuador",
    "England",
    "Congo DR",
    "Belgium",
    "Senegal",
    "USA",
    "Bosnia–Herz",
    "Spain",
    "Austria",
    "Portugal",
    "Croatia",
    "Switzerland",
    "Algeria",
    "Egypt",
    "Australia",
    "Argentina",
    "Cabo Verde",
    "Colombia",
    "Ghana"
}


# ============================================================
# LOAD AND WRANGLE DATA
# ============================================================

def load_and_wrangle_data():

    # Check whether CSV file exists
    if not CSV_FILE.exists():

        raise FileNotFoundError(
            f"CSV file not found:\n{CSV_FILE}\n\n"
            "Place fifa_world_cup_2026_player_shooting.csv "
            "inside the main FIFA_2026_Analysis folder."
        )

    # Read data directly from CSV file
    df = pd.read_csv(
        CSV_FILE
    )

    # Store original information before wrangling
    original_columns = list(
        df.columns
    )

    original_rows = len(df)

    # Keep only variables required for analysis
    df = df[
        [
            "Player",
            "Pos",
            "Squad",
            "Age",
            "90s",
            "Sh",
            "SoT",
            "SoT/90"
        ]
    ].copy()

    # Remove country code from squad
    # Example:
    # "us USA" becomes "USA"
    # "br Brazil" becomes "Brazil"
    df["Team"] = (
        df["Squad"]
        .astype(str)
        .str.replace(
            r"^[a-z]{2,3}\s+",
            "",
            regex=True
        )
        .str.strip()
    )

    # Convert required variables to numeric
    numeric_columns = [
        "90s",
        "Sh",
        "SoT",
        "SoT/90"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return (
        df,
        original_rows,
        original_columns
    )


# ============================================================
# PREPARE FORWARD POPULATION
# ============================================================

def prepare_forwards():

    df, _, _ = load_and_wrangle_data()

    # Keep players whose position contains FW
    #
    # Examples retained:
    # FW
    # FWMF
    # MFFW
    # DFFW
    forwards = df[
        df["Pos"]
        .astype(str)
        .str.contains(
            "FW",
            na=False
        )
    ].copy()

    # Remove players with zero playing time
    forwards = forwards[
        forwards["90s"] > 0
    ].copy()

    # Remove players with missing SoT/90
    forwards = forwards.dropna(
        subset=["SoT/90"]
    ).copy()

    # Classify players according to team progression
    forwards["Team_Status"] = np.where(

        forwards["Team"].isin(
            PROGRESSED_TEAMS
        ),

        "Progressed",

        "Eliminated"
    )

    return forwards


# ============================================================
# CREATE STRATIFIED SAMPLE
# ============================================================

def create_sample():

    forwards = prepare_forwards()

    # Separate progressed-team forwards
    progressed_population = forwards[
        forwards["Team_Status"]
        == "Progressed"
    ].copy()

    # Separate eliminated-team forwards
    eliminated_population = forwards[
        forwards["Team_Status"]
        == "Eliminated"
    ].copy()


    # --------------------------------------------------------
    # CHECK POPULATION SIZE
    # --------------------------------------------------------

    if len(progressed_population) < N_PER_GROUP:

        raise ValueError(
            "ERROR: Progressed group has fewer than "
            f"{N_PER_GROUP} eligible observations."
        )


    if len(eliminated_population) < N_PER_GROUP:

        raise ValueError(
            "ERROR: Eliminated group has fewer than "
            f"{N_PER_GROUP} eligible observations."
        )


    # --------------------------------------------------------
    # STRATIFIED RANDOM SAMPLING
    # --------------------------------------------------------
    #
    # Randomly select 30 forwards from progressed teams
    # and 30 forwards from eliminated teams.
    #
    # random_state ensures reproducibility.
    # --------------------------------------------------------

    progressed_sample = (
        progressed_population
        .sample(
            n=N_PER_GROUP,
            random_state=RANDOM_SEED
        )
    )


    eliminated_sample = (
        eliminated_population
        .sample(
            n=N_PER_GROUP,
            random_state=RANDOM_SEED
        )
    )


    # Combine both samples
    sample = pd.concat(
        [
            progressed_sample,
            eliminated_sample
        ],
        ignore_index=True
    )


    return (
        forwards,
        progressed_population,
        eliminated_population,
        progressed_sample,
        eliminated_sample,
        sample
    )


# ============================================================
# GET TWO TEST VARIABLES
# ============================================================

def get_test_variables():

    (
        _,
        _,
        _,
        progressed_sample,
        eliminated_sample,
        sample
    ) = create_sample()


    # SoT/90 values for progressed-team forwards
    progressed = progressed_sample[
        "SoT/90"
    ].astype(float)


    # SoT/90 values for eliminated-team forwards
    eliminated = eliminated_sample[
        "SoT/90"
    ].astype(float)


    return (
        sample,
        progressed,
        eliminated
    )


# ============================================================
# CONFIDENCE INTERVAL FUNCTION
# ============================================================

def mean_confidence_interval(
    values,
    confidence=0.95
):

    # Convert values to clean numeric Series
    values = (
        pd.Series(values)
        .dropna()
        .astype(float)
    )

    # Sample size
    n = len(values)

    # Sample mean
    mean = values.mean()

    # Sample standard deviation
    standard_deviation = (
        values.std(ddof=1)
    )

    # Standard error
    standard_error = (
        standard_deviation
        / np.sqrt(n)
    )

    # Critical t-value
    critical_t = stats.t.ppf(

        (1 + confidence) / 2,

        df=n - 1
    )

    # Margin of error
    margin_of_error = (
        critical_t
        * standard_error
    )


    # Return confidence interval information
    return {

        "n":
            n,

        "mean":
            mean,

        "standard_deviation":
            standard_deviation,

        "standard_error":
            standard_error,

        "lower":
            mean - margin_of_error,

        "upper":
            mean + margin_of_error
    }