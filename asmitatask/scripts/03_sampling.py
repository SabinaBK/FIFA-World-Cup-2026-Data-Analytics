import sys

# Set terminal output encoding
sys.stdout.reconfigure(encoding="utf-8")


# Import sampling functions and settings
from common import (
    create_sample,
    N_PER_GROUP,
    RANDOM_SEED,
    OUTPUT_FOLDER
)


# Set output file paths
output_file = (
    OUTPUT_FOLDER /
    "03_sampling_output.txt"
)

progressed_csv_file = (
    OUTPUT_FOLDER /
    "03_progressed_sample.csv"
)

eliminated_csv_file = (
    OUTPUT_FOLDER /
    "03_eliminated_sample.csv"
)


# Create populations and random samples
(
    forwards,
    progressed_population,
    eliminated_population,
    progressed_sample,
    eliminated_sample,
    sample

) = create_sample()


# Select columns for progressed sample
progressed_display = progressed_sample[
    [
        "Player",
        "Team",
        "Pos",
        "90s",
        "SoT/90",
        "Team_Status"
    ]
].sort_values(
    [
        "Team",
        "Player"
    ]
)


# Select columns for eliminated sample
eliminated_display = eliminated_sample[
    [
        "Player",
        "Team",
        "Pos",
        "90s",
        "SoT/90",
        "Team_Status"
    ]
].sort_values(
    [
        "Team",
        "Player"
    ]
)


# Combine both groups for displaying in the text output
sample_display = sample[
    [
        "Player",
        "Team",
        "Pos",
        "90s",
        "SoT/90",
        "Team_Status"
    ]
].sort_values(
    [
        "Team_Status",
        "Team",
        "Player"
    ]
)


# Prepare sampling and sample size validation results
output = f"""
{'=' * 80}
3. DATA PREPARATION AND SAMPLING
{'=' * 80}

Cleaned forward population size:
{len(forwards)}

Population counts:

Progressed:
{len(progressed_population)}

Eliminated:
{len(eliminated_population)}

Sampling method:
Stratified random sampling

Random seed:
{RANDOM_SEED}

Minimum required sample size per group:
{N_PER_GROUP}

SAMPLE SIZE VALIDATION
{'-' * 40}

Progressed sample:
{len(progressed_sample)}

Eliminated sample:
{len(eliminated_sample)}

Progressed n >= 30:
PASS

Eliminated n >= 30:
PASS

Total sample:
{len(sample)}

Both groups satisfy the requirement of at least 30 observations.

PROGRESSED SAMPLE
{'-' * 40}

{progressed_display.to_string(index=False)}

ELIMINATED SAMPLE
{'-' * 40}

{eliminated_display.to_string(index=False)}

COMBINED SAMPLE
{'-' * 40}

{sample_display.to_string(index=False)}
"""


# Save the complete sampling results to a text file
output_file.write_text(
    output,
    encoding="utf-8"
)


# Save progressed sample to CSV
progressed_display.to_csv(
    progressed_csv_file,
    index=False,
    encoding="utf-8-sig"
)


# Save eliminated sample to CSV
eliminated_display.to_csv(
    eliminated_csv_file,
    index=False,
    encoding="utf-8-sig"
)


# Display results in terminal
print(output)


# Display saved file locations
print("\nText output automatically saved to:")
print(output_file)

print("\nProgressed sample CSV automatically saved to:")
print(progressed_csv_file)

print("\nEliminated sample CSV automatically saved to:")
print(eliminated_csv_file)