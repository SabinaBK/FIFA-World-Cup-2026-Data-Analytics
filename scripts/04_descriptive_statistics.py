from common import (
    get_test_variables,
    OUTPUT_FOLDER
)


output_file = (
    OUTPUT_FOLDER /
    "04_descriptive_statistics_output.txt"
)


sample, progressed, eliminated = (
    get_test_variables()
)


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


output_file.write_text(
    output,
    encoding="utf-8"
)


print(output)

print(
    "\nOutput automatically saved to:"
)

print(output_file)