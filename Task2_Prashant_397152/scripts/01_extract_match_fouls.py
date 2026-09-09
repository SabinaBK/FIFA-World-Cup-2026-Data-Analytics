"""
Extract FIFA World Cup 2026 match-level foul data.

Primary source:
https://www.thestatsdontlie.com/football/world-cup-2026/

Published Google Sheets endpoint:
https://docs.google.com/spreadsheets/d/e/2PACX-1vSWZFlaUHTBK09v4I1Kv7ZQ0ophhlpsCr7VPFW5dkbdG0Zpl8mRkXrTZezZMr1Ia9V9cpwmq7BKPQ03/pubhtml/sheet?headers=false&gid=995472238

Supplementary approved source for the omitted third-place match:
https://fbref.com/en/matches/aba06a2a/France-England-July-18-2026-World-Cup

Note:
The published Google Sheets endpoint contains 103 match records and omits
the third-place play-off. The verified France versus England third-place
match is added transparently from FBref so the final dataset contains all
104 tournament matches.
"""

import csv
import html
import os
import re
import urllib.request
from datetime import datetime


PRIMARY_SOURCE_URL = (
    "https://www.thestatsdontlie.com/football/world-cup-2026/"
)

EMBEDDED_SHEET_ENDPOINT = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSWZFlaUHTBK09v4I1Kv7ZQ0ophhlpsCr7VPFW5dkbdG0Zpl8mRkXrTZezZMr1Ia9V9cpwmq7BKPQ03/"
    "pubhtml/sheet?headers=false&gid=995472238"
)

FBREF_THIRD_PLACE_MATCH_URL = (
    "https://fbref.com/en/matches/aba06a2a/"
    "France-England-July-18-2026-World-Cup"
)

RAW_OUTPUT_PATH = os.path.join(
    "data",
    "raw",
    "world_cup_2026_match_fouls_raw.csv",
)

REPORT_OUTPUT_PATH = os.path.join(
    "outputs",
    "match_extraction_report.txt",
)

VALID_DETAILED_STAGES = [
    "GROUP STAGE",
    "ROUND OF 32",
    "ROUND OF 16",
    "QUARTER FINALS",
    "SEMI FINALS",
    "FINAL",
]

THIRD_PLACE_MATCH = {
    "date": "18/07/2026",
    "detailed_stage": "THIRD-PLACE PLAY-OFF",
    "stage_group": "Knockout",
    "team_1": "France",
    "team_2": "England",
    "team_1_score_raw": "4",
    "team_2_score_raw": "6",
    "team_1_goals": 4,
    "team_2_goals": 6,
    "result_decision": "Normal Time / Extra Time",
    "team_1_fouls": 14,
    "team_2_fouls": 8,
}


def fetch_sheet_html(url: str) -> str:
    """Download HTML from the published Google Sheets endpoint."""

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Safari/605.1.15"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,*/*;q=0.8"
        ),
    }

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def clean_cell(cell: str) -> str:
    """Remove HTML tags and decode HTML entities from a table cell."""

    text = re.sub(r"<[^>]+>", "", cell)
    return html.unescape(text).strip()


def score_to_goals(score: str) -> int:
    """Extract numeric goals from score values such as '2', '1p' or 'p0'."""

    digits = re.findall(r"\d+", score)

    if not digits:
        raise ValueError(f"Could not read numeric score from: {score!r}")

    return int(digits[0])


def parse_match_rows(html_content: str) -> list[dict]:
    """Parse match-level records from the published sheet HTML."""

    rows = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", html_content)

    current_stage = None
    matches = []

    for row in rows:
        cells = re.findall(
            r"<(?:td|th)[^>]*>([\s\S]*?)</(?:td|th)>",
            row,
        )

        clean = [clean_cell(cell) for cell in cells]

        if len(clean) == 2 and clean[1] in VALID_DETAILED_STAGES:
            current_stage = clean[1]
            continue

        if len(clean) < 29 or current_stage is None:
            continue

        if clean[1] in ("", "Date") or "/" not in clean[1]:
            continue

        try:
            score_1_raw = clean[3]
            score_2_raw = clean[4]

            matches.append(
                {
                    "match_id": len(matches) + 1,
                    "date": clean[1],
                    "detailed_stage": current_stage,
                    "stage_group": (
                        "Group Stage"
                        if current_stage == "GROUP STAGE"
                        else "Knockout"
                    ),
                    "team_1": clean[2],
                    "team_2": clean[5],
                    "team_1_score_raw": score_1_raw,
                    "team_2_score_raw": score_2_raw,
                    "team_1_goals": score_to_goals(score_1_raw),
                    "team_2_goals": score_to_goals(score_2_raw),
                    "result_decision": (
                        "Penalty Shootout"
                        if (
                            "p" in score_1_raw.lower()
                            or "p" in score_2_raw.lower()
                        )
                        else "Normal Time / Extra Time"
                    ),
                    "team_1_fouls": int(clean[27]),
                    "team_2_fouls": int(clean[28]),
                }
            )

        except (ValueError, IndexError):
            continue

    return matches


def add_verified_third_place_match(matches: list[dict]) -> list[dict]:
    """Add the verified FBref third-place match if it is absent."""

    third_place_exists = any(
        match["detailed_stage"] == "THIRD-PLACE PLAY-OFF"
        for match in matches
    )

    if not third_place_exists:
        matches.append(THIRD_PLACE_MATCH.copy())

    matches.sort(
        key=lambda match: (
            datetime.strptime(match["date"], "%d/%m/%Y"),
            0 if match["detailed_stage"] == "THIRD-PLACE PLAY-OFF" else 1,
        )
    )

    for match_id, match in enumerate(matches, start=1):
        match["match_id"] = match_id

    return matches


def validate_completed_dataset(matches: list[dict]) -> None:
    """Validate the complete 104-match dataset."""

    if len(matches) != 104:
        raise AssertionError(
            f"Expected 104 matches after supplementation, found {len(matches)}."
        )

    match_ids = [match["match_id"] for match in matches]

    if match_ids != list(range(1, 105)):
        raise AssertionError(
            "Match IDs are not sequential from 1 to 104."
        )

    third_place_matches = [
        match
        for match in matches
        if match["detailed_stage"] == "THIRD-PLACE PLAY-OFF"
    ]

    if len(third_place_matches) != 1:
        raise AssertionError(
            "Expected exactly one third-place play-off record."
        )


def save_csv(matches: list[dict], output_path: str) -> None:
    """Save all completed match-level records as CSV."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = [
        "match_id",
        "date",
        "detailed_stage",
        "stage_group",
        "team_1",
        "team_2",
        "team_1_score_raw",
        "team_2_score_raw",
        "team_1_goals",
        "team_2_goals",
        "result_decision",
        "team_1_fouls",
        "team_2_fouls",
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)


def save_report(matches: list[dict], report_path: str) -> None:
    """Save an extraction report with complete source documentation."""

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    group_count = sum(
        match["stage_group"] == "Group Stage"
        for match in matches
    )

    knockout_count = sum(
        match["stage_group"] == "Knockout"
        for match in matches
    )

    lines = [
        "FIFA WORLD CUP 2026 MATCH FOULS EXTRACTION REPORT",
        "=" * 70,
        f"Extraction time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "PRIMARY SOURCE:",
        f"The Stats Don't Lie: {PRIMARY_SOURCE_URL}",
        f"Published Google Sheet: {EMBEDDED_SHEET_ENDPOINT}",
        "",
        "SUPPLEMENTARY APPROVED SOURCE:",
        f"FBref third-place match report: {FBREF_THIRD_PLACE_MATCH_URL}",
        "",
        "DATA COMPLETENESS:",
        "The published Google Sheets endpoint contains 103 match records.",
        "It omits the official third-place play-off.",
        "The omitted France versus England match was verified from FBref",
        "and added as one transparent supplementary record.",
        "No values were estimated, imputed or fabricated.",
        "",
        "VERIFIED SUPPLEMENTARY RECORD:",
        "France 4-6 England",
        "Date: 18/07/2026",
        "Stage: THIRD-PLACE PLAY-OFF",
        "France fouls: 14",
        "England fouls: 8",
        "",
        "FINAL DATASET SUMMARY:",
        f"Group stage matches: {group_count}",
        f"Knockout matches: {knockout_count}",
        f"Total completed match records: {len(matches)}",
    ]

    with open(report_path, mode="w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def main() -> None:
    """Extract primary data, add approved supplementary record and save CSV."""

    print("Downloading the published Google Sheet...")
    html_content = fetch_sheet_html(EMBEDDED_SHEET_ENDPOINT)

    print("Parsing primary match rows...")
    matches = parse_match_rows(html_content)

    if not matches:
        raise ValueError(
            "No match rows were extracted. Check the sheet endpoint and table format."
        )

    print(f"Primary source matches extracted: {len(matches)}")

    matches = add_verified_third_place_match(matches)

    print("Adding verified FBref third-place match...")
    print(f"Completed dataset matches: {len(matches)}")

    validate_completed_dataset(matches)

    save_csv(matches, RAW_OUTPUT_PATH)
    save_report(matches, REPORT_OUTPUT_PATH)

    print("Extraction and supplementation completed successfully.")
    print(f"Raw data: {RAW_OUTPUT_PATH}")
    print(f"Report: {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()