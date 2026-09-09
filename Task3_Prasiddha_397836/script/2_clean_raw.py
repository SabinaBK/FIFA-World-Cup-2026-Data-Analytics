import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw data"

# Load raw dataset
df = pd.read_csv(RAW_DIR / "fifa_passing_raw.csv")

print("Before cleaning:")
print(df["Player"].head(20))


# -----------------------------------------
# CLEAN PLAYER NAME
# -----------------------------------------

def clean_player_name(value):
    value = str(value).strip()

    # FIFA format examples:
    # RodriESPESPMF
    # Pau CubarsiESPESPDF
    # Leandro ParedesARGARGMF
    #
    # Remove:
    # 3-letter country code
    # repeated 3-letter country code
    # position (GK, DF, MF, FW)

    value = re.sub(
        r'[A-Z]{3}[A-Z]{3}(?:GK|DF|MF|FW)$',
        '',
        value
    )

    return value.strip()


df["Player"] = df["Player"].apply(clean_player_name)


# -----------------------------------------
# CHECK RESULT
# -----------------------------------------

print("\nAfter cleaning:")
print(df["Player"].head(30).to_string(index=False))


# -----------------------------------------
# SAVE CLEANED DATA
# -----------------------------------------

df.to_csv(
    "fifa_passing_cleaned.csv",
    index=False
)

df.to_excel(
    "fifa_passing_cleaned.xlsx",
    index=False
)

print("\nCleaned files saved successfully.")