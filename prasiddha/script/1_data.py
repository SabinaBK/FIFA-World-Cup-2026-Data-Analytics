from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw data"



# -----------------------------------
# 1. READ HTML FILE
# -----------------------------------

tables = pd.read_html(BASE_DIR / "player.html")

print("Number of tables found:", len(tables))


# -----------------------------------
# 2. SELECT THE TABLE
# -----------------------------------

# Change [0] if your passing table has a different number
df = tables[0]

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nNumber of rows:", len(df))


# -----------------------------------
# 3. SAVE RAW DATA
# -----------------------------------

df.to_csv(
     RAW_DIR / "fifa_passing_raw.csv",
    index=False
)

df.to_excel(
     RAW_DIR / "fifa_passing_raw.xlsx",
    index=False
)

print("\nRaw data saved successfully!")
print("CSV: fifa_passing_raw.csv")
print("Excel: fifa_passing_raw.xlsx")