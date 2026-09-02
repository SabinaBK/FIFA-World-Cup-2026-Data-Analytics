"""
FIFA World Cup 2026 Team-Match Data Preparation Script

Input:
    data/raw/world_cup_2026_match_fouls_raw.csv

Outputs:
    data/processed/team_match_fouls_prepared.csv
    outputs/team_match_preparation_report.txt
"""

import csv
import os
from collections import Counter
from datetime import datetime


INPUT_RAW_PATH = os.path.join(
    "data",
    "raw",
    "world_cup_2026_match_fouls_raw.csv",
)

OUTPUT_PROCESSED_PATH = os.path.join(
    "data",
    "processed",
    "team_match_fouls_prepared.csv",
)

REPORT_OUTPUT_PATH = os.path.join(
    "outputs",
    "team_match_preparation_report.txt",
)

REQUIRED_COLUMNS = [
    "match_id",
    "date",
    "detailed_stage",
    "stage_group",
    "team",
    "opponent",
    "team_position",
    "goals_for",
    "goals_against",
    "result_decision",
    "result",
    "fouls_committed",
]


def load_raw_matches(file_path: str) -> list[dict]:
    """Load match-level records from the extracted CSV file."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with open(file_path, mode="r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def determine_results(
    match_id: int,
    goals_1: int,
    goals_2: int,
    score_1_raw: str,
    score_2_raw: str,
    result_decision: str,
) -> tuple[str, str]:
    """Determine Team 1 and Team 2 results for one match."""

    score_1_lower = score_1_raw.lower()
    score_2_lower = score_2_raw.lower()

    if result_decision == "Penalty Shootout":
        if "p" in score_1_lower and "p" not in score_2_lower:
            return "Win", "Loss"

        if "p" in score_2_lower and "p" not in score_1_lower:
            return "Loss", "Win"

        raise ValueError(
            f"Match ID {match_id} is marked as a penalty shootout, "
            f"but a unique penalty winner could not be identified: "
            f"'{score_1_raw}' vs '{score_2_raw}'."
        )

    if goals_1 > goals_2:
        return "Win", "Loss"

    if goals_2 > goals_1:
        return "Loss", "Win"

    return "Draw", "Draw"


def transform_matches_to_team_matches(
    matches: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Transform every match into one Team 1 row and one Team 2 row."""

    team_match_records = []
    penalty_matches_summary = []

    for match in matches:
        match_id = int(match["match_id"])
        match_date = match["date"]
        detailed_stage = match["detailed_stage"]
        stage_group = match["stage_group"]

        team_1 = match["team_1"]
        team_2 = match["team_2"]

        score_1_raw = match["team_1_score_raw"]
        score_2_raw = match["team_2_score_raw"]

        goals_1 = int(match["team_1_goals"])
        goals_2 = int(match["team_2_goals"])

        result_decision = match["result_decision"]

        fouls_1 = int(match["team_1_fouls"])
        fouls_2 = int(match["team_2_fouls"])

        result_1, result_2 = determine_results(
            match_id=match_id,
            goals_1=goals_1,
            goals_2=goals_2,
            score_1_raw=score_1_raw,
            score_2_raw=score_2_raw,
            result_decision=result_decision,
        )

        if result_decision == "Penalty Shootout":
            penalty_matches_summary.append(
                {
                    "match_id": match_id,
                    "date": match_date,
                    "detailed_stage": detailed_stage,
                    "team_1": team_1,
                    "team_1_score_raw": score_1_raw,
                    "result_1": result_1,
                    "fouls_1": fouls_1,
                    "team_2": team_2,
                    "team_2_score_raw": score_2_raw,
                    "result_2": result_2,
                    "fouls_2": fouls_2,
                }
            )

        team_match_records.append(
            {
                "match_id": match_id,
                "date": match_date,
                "detailed_stage": detailed_stage,
                "stage_group": stage_group,
                "team": team_1,
                "opponent": team_2,
                "team_position": "Team 1",
                "goals_for": goals_1,
                "goals_against": goals_2,
                "result_decision": result_decision,
                "result": result_1,
                "fouls_committed": fouls_1,
            }
        )

        team_match_records.append(
            {
                "match_id": match_id,
                "date": match_date,
                "detailed_stage": detailed_stage,
                "stage_group": stage_group,
                "team": team_2,
                "opponent": team_1,
                "team_position": "Team 2",
                "goals_for": goals_2,
                "goals_against": goals_1,
                "result_decision": result_decision,
                "result": result_2,
                "fouls_committed": fouls_2,
            }
        )

    return team_match_records, penalty_matches_summary


def validate_team_matches(matches: list[dict], team_matches: list[dict]) -> None:
    """Validate row counts, pairs, required values, and outcomes."""

    expected_team_rows = len(matches) * 2

    if len(team_matches) != expected_team_rows:
        raise AssertionError(
            f"Expected {expected_team_rows} team-match rows, "
            f"but found {len(team_matches)}."
        )

    match_id_counts = Counter(row["match_id"] for row in team_matches)

    for match_id, count in match_id_counts.items():
        if count != 2:
            raise AssertionError(
                f"Match ID {match_id} occurs {count} times; it should occur twice."
            )

    records_by_match_id = {}

    for row in team_matches:
        for column in REQUIRED_COLUMNS:
            value = row.get(column)

            if value is None or str(value).strip() == "":
                raise AssertionError(
                    f"Missing value in '{column}' for record: {row}"
                )

        records_by_match_id.setdefault(row["match_id"], []).append(row)

    for match_id, rows in records_by_match_id.items():
        positions = sorted(row["team_position"] for row in rows)

        if positions != ["Team 1", "Team 2"]:
            raise AssertionError(
                f"Match ID {match_id} has invalid team positions: {positions}"
            )

        teams = {row["team"] for row in rows}

        if len(teams) != 2:
            raise AssertionError(
                f"Match ID {match_id} does not contain two distinct teams."
            )

        results = sorted(row["result"] for row in rows)
        decision = rows[0]["result_decision"]

        if decision == "Penalty Shootout":
            valid_results = ["Loss", "Win"]
        else:
            valid_results = [["Draw", "Draw"], ["Loss", "Win"]]

        if decision == "Penalty Shootout":
            if results != valid_results:
                raise AssertionError(
                    f"Penalty match {match_id} has invalid results: {results}"
                )
        elif results not in valid_results:
            raise AssertionError(
                f"Match {match_id} has invalid results: {results}"
            )


def save_processed_csv(team_matches: list[dict], output_path: str) -> None:
    """Save prepared team-match records to a CSV file."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(team_matches)


def generate_preparation_report(
    matches: list[dict],
    team_matches: list[dict],
    penalty_summary: list[dict],
    report_path: str,
) -> None:
    """Generate a data-preparation report based on actual results."""

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    stage_group_counts = Counter(
        row["stage_group"] for row in team_matches
    )
    detailed_stage_counts = Counter(
        row["detailed_stage"] for row in team_matches
    )
    result_counts = Counter(
        row["result"] for row in team_matches
    )

    n_win = result_counts["Win"]
    n_loss = result_counts["Loss"]
    n_draw = result_counts["Draw"]

    missing_counts = {column: 0 for column in REQUIRED_COLUMNS}

    for row in team_matches:
        for column in REQUIRED_COLUMNS:
            value = row.get(column)

            if value is None or str(value).strip() == "":
                missing_counts[column] += 1

    lines = [
        "=" * 80,
        "FIFA WORLD CUP 2026 TEAM-MATCH DATA PREPARATION REPORT",
        "=" * 80,
        f"Preparation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Input raw dataset: {INPUT_RAW_PATH}",
        f"Output prepared dataset: {OUTPUT_PROCESSED_PATH}",
        "-" * 80,
        "ROW COUNT AUDIT:",
        f"  - Input matches: {len(matches)}",
        f"  - Output team-match records: {len(team_matches)}",
        f"  - Expected output records: {len(matches) * 2}",
        "",
        "STAGE DISTRIBUTION:",
        f"  - Group Stage records: {stage_group_counts['Group Stage']}",
        f"  - Knockout records: {stage_group_counts['Knockout']}",
        "",
        "DETAILED STAGE BREAKDOWN:",
    ]

    for stage in [
        "GROUP STAGE",
        "ROUND OF 32",
        "ROUND OF 16",
        "QUARTER FINALS",
        "SEMI FINALS",
        "FINAL",
    ]:
        record_count = detailed_stage_counts[stage]
        lines.append(
            f"  - {stage:<20}: {record_count:>3} records "
            f"({record_count // 2} matches)"
        )

    lines.extend(
        [
            "",
            "RESULT CLASSIFICATION:",
            f"  - Wins: {n_win}",
            f"  - Losses: {n_loss}",
            f"  - Draws: {n_draw}",
            f"  - Total records: {n_win + n_loss + n_draw}",
            "",
            "RESEARCH SAMPLE:",
            f"  - Winning teams: {n_win}",
            f"  - Losing teams: {n_loss}",
            (
                "  - Sample-size adequacy (both groups >= 30): "
                f"{'YES' if n_win >= 30 and n_loss >= 30 else 'NO'}"
            ),
            "",
            "PENALTY SHOOTOUTS:",
            f"  - Penalty shootout matches identified: {len(penalty_summary)}",
            "",
            "MISSING VALUE AUDIT:",
        ]
    )

    for column, count in missing_counts.items():
        lines.append(f"  - {column}: {count}")

    lines.extend(
        [
            "",
            "PENALTY SHOOTOUT DETAILS:",
        ]
    )

    if penalty_summary:
        for match in penalty_summary:
            lines.append(
                f"  - Match {match['match_id']} "
                f"({match['detailed_stage']}, {match['date']}): "
                f"{match['team_1']} [{match['team_1_score_raw']}] "
                f"= {match['result_1']}; "
                f"{match['team_2']} [{match['team_2_score_raw']}] "
                f"= {match['result_2']}"
            )
    else:
        lines.append("  - No penalty shootout matches were identified.")

    lines.append("=" * 80)

    with open(report_path, mode="w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def print_terminal_summary(
    team_matches: list[dict],
    penalty_summary: list[dict],
) -> None:
    """Print concise outcome and validation information."""

    result_counts = Counter(
        row["result"] for row in team_matches
    )

    print("\nTEAM-MATCH PREPARATION RESULTS")
    print("=" * 50)
    print(f"Win records: {result_counts['Win']}")
    print(f"Loss records: {result_counts['Loss']}")
    print(f"Draw records: {result_counts['Draw']}")
    print(f"Total records: {len(team_matches)}")
    print(f"Penalty shootout matches: {len(penalty_summary)}")


def main() -> None:
    """Run the complete team-match data-preparation process."""

    print(f"Reading raw data: {INPUT_RAW_PATH}")
    matches = load_raw_matches(INPUT_RAW_PATH)

    print(f"Raw matches loaded: {len(matches)}")
    print("Creating team-match records...")

    team_matches, penalty_summary = transform_matches_to_team_matches(
        matches
    )

    print("Validating prepared records...")
    validate_team_matches(matches, team_matches)

    save_processed_csv(team_matches, OUTPUT_PROCESSED_PATH)

    generate_preparation_report(
        matches=matches,
        team_matches=team_matches,
        penalty_summary=penalty_summary,
        report_path=REPORT_OUTPUT_PATH,
    )

    print_terminal_summary(team_matches, penalty_summary)

    print("\nPreparation completed successfully.")
    print(f"Prepared CSV: {OUTPUT_PROCESSED_PATH}")
    print(f"Report: {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()