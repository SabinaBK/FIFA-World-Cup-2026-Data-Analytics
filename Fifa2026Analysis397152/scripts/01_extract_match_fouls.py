"""
Extract FIFA World Cup 2026 match-level foul data from the published source.

Source website:
https://www.thestatsdontlie.com/football/world-cup-2026/

Published Google Sheets endpoint:
https://docs.google.com/spreadsheets/d/e/2PACX-1vSWZFlaUHTBK09v4I1Kv7ZQ0ophhlpsCr7VPFW5dkbdG0Zpl8mRkXrTZezZMr1Ia9V9cpwmq7BKPQ03/pubhtml/sheet?headers=false&gid=995472238
"""

import csv
import html
import os
import re
import urllib.request
from datetime import datetime


APPROVED_WEBSITE_URL = "https://www.thestatsdontlie.com/football/world-cup-2026/"

EMBEDDED_SHEET_ENDPOINT = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSWZFlaUHTBK09v4I1Kv7ZQ0ophhlpsCr7VPFW5dkbdG0Zpl8mRkXrTZezZMr1Ia9V9cpwmq7BKPQ03/"
    "pubhtml/sheet?headers=false&gid=995472238"
)

RAW_OUTPUT_PATH = os.path.join(
    "data", "raw", "world_cup_2026_match_fouls_raw.csv"
)

REPORT_OUTPUT_PATH = os.path.join(
    "outputs", "match_extraction_report.txt"
)

VALID_DETAILED_STAGES = [
    "GROUP STAGE",
    "ROUND OF 32",
    "ROUND OF 16",
    "QUARTER FINALS",
    "SEMI FINALS",
    "FINAL",
]


def fetch_sheet_html(url: str) -> str:
    """Download the published Google Sheets HTML."""

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Safari/605.1.15"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def clean_cell(cell: str) -> str:
    """Remove HTML tags and decode HTML entities from one table cell."""

    text = re.sub(r"<[^>]+>", "", cell)
    return html.unescape(text).strip()


def score_to_goals(score: str) -> int:
    """Convert score text such as '2', '1p', or 'p0' to an integer goal value."""

    digits = re.findall(r"\d+", score)
    if not digits:
        raise ValueError(f"Could not read numeric score from: {score!r}")
    return int(digits[0])


def parse_match_rows(html_content: str) -> list[dict]:
    """Parse match rows from the published Google Sheets HTML table."""

    rows = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", html_content)

    current_stage = None
    matches = []

    for row in rows:
        cells = re.findall(r"<(?:td|th)[^>]*>([\s\S]*?)</(?:td|th)>", row)
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

            match = {
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
                    if "p" in score_1_raw.lower() or "p" in score_2_raw.lower()
                    else "Normal Time / Extra Time"
                ),
                "team_1_fouls": int(clean[27]),
                "team_2_fouls": int(clean[28]),
            }

            matches.append(match)

        except (ValueError, IndexError):
            continue

    return matches


def save_csv(matches: list[dict], output_path: str) -> None:
    """Save extracted match-level records as a CSV file."""

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

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)


def save_report(matches: list[dict], report_path: str) -> None:
    """Save a short extraction report."""

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
        "=" * 60,
        f"Extraction time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Source website: {APPROVED_WEBSITE_URL}",
        f"Published sheet: {EMBEDDED_SHEET_ENDPOINT}",
        "",
        f"Group stage matches: {group_count}",
        f"Knockout matches: {knockout_count}",
        f"Total matches extracted: {len(matches)}",
    ]

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def main() -> None:
    """Run the extraction process."""

    print("Downloading the published Google Sheet...")
    html_content = fetch_sheet_html(EMBEDDED_SHEET_ENDPOINT)

    print("Parsing match rows...")
    matches = parse_match_rows(html_content)

    if not matches:
        raise ValueError(
            "No match rows were extracted. Check the sheet endpoint and table format."
        )

    save_csv(matches, RAW_OUTPUT_PATH)
    save_report(matches, REPORT_OUTPUT_PATH)

    print(f"Extraction complete: {len(matches)} matches saved.")
    print(f"Raw data: {RAW_OUTPUT_PATH}")
    print(f"Report: {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()