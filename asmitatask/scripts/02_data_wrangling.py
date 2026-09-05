# Import data wrangling function and output folder
from common import (
    load_and_wrangle_data,
    OUTPUT_FOLDER
)

# Set the output file path
output_file = (
    OUTPUT_FOLDER /
    "02_data_wrangling_output.txt"
)

# Load and wrangle the dataset
df, original_rows, original_columns = (
    load_and_wrangle_data()
)

# Select variables required for the analysis
selected_variables = [
    "Player",
    "Pos",
    "Team",
    "90s",
    "Sh",
    "SoT",
    "SoT/90"
]

# Prepare the data wrangling results
output = f"""
{'=' * 80}
2. DATA WRANGLING
{'=' * 80}

Raw player records loaded:
{original_rows}

Original columns:
{original_columns}

Selected variables after wrangling:
{selected_variables}

First 10 records after wrangling:
{df[selected_variables].head(10).to_string(index=False)}

Data wrangling completed successfully.
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