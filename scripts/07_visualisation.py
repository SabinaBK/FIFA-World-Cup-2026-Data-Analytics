import matplotlib.pyplot as plt

from common import (
    get_test_variables,
    OUTPUT_FOLDER
)


txt_output = (
    OUTPUT_FOLDER /
    "07_visualisation_output.txt"
)


image_output = (
    OUTPUT_FOLDER /
    "07_sot90_boxplot.png"
)


sample, progressed, eliminated = (
    get_test_variables()
)


# ============================================================
# CREATE BOXPLOT
# ============================================================

plt.figure(
    figsize=(7, 5)
)


sample.boxplot(
    column="SoT/90",
    by="Team_Status"
)


plt.title(
    "Forward Shots on Target per 90 by Team Progression"
)


plt.suptitle("")


plt.xlabel(
    "Team Status"
)


plt.ylabel(
    "Shots on Target per 90 Minutes"
)


plt.tight_layout()


plt.savefig(
    image_output,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


output = f"""
{'=' * 80}
7. VISUALISATION
{'=' * 80}

Visualisation:
Boxplot

Variable:
Shots on Target per 90 Minutes (SoT/90)

Groups:
Progressed-team forwards
Eliminated-team forwards

Progressed sample size:
{len(progressed)}

Eliminated sample size:
{len(eliminated)}

The boxplot was created successfully.

Image saved as:
{image_output.name}
"""


txt_output.write_text(
    output,
    encoding="utf-8"
)


print(output)

print(
    "\nText output automatically saved to:"
)

print(txt_output)

print(
    "\nFigure automatically saved to:"
)

print(image_output)