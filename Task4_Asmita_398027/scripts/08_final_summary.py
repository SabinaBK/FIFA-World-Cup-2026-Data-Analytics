from scipy import stats

# Import required variables, functions, and output folder
from common import (
    QUESTION,
    ALPHA,
    RANDOM_SEED,
    get_test_variables,
    mean_confidence_interval,
    OUTPUT_FOLDER
)


# Set the output file path
output_file = (
    OUTPUT_FOLDER /
    "08_final_summary_output.txt"
)


# Get sample data for both groups
sample, progressed, eliminated = (
    get_test_variables()
)


# Calculate descriptive statistics
progressed_mean = (
    progressed.mean()
)

eliminated_mean = (
    eliminated.mean()
)

progressed_sd = (
    progressed.std(ddof=1)
)

eliminated_sd = (
    eliminated.std(ddof=1)
)

progressed_median = (
    progressed.median()
)

eliminated_median = (
    eliminated.median()
)


# Calculate 95% confidence intervals
progressed_ci = (
    mean_confidence_interval(
        progressed
    )
)

eliminated_ci = (
    mean_confidence_interval(
        eliminated
    )
)


# Perform Welch's independent two-sample t-test
t_statistic, p_value = (
    stats.ttest_ind(
        progressed,
        eliminated,
        equal_var=False
    )
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


# Prepare the final analysis summary
output = f"""
{'=' * 80}
8. FINAL CONCLUSION OF ANALYSIS OF FIFA WORLD CUP 2026 FORWARDS SHOTS ON TARGET PER 90 MINUTES
{'=' * 80}

ANALYTIC QUESTION

{QUESTION}


DATA PREPARATION AND SAMPLING

The population consisted of all forwards who appeared in at least one
FIFA World Cup 2026 match and had a valid SoT/90 value.

Players whose FBref position contained 'FW' were retained, while
players with zero playing time were excluded.

Teams appearing in the Round of 32 were classified as Progressed,
and the remaining group-stage teams were classified as Eliminated.

Stratified random sampling with random seed {RANDOM_SEED} was used.

Progressed-team sample:
n = {len(progressed)}

Eliminated-team sample:
n = {len(eliminated)}

Total sample:
n = {len(sample)}

Both comparison groups therefore contain at least 30 observations.


DESCRIPTIVE STATISTICS

Progressed-team forwards:
Mean SoT/90 = {progressed_mean:.3f}
SD = {progressed_sd:.3f}
Median = {progressed_median:.3f}

Eliminated-team forwards:
Mean SoT/90 = {eliminated_mean:.3f}
SD = {eliminated_sd:.3f}
Median = {eliminated_median:.3f}


95% CONFIDENCE INTERVALS

Progressed-team forwards:
[{progressed_ci['lower']:.3f}, {progressed_ci['upper']:.3f}]

Eliminated-team forwards:
[{eliminated_ci['lower']:.3f}, {eliminated_ci['upper']:.3f}]


TWO-SAMPLE T-TEST

Test:
Welch's independent two-sample t-test

t-statistic:
{t_statistic:.4f}

p-value:
{p_value:.4f}

Significance level:
alpha = {ALPHA}


DECISION

{decision}


CONCLUSION

{conclusion}


{'=' * 80}
END OF ANALYSIS
{'=' * 80}
"""


# Save the final summary to a text file
output_file.write_text(
    output,
    encoding="utf-8"
)


# Display the final summary and saved file location
print(output)

print(
    "\nFinal summary automatically saved to:"
)

print(output_file)