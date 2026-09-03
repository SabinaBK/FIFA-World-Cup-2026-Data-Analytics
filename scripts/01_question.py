from common import (
    QUESTION,
    ALPHA,
    OUTPUT_FOLDER
)


output_file = (
    OUTPUT_FOLDER /
    "01_question_output.txt"
)


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


output_file.write_text(
    output,
    encoding="utf-8"
)


print(output)

print(
    "\nOutput automatically saved to:"
)

print(output_file)