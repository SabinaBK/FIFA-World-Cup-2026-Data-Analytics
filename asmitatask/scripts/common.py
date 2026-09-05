from pathlib import Path

import pandas as pd
import numpy as np
from scipy import stats


# Set project and output paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_FOLDER = PROJECT_ROOT / "outputs"

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# Set CSV file location
CSV_FILE = (
    PROJECT_ROOT /
    "rawdata" /
    "fifa_world_cup_2026_player_shooting.csv"
)


# Define research settings
QUESTION = (
    "Is the average number of shots on target per 90 minutes different "
    "between forwards from progressed teams and forwards from eliminated "
    "teams in the FIFA World Cup 2026?"
)

ALPHA = 0.05

RANDOM_SEED = 140

N_PER_GROUP = 30


# List teams that progressed to the Round of 32
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


# Load and wrangle the dataset
def load_and_wrangle_data():

    # Check whether the CSV file exists
    if not CSV_FILE.exists():

        raise FileNotFoundError(
            f"CSV file not found:\n{CSV_FILE}\n\n"
            "Place fifa_world_cup_2026_player_shooting.csv "
            "inside the rawdata folder."
        )

    # Read the CSV file
    df = pd.read_csv(
        CSV_FILE
    )

    # Store original dataset information
    original_columns = list(
        df.columns
    )

    original_rows = len(df)

    # Keep variables required for the analysis
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

    # Remove country codes from squad names
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


# Prepare the forward population
def prepare_forwards():

    df, _, _ = load_and_wrangle_data()

    # Keep players whose position contains FW
    forwards = df[
        df["Pos"]
        .astype(str)
        .str.contains(
            "FW",
            na=False
        )
    ].copy()

    # Remove zero playing time and missing SoT/90 values
    forwards = forwards[
        forwards["90s"] > 0
    ].copy()

    forwards = forwards.dropna(
        subset=["SoT/90"]
    ).copy()

    # Classify forwards as progressed or eliminated
    forwards["Team_Status"] = np.where(

        forwards["Team"].isin(
            PROGRESSED_TEAMS
        ),

        "Progressed",

        "Eliminated"
    )

    return forwards


# Create stratified random samples
def create_sample():

    forwards = prepare_forwards()

    # Separate the two populations
    progressed_population = forwards[
        forwards["Team_Status"]
        == "Progressed"
    ].copy()

    eliminated_population = forwards[
        forwards["Team_Status"]
        == "Eliminated"
    ].copy()

    # Check that both groups have enough observations
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

    # Randomly select 30 observations from each group
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


# Get SoT/90 values for statistical testing
def get_test_variables():

    (
        _,
        _,
        _,
        progressed_sample,
        eliminated_sample,
        sample
    ) = create_sample()

    progressed = progressed_sample[
        "SoT/90"
    ].astype(float)

    eliminated = eliminated_sample[
        "SoT/90"
    ].astype(float)

    return (
        sample,
        progressed,
        eliminated
    )


# Calculate the confidence interval for a sample mean
def mean_confidence_interval(
    values,
    confidence=0.95
):

    # Clean and convert the values
    values = (
        pd.Series(values)
        .dropna()
        .astype(float)
    )

    # Calculate confidence interval components
    n = len(values)

    mean = values.mean()

    standard_deviation = (
        values.std(ddof=1)
    )

    standard_error = (
        standard_deviation
        / np.sqrt(n)
    )

    critical_t = stats.t.ppf(
        (1 + confidence) / 2,
        df=n - 1
    )

    margin_of_error = (
        critical_t
        * standard_error
    )

    # Return confidence interval results
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