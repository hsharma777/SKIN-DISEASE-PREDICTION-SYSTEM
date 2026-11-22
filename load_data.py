import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = os.path.join(BASE_DIR, "data", "cleaned_metadata.csv")
DB_FILE = os.path.join(BASE_DIR, "skin_disease.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

df = pd.read_csv(CSV_FILE)

con = sqlite3.connect(DB_FILE)

try:
    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        con.executescript(file.read())

    df.to_sql(
        "skin_records",
        con,
        if_exists="append",
        index=False
    )

    total = con.execute(
        "SELECT COUNT(*) FROM skin_records"
    ).fetchone()[0]

    print("Data imported successfully!")
    print("Database:", DB_FILE)
    print("Total records:", total)

    result = con.execute("""
        SELECT diagnostic, COUNT(*)
        FROM skin_records
        GROUP BY diagnostic
        ORDER BY COUNT(*) DESC
    """).fetchall()

    print("\nDisease-wise records:")

    for disease, count in result:
        print(disease, ":", count)

finally:
    con.close()
