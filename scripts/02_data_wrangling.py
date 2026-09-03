from common import (
    load_and_wrangle_data,
    OUTPUT_FOLDER
)


output_file = (
    OUTPUT_FOLDER /
    "02_data_wrangling_output.txt"
)


df, original_rows, original_columns = (
    load_and_wrangle_data()
)


selected_variables = [
    "Player",
    "Pos",
    "Team",
    "90s",
    "Sh",
    "SoT",
    "SoT/90"
]


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


output_file.write_text(
    output,
    encoding="utf-8"
)


print(output)

print(
    "\nOutput automatically saved to:"
)

print(output_file)