import pandas as pd

df = pd.read_csv("data/cleaned_metadata.csv")

print("Disease distribution:")
print(df["diagnostic"].value_counts())

features = [
    "gender", "region", "itch", "grew",
    "hurt", "changed", "bleed", "elevation"
]

for col in features:
    print("\n", col)
    print(df[col].value_counts())
