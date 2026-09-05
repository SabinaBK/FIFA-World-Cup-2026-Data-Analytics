# Import required function and output folder
from common import (
    get_test_variables,
    OUTPUT_FOLDER
)


# Set the output file path
output_file = (
    OUTPUT_FOLDER /
    "04_descriptive_statistics_output.txt"
)


# Get sample data for both groups
sample, progressed, eliminated = (
    get_test_variables()
)


# Calculate descriptive statistics for SoT/90 by team status
descriptive = (
    sample
    .groupby(
        "Team_Status"
    )["SoT/90"]
    .agg(
        n="count",
        mean="mean",
        median="median",
        standard_deviation="std",
        minimum="min",
        maximum="max"
    )
)


# Prepare the descriptive statistics results
output = f"""
{'=' * 80}
4. DESCRIPTIVE STATISTICS
{'=' * 80}

Variable:
Shots on Target per 90 Minutes (SoT/90)

Descriptive Statistics:
{descriptive.round(3).to_string()}

Sample Size Check:

Progressed:
n = {len(progressed)}

Eliminated:
n = {len(eliminated)}
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