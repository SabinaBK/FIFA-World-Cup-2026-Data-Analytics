from scipy import stats

# Import required variables and output folder
from common import (
    get_test_variables,
    ALPHA,
    OUTPUT_FOLDER
)


# Set the output file path
output_file = (
    OUTPUT_FOLDER /
    "06_t_test_output.txt"
)


# Get test variables for both groups
sample, progressed, eliminated = (
    get_test_variables()
)


# Check that both groups have at least 30 observations
if len(progressed) < 30:
    raise ValueError(
        "Progressed sample has fewer than 30 observations."
    )


if len(eliminated) < 30:
    raise ValueError(
        "Eliminated sample has fewer than 30 observations."
    )


# Perform Welch's independent two-sample t-test
t_statistic, p_value = (
    stats.ttest_ind(
        progressed,
        eliminated,
        equal_var=False
    )
)


# Calculate group means and mean difference
progressed_mean = (
    progressed.mean()
)

eliminated_mean = (
    eliminated.mean()
)

mean_difference = (
    progressed_mean
    -
    eliminated_mean
)


# Make the hypothesis test decision
if p_value < ALPHA:

    decision = "Reject H0"

    conclusion = (
        "At the 5% significance level, there is statistically "
        "significant evidence that the average number of shots "
        "on target per 90 minutes differs between forwards from "
        "progressed teams and forwards from eliminated teams "
        "in the FIFA World Cup 2026."
    )

else:

    decision = "Fail to reject H0"

    conclusion = (
        "At the 5% significance level, there is insufficient "
        "statistical evidence to conclude that the average "
        "number of shots on target per 90 minutes differs "
        "between forwards from progressed teams and forwards "
        "from eliminated teams in the FIFA World Cup 2026."
    )


# Prepare the t-test results
output = f"""
{'=' * 80}
6. INFERENTIAL STATISTICS - TWO-SAMPLE T-TEST
{'=' * 80}

Test:
Welch's Independent Two-Sample T-Test

Why Welch's t-test?
- The two groups contain different players.
- SoT/90 is a numerical variable.
- Equal population variances do not need to be assumed.

SAMPLE SIZE CHECK
{'-' * 40}

Progressed sample:
n = {len(progressed)}

Eliminated sample:
n = {len(eliminated)}

Progressed n >= 30:
PASS

Eliminated n >= 30:
PASS


TEST RESULTS
{'-' * 40}

Progressed mean SoT/90:
{progressed_mean:.3f}

Eliminated mean SoT/90:
{eliminated_mean:.3f}

Mean difference:
{mean_difference:.3f}

t-statistic:
{t_statistic:.4f}

p-value:
{p_value:.4f}

Alpha:
{ALPHA}


HYPOTHESIS DECISION
{'-' * 40}

{decision}


STATISTICAL CONCLUSION
{'-' * 40}

{conclusion}
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