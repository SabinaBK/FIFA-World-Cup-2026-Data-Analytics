import pandas as pd

df = pd.read_csv("fifa_passing_cleaned.csv")

high_accuracy = df[df["Passing Accuracy (%)"] >= 90]
low_accuracy = df[df["Passing Accuracy (%)"] < 90]

print("90% or greater:", len(high_accuracy))
print("Less than 90%:", len(low_accuracy))