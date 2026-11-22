import pandas as pd
df = pd.read_csv("data/metadata.csv")

print("Original records:", len(df))

columns = [
    "patient_id",
    "age",
    "gender",
    "region",
    "itch",
    "grew",
    "hurt",
    "changed",
    "bleed",
    "elevation",
    "diagnostic"
]

df = df[columns].copy()
df = df.dropna(subset=["diagnostic"])
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip().str.upper()

df["gender"] = df["gender"].fillna("UNKNOWN")

symptoms = [
    "itch", "grew", "hurt",
    "changed", "bleed", "elevation"
]

for col in symptoms:
    df[col] = df[col].replace("UNK", "UNKNOWN")
    df[col] = df[col].fillna("UNKNOWN")

df["age"] = pd.to_numeric(df["age"], errors="coerce")

df = df[df["age"].between(0, 120)]

df = df.drop_duplicates()

df.to_csv("data/cleaned_metadata.csv", index=False)

print("\nCleaned records:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDisease distribution:")
print(df["diagnostic"].value_counts())

print("\nCleaned dataset saved successfully!")
