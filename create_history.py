import sqlite3

con = sqlite3.connect("skin_disease.db")

con.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender TEXT,
    region TEXT,
    itch TEXT,
    grew TEXT,
    hurt TEXT,
    changed TEXT,
    bleed TEXT,
    elevation TEXT,
    predicted_disease TEXT,
    confidence REAL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

con.commit()
con.close()

print("Prediction history table created successfully!")
