import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

CLEAN_DIR = DATA_DIR / "cleaned data"
SAMPLE_DIR = DATA_DIR / "sampling data"
# Create output folder automatically if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

df = pd.read_csv(  CLEAN_DIR / "fifa_passing_cleaned.csv")

print("Total cleaned players:", len(df))


# ==========================================
# 2. CREATE TWO GROUPS
# ==========================================

group_90_plus = df[
    df["Passing Accuracy (%)"] >= 90
]

group_below_90 = df[
    df["Passing Accuracy (%)"] < 90
]

print("\nPopulation group sizes:")
print("Passing accuracy >= 90%:", len(group_90_plus))
print("Passing accuracy < 90%:", len(group_below_90))


# ==========================================
# 3. RANDOM SAMPLING
# ==========================================

# Randomly select 40 players from each group

sample_90_plus = group_90_plus.sample(
    n=40,
    random_state=42
)

sample_below_90 = group_below_90.sample(
    n=40,
    random_state=42
)


# ==========================================
# 4. ADD GROUP LABEL
# ==========================================

sample_90_plus = sample_90_plus.copy()
sample_below_90 = sample_below_90.copy()

sample_90_plus["Accuracy_Group"] = "90% or greater"
sample_below_90["Accuracy_Group"] = "Below 90%"


# ==========================================
# 5. COMBINE THE TWO SAMPLES
# ==========================================

sample_df = pd.concat(
    [sample_90_plus, sample_below_90],
    ignore_index=True
)

# Randomise row order
sample_df = sample_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Add Sample ID
sample_df.insert(
    0,
    "Sample_ID",
    range(1, len(sample_df) + 1)
)


# ==========================================
# 6. DISPLAY SAMPLE INFORMATION
# ==========================================

print("\n========== SAMPLE ==========")

print("Total sample size:", len(sample_df))

print("\nSample group sizes:")
print(sample_df["Accuracy_Group"].value_counts())

print("\nSample:")
print(sample_df.to_string(index=False))


# ==========================================
# 7. SAVE SAMPLE
# ==========================================

sample_df.to_csv(
    SAMPLE_DIR / "passing_two_sample_80.csv",
    index=False
)

sample_df.to_excel(
    SAMPLE_DIR / "passing_two_sample_80.xlsx",
    index=False
)

print("\nSample files saved successfully.")

# ==========================================
# 8. DESCRIPTIVE STATISTICS
# ==========================================

print("\n========== DESCRIPTIVE STATISTICS ==========")

# Separate Passes Completed for both groups
high_group = sample_90_plus["Passes Completed"]
low_group = sample_below_90["Passes Completed"]


# 90% OR GREATER GROUP
print("\n--- Passing Accuracy >= 90% ---")

print("Sample Size:", high_group.count())
print("Mean:", round(high_group.mean(), 2))
print("Median:", round(high_group.median(), 2))
print("Standard Deviation:", round(high_group.std(), 2))
print("Minimum:", high_group.min())
print("Maximum:", high_group.max())


# BELOW 90% GROUP
print("\n--- Passing Accuracy < 90% ---")

print("Sample Size:", low_group.count())
print("Mean:", round(low_group.mean(), 2))
print("Median:", round(low_group.median(), 2))
print("Standard Deviation:", round(low_group.std(), 2))
print("Minimum:", low_group.min())
print("Maximum:", low_group.max())


# ==========================================
# 9. MEAN DIFFERENCE
# ==========================================

mean_difference = high_group.mean() - low_group.mean()

print("\nMean Difference:", round(mean_difference, 2))

# ==========================================
# 11. TWO-SAMPLE T-TEST
# ==========================================

print("\n========== TWO-SAMPLE T-TEST ==========")

# Remove any missing values
high_group = sample_90_plus["Passes Completed"].dropna()
low_group = sample_below_90["Passes Completed"].dropna()

# Welch's independent two-sample t-test
t_statistic, p_value = stats.ttest_ind(
    high_group,
    low_group,
    equal_var=False
)

print(f"90% or Greater Sample Size: {len(high_group)}")
print(f"Below 90% Sample Size: {len(low_group)}")

print(f"\n90% or Greater Mean: {high_group.mean():.2f}")
print(f"Below 90% Mean: {low_group.mean():.2f}")

print(f"\nMean Difference: "
      f"{high_group.mean() - low_group.mean():.2f}")

print(f"T-statistic: {t_statistic:.4f}")
print(f"P-value: {p_value:.4f}")


# ==========================================
# 12. HYPOTHESIS DECISION
# ==========================================

alpha = 0.05

print(f"\nSignificance Level (alpha): {alpha}")

if p_value < alpha:
    print("Decision: Reject the null hypothesis.")
    print(
        "Conclusion: There is a statistically significant "
        "difference in the average number of completed passes "
        "between players with passing accuracy of 90% or greater "
        "and players with passing accuracy below 90%."
    )
else:
    print("Decision: Fail to reject the null hypothesis.")
    print(
        "Conclusion: There is insufficient evidence to conclude "
        "that there is a statistically significant difference "
        "in the average number of completed passes between "
        "players with passing accuracy of 90% or greater "
        "and players with passing accuracy below 90%."
    )
# ==========================================
# 95% CONFIDENCE INTERVALS
# ==========================================

import numpy as np
from scipy import stats

print("\n========== 95% CONFIDENCE INTERVALS ==========")

# Data from the two samples
high_group = sample_90_plus["Passes Completed"].dropna()
low_group = sample_below_90["Passes Completed"].dropna()


# Function to calculate 95% CI
def calculate_ci(data):

    n = len(data)
    mean = data.mean()
    std = data.std(ddof=1)

    # Standard error
    se = std / np.sqrt(n)

    # Critical t-value
    t_critical = stats.t.ppf(
        0.975,
        df=n - 1
    )

    # Margin of error
    margin_error = t_critical * se

    lower = mean - margin_error
    upper = mean + margin_error

    return mean, se, lower, upper


# ==========================================
# >= 90% GROUP
# ==========================================

mean_high, se_high, lower_high, upper_high = calculate_ci(
    high_group
)

print("\n--- Passing Accuracy >= 90% ---")
print(f"Sample Size: {len(high_group)}")
print(f"Mean: {mean_high:.2f}")
print(f"Standard Error: {se_high:.2f}")
print(
    f"95% Confidence Interval: "
    f"({lower_high:.2f}, {upper_high:.2f})"
)


# ==========================================
# < 90% GROUP
# ==========================================

mean_low, se_low, lower_low, upper_low = calculate_ci(
    low_group
)

print("\n--- Passing Accuracy < 90% ---")
print(f"Sample Size: {len(low_group)}")
print(f"Mean: {mean_low:.2f}")
print(f"Standard Error: {se_low:.2f}")
print(
    f"95% Confidence Interval: "
    f"({lower_low:.2f}, {upper_low:.2f})"
)

# ==========================================
# 95% CI FOR DIFFERENCE BETWEEN MEANS
# Welch method
# ==========================================

mean_difference = mean_high - mean_low

n1 = len(high_group)
n2 = len(low_group)

var1 = high_group.var(ddof=1)
var2 = low_group.var(ddof=1)

# Standard error of difference
se_difference = np.sqrt(
    (var1 / n1) + (var2 / n2)
)

# Welch-Satterthwaite degrees of freedom
df_welch = (
    ((var1 / n1) + (var2 / n2)) ** 2
    /
    (
        ((var1 / n1) ** 2 / (n1 - 1))
        +
        ((var2 / n2) ** 2 / (n2 - 1))
    )
)

# Critical t-value
t_critical = stats.t.ppf(
    0.975,
    df=df_welch
)

margin_error = t_critical * se_difference

lower_difference = mean_difference - margin_error
upper_difference = mean_difference + margin_error


print("\n--- Difference Between Group Means ---")

print(f"Mean Difference: {mean_difference:.2f}")

print(
    f"95% CI for Mean Difference: "
    f"({lower_difference:.2f}, "
    f"{upper_difference:.2f})"
)

# ==========================================
# SAVE COMPLETE ANALYSIS OUTPUT
# ==========================================

output_file = OUTPUT_DIR / "analysis_results.txt"

with open(output_file, "w") as file:

    file.write("FIFA WORLD CUP 2026 PASSING ANALYSIS\n")
    file.write("====================================\n\n")

    # --------------------------------------
    # Research Question
    # --------------------------------------

    file.write("RESEARCH QUESTION\n")
    file.write("-----------------\n")

    file.write(
        "Is the average number of completed passes significantly different "
        "between FIFA World Cup 2026 players with passing accuracy of 90% "
        "or greater and players with passing accuracy below 90%?\n\n"
    )

    # --------------------------------------
    # Population and Sampling
    # --------------------------------------

    file.write("POPULATION AND SAMPLING\n")
    file.write("-----------------------\n")

    file.write(
        f"Population - Passing Accuracy >= 90%: "
        f"{len(group_90_plus)} players\n"
    )

    file.write(
        f"Population - Passing Accuracy < 90%: "
        f"{len(group_below_90)} players\n"
    )

    file.write(
        f"Sample - Passing Accuracy >= 90%: "
        f"{len(high_group)} players\n"
    )

    file.write(
        f"Sample - Passing Accuracy < 90%: "
        f"{len(low_group)} players\n"
    )

    file.write(
        f"Total Sample Size: "
        f"{len(high_group) + len(low_group)} players\n\n"
    )

    # --------------------------------------
    # Descriptive Statistics
    # --------------------------------------

    file.write("DESCRIPTIVE STATISTICS\n")
    file.write("----------------------\n")

    file.write("Passing Accuracy >= 90%\n")
    file.write(f"Sample Size: {len(high_group)}\n")
    file.write(f"Mean: {high_group.mean():.2f}\n")
    file.write(f"Median: {high_group.median():.2f}\n")
    file.write(
        f"Standard Deviation: {high_group.std(ddof=1):.2f}\n"
    )
    file.write(f"Minimum: {high_group.min():.2f}\n")
    file.write(f"Maximum: {high_group.max():.2f}\n\n")

    file.write("Passing Accuracy < 90%\n")
    file.write(f"Sample Size: {len(low_group)}\n")
    file.write(f"Mean: {low_group.mean():.2f}\n")
    file.write(f"Median: {low_group.median():.2f}\n")
    file.write(
        f"Standard Deviation: {low_group.std(ddof=1):.2f}\n"
    )
    file.write(f"Minimum: {low_group.min():.2f}\n")
    file.write(f"Maximum: {low_group.max():.2f}\n\n")

    file.write(
        f"Mean Difference: {mean_difference:.2f}\n\n"
    )

    # --------------------------------------
    # Confidence Intervals
    # --------------------------------------

    file.write("95% CONFIDENCE INTERVALS\n")
    file.write("------------------------\n")

    file.write("Passing Accuracy >= 90%\n")
    file.write(
        f"95% CI: ({lower_high:.2f}, {upper_high:.2f})\n\n"
    )

    file.write("Passing Accuracy < 90%\n")
    file.write(
        f"95% CI: ({lower_low:.2f}, {upper_low:.2f})\n\n"
    )

    file.write("Difference Between Means\n")
    file.write(
        f"95% CI: ({lower_difference:.2f}, "
        f"{upper_difference:.2f})\n\n"
    )

    # --------------------------------------
    # Hypotheses
    # --------------------------------------

    file.write("HYPOTHESES\n")
    file.write("----------\n")

    file.write(
        "H0: The mean number of completed passes is the same "
        "for players with passing accuracy >= 90% and players "
        "with passing accuracy < 90%.\n"
    )

    file.write(
        "H1: The mean number of completed passes is different "
        "between players with passing accuracy >= 90% and players "
        "with passing accuracy < 90%.\n\n"
    )

    # --------------------------------------
    # Two-Sample T-Test
    # --------------------------------------

    file.write("WELCH TWO-SAMPLE T-TEST\n")
    file.write("-----------------------\n")

    file.write(f"T-statistic: {t_statistic:.4f}\n")
    file.write(f"P-value: {p_value:.6f}\n")
    file.write(f"Significance Level (alpha): {alpha}\n\n")

    # --------------------------------------
    # Decision and Conclusion
    # --------------------------------------

    file.write("DECISION\n")
    file.write("--------\n")

    if p_value < alpha:

        file.write(
            "Reject the null hypothesis (H0).\n\n"
        )

        file.write("CONCLUSION\n")
        file.write("----------\n")

        file.write(
            "There is statistically significant evidence that "
            "the average number of completed passes differs between "
            "FIFA World Cup 2026 players with passing accuracy of "
            "90% or greater and players with passing accuracy below 90%.\n"
        )

        file.write(
            f"The >=90% group completed an average of "
            f"{high_group.mean():.2f} passes, compared with "
            f"{low_group.mean():.2f} passes for the <90% group.\n"
        )

        file.write(
            f"The estimated mean difference was "
            f"{mean_difference:.2f} passes, with a 95% confidence "
            f"interval from {lower_difference:.2f} to "
            f"{upper_difference:.2f} passes.\n"
        )

    else:

        file.write(
            "Fail to reject the null hypothesis (H0).\n\n"
        )

        file.write("CONCLUSION\n")
        file.write("----------\n")

        file.write(
            "There is insufficient statistical evidence to conclude "
            "that the average number of completed passes differs "
            "between the two passing-accuracy groups.\n"
        )

print(f"\nComplete analysis saved to: {output_file}")

# ==========================================
# HISTOGRAMS
# ==========================================

import matplotlib.pyplot as plt

# Histogram: Passing Accuracy >= 90%
plt.figure(figsize=(8, 5))

plt.hist(
    high_group,
    bins=10,
    edgecolor="black"
)

plt.title("Completed Passes: Passing Accuracy >= 90%")
plt.xlabel("Passes Completed")
plt.ylabel("Number of Players")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "histogram_90_or_greater.png",
    dpi=300
)

plt.close()


# Histogram: Passing Accuracy < 90%
plt.figure(figsize=(8, 5))

plt.hist(
    low_group,
    bins=10,
    edgecolor="black"
)

plt.title("Completed Passes: Passing Accuracy < 90%")
plt.xlabel("Passes Completed")
plt.ylabel("Number of Players")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "histogram_below_90.png",
    dpi=300
)

plt.close()

print("Histograms saved successfully.")