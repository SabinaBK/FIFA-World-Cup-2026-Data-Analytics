# Import required variables from common.py
from common import (
    QUESTION,
    ALPHA,
    OUTPUT_FOLDER
)

# Set the output file path
output_file = (
    OUTPUT_FOLDER /
    "01_question_output.txt"
)

# Define the research question, population, groups, and hypotheses
output = f"""
{'=' * 80}
1. ANALYTIC QUESTION FORMULATION
{'=' * 80}

Research Question:
{QUESTION}

Population:
All forwards who appeared in at least one FIFA World Cup 2026 match
and have a valid shots-on-target-per-90 value.

Groups:
Group 1: Forwards from teams that progressed to the Round of 32.
Group 2: Forwards from teams eliminated during the group stage.

Hypotheses:
H0: mean SoT/90 (Progressed) = mean SoT/90 (Eliminated)
H1: mean SoT/90 (Progressed) != mean SoT/90 (Eliminated)

Significance level:
alpha = {ALPHA}
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