import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw data"
CLEAN_DIR = DATA_DIR / "cleaned data"

# ==========================================
# 1. LOAD RAW FIFA DATA
# ==========================================

df = pd.read_csv( RAW_DIR / "fifa_passing_raw.csv")

print("\n========== RAW DATA ==========")

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10))


# ==========================================
# 2. CHECK MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())


# ==========================================
# 3. CHECK DUPLICATES
# ==========================================

print("\n========== DUPLICATES ==========")

print("Duplicate rows:", df.duplicated().sum())


# Remove exact duplicate rows
df = df.drop_duplicates()


# ==========================================
# 4. CLEAN PLAYER NAMES
# ==========================================

def clean_player_name(value):

    if pd.isna(value):
        return value

    value = str(value).strip()

    # Example:
    # RodriESPESPMF -> Rodri
    # Pau CubarsiESPESPDF -> Pau Cubarsi

    value = re.sub(
        r'[A-Z]{3}[A-Z]{3}(?:GK|DF|MF|FW)$',
        '',
        value
    )

    return value.strip()


df["Player"] = df["Player"].apply(clean_player_name)


# ==========================================
# 5. CONVERT PASSING ACCURACY TO NUMERIC
# ==========================================

accuracy_column = "Passing Accuracy (%)"

# Remove % symbol if present
df[accuracy_column] = (
    df[accuracy_column]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)

# Convert text to numeric
df[accuracy_column] = pd.to_numeric(
    df[accuracy_column],
    errors="coerce"
)


# ==========================================
# 6. CONVERT PASSING VARIABLES TO NUMERIC
# ==========================================

numeric_columns = [
    "Passes",
    "Passes Completed",
    "Passing Accuracy (%)"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ==========================================
# 7. CHECK MISSING PASSING ACCURACY
# ==========================================

print("\nMissing Passing Accuracy:",
      df[accuracy_column].isnull().sum())


# Remove observations without usable passing accuracy
df = df.dropna(
    subset=[accuracy_column]
)


# ==========================================
# 8. CHECK VALID RANGE
# ==========================================

# Passing accuracy must be between 0 and 100

invalid_accuracy = df[
    (df[accuracy_column] < 0) |
    (df[accuracy_column] > 100)
]

print("\nInvalid Passing Accuracy rows:",
      len(invalid_accuracy))

df = df[
    (df[accuracy_column] >= 0) &
    (df[accuracy_column] <= 100)
]


# ==========================================
# 9. FINAL DATA CHECK
# ==========================================

print("\n========== CLEANED DATA ==========")

print("Number of cleaned rows:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nData types:")
print(df.dtypes)

print("\nFirst 20 cleaned rows:")
print(df.head(20).to_string(index=False))


# ==========================================
# 10. SAVE CLEANED DATA
# ==========================================

df.to_csv(
    CLEAN_DIR / "fifa_passing_cleaned.csv",
    index=False
)

df.to_excel(
    CLEAN_DIR / "fifa_passing_cleaned.xlsx",
    index=False
)

print("\nCleaned dataset saved successfully.")