DROP TABLE IF EXISTS skin_records;

CREATE TABLE skin_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    region TEXT NOT NULL,
    itch TEXT,
    grew TEXT,
    hurt TEXT,
    changed TEXT,
    bleed TEXT,
    elevation TEXT,
    diagnostic TEXT NOT NULL
);


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
);

