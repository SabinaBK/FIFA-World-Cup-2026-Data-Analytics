"""
FIFA World Cup 2026 Statistical Analysis Script

Input:
    data/processed/team_match_fouls_prepared.csv

Outputs:
    outputs/fouls_descriptive_statistics.csv
    outputs/fouls_confidence_intervals.csv
    outputs/fouls_hypothesis_test_results.csv
    outputs/fouls_statistical_summary.txt
"""

import os

import pandas as pd
from scipy import stats


INPUT_PATH = os.path.join(
    "data",
    "processed",
    "team_match_fouls_prepared.csv",
)

OUTPUT_DIRECTORY = "outputs"


def confidence_interval(
    values: pd.Series,
    confidence_level: float = 0.95,
) -> tuple[float, float]:
    """Calculate a confidence interval for a sample mean."""

    sample_size = len(values)
    sample_mean = values.mean()
    standard_error = stats.sem(values)

    critical_value = stats.t.ppf(
        (1 + confidence_level) / 2,
        sample_size - 1,
    )

    margin_of_error = critical_value * standard_error

    return (
        sample_mean - margin_of_error,
        sample_mean + margin_of_error,
    )


def main() -> None:
    """Run descriptive and inferential statistical analysis."""

    data = pd.read_csv(INPUT_PATH)

    required_columns = {
        "result",
        "fouls_committed",
    }

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    winners = data.loc[
        data["result"] == "Win",
        "fouls_committed",
    ].astype(float)

    losers = data.loc[
        data["result"] == "Loss",
        "fouls_committed",
    ].astype(float)

    if len(winners) == 0 or len(losers) == 0:
        raise ValueError(
            "Winner or loser observations are missing."
        )

    winner_ci_lower, winner_ci_upper = confidence_interval(winners)
    loser_ci_lower, loser_ci_upper = confidence_interval(losers)

    test_result = stats.ttest_ind(
        winners,
        losers,
        equal_var=False,
    )

    mean_difference = winners.mean() - losers.mean()

    descriptive_statistics = pd.DataFrame(
        {
            "group": [
                "Winning teams",
                "Losing teams",
            ],
            "n": [
                len(winners),
                len(losers),
            ],
            "mean_fouls": [
                winners.mean(),
                losers.mean(),
            ],
            "standard_deviation": [
                winners.std(),
                losers.std(),
            ],
            "minimum": [
                winners.min(),
                losers.min(),
            ],
            "maximum": [
                winners.max(),
                losers.max(),
            ],
        }
    )

    confidence_intervals = pd.DataFrame(
        {
            "group": [
                "Winning teams",
                "Losing teams",
            ],
            "n": [
                len(winners),
                len(losers),
            ],
            "mean_fouls": [
                winners.mean(),
                losers.mean(),
            ],
            "ci_level": [
                0.95,
                0.95,
            ],
            "ci_lower": [
                winner_ci_lower,
                loser_ci_lower,
            ],
            "ci_upper": [
                winner_ci_upper,
                loser_ci_upper,
            ],
        }
    )

    hypothesis_results = pd.DataFrame(
        {
            "test": [
                "Welch independent-samples t-test",
            ],
            "winner_n": [
                len(winners),
            ],
            "loser_n": [
                len(losers),
            ],
            "winner_mean": [
                winners.mean(),
            ],
            "loser_mean": [
                losers.mean(),
            ],
            "mean_difference_winner_minus_loser": [
                mean_difference,
            ],
            "t_statistic": [
                test_result.statistic,
            ],
            "degrees_of_freedom": [
                test_result.df,
            ],
            "p_value_two_tailed": [
                test_result.pvalue,
            ],
            "alpha": [
                0.05,
            ],
            "decision": [
                (
                    "Reject H0"
                    if test_result.pvalue < 0.05
                    else "Fail to reject H0"
                ),
            ],
        }
    )

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    descriptive_statistics.to_csv(
        os.path.join(
            OUTPUT_DIRECTORY,
            "fouls_descriptive_statistics.csv",
        ),
        index=False,
    )

    confidence_intervals.to_csv(
        os.path.join(
            OUTPUT_DIRECTORY,
            "fouls_confidence_intervals.csv",
        ),
        index=False,
    )

    hypothesis_results.to_csv(
        os.path.join(
            OUTPUT_DIRECTORY,
            "fouls_hypothesis_test_results.csv",
        ),
        index=False,
    )

    decision = (
        "Reject H0"
        if test_result.pvalue < 0.05
        else "Fail to reject H0"
    )

    summary_lines = [
        "FIFA WORLD CUP 2026 FOULS STATISTICAL ANALYSIS",
        "=" * 60,
        "",
        "1. DESCRIPTIVE STATISTICS",
        "=" * 60,
        f"Winning teams: n = {len(winners)}",
        f"Winning teams mean fouls: {winners.mean():.4f}",
        f"Winning teams standard deviation: {winners.std():.4f}",
        f"Winning teams standard error: {stats.sem(winners):.4f}",
        f"Losing teams: n = {len(losers)}",
        f"Losing teams mean fouls: {losers.mean():.4f}",
        f"Losing teams standard deviation: {losers.std():.4f}",
        f"Losing teams standard error: {stats.sem(losers):.4f}",
        f"Mean difference (winner - loser): {mean_difference:.4f}",
        "",
        "2. 95% CONFIDENCE INTERVALS",
        "=" * 60,
        (
            f"Winning teams: "
            f"{winner_ci_lower:.4f} to {winner_ci_upper:.4f}"
        ),
        (
            f"Losing teams: "
            f"{loser_ci_lower:.4f} to {loser_ci_upper:.4f}"
        ),
        "",
        "3. HYPOTHESIS TEST: WELCH INDEPENDENT-SAMPLES T-TEST",
        "=" * 60,
        f"Null Hypothesis (H0): mu_win = mu_loss (No difference in average fouls)",
        f"Alternative Hypothesis (H1) : mu_win != mu_loss (Difference in average fouls exists)",
        f"Mean difference (winner - loser): {mean_difference:.4f}",
        f"t-statistic: {test_result.statistic:.4f}",
        f"Degrees of freedom: {test_result.df:.4f}",
        f"Two-tailed p-value: {test_result.pvalue:.4f}",
        "Significance level: 0.05",
        f"Decision: {decision}",
    ]

    summary_path = os.path.join(
        OUTPUT_DIRECTORY,
        "fouls_statistical_summary.txt",
    )

    with open(summary_path, "w", encoding="utf-8") as file:
        file.write("\n".join(summary_lines) + "\n")

    print("\n".join(summary_lines))
    print("")
    print("Statistical analysis completed successfully.")


if __name__ == "__main__":
    main()