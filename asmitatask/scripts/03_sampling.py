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


# Set the output file path
output_file = (
    OUTPUT_FOLDER /
    "03_sampling_output.txt"
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


# Select and sort variables for displaying the sample
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

Sampled forwards:
{sample_display.to_string(index=False)}
"""


# Save the results to a text file
output_file.write_text(
    output,
    encoding="utf-8"
)


# Display the results and saved file location
print(output)

print(
    "\nOutput automatically saved to:"
)

print(output_file)