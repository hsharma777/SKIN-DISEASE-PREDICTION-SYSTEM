from flask import Flask, render_template, request, redirect, session
from prediction import predict_disease
import sqlite3
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "skin_disease.db")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(STATIC_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

@app.route("/")
def home():

    con = sqlite3.connect(DATABASE)

    total = con.execute(
        "SELECT COUNT(*) FROM skin_records"
    ).fetchone()[0]

    patients = con.execute(
        "SELECT COUNT(DISTINCT patient_id) FROM skin_records"
    ).fetchone()[0]

    disease_count = con.execute(
        "SELECT COUNT(DISTINCT diagnostic) FROM skin_records"
    ).fetchone()[0]

    diseases = con.execute("""
        SELECT diagnostic, COUNT(*)
        FROM skin_records
        GROUP BY diagnostic
        ORDER BY COUNT(*) DESC
    """).fetchall()

    ages = con.execute("""
        SELECT
        CASE
            WHEN age < 20 THEN 'Below 20'
            WHEN age < 40 THEN '20-39'
            WHEN age < 60 THEN '40-59'
            ELSE '60+'
        END, COUNT(*)
        FROM skin_records
        GROUP BY 1
        ORDER BY 1
    """).fetchall()

    genders = con.execute("""
        SELECT gender, COUNT(*)
        FROM skin_records
        GROUP BY gender
    """).fetchall()

    regions = con.execute("""
        SELECT region, COUNT(*)
        FROM skin_records
        GROUP BY region
        ORDER BY COUNT(*) DESC
    """).fetchall()

    con.close()

    plt.figure(figsize=(8, 4))
    plt.bar([x[0] for x in diseases], [x[1] for x in diseases])
    plt.title("Disease-wise Distribution")
    plt.xlabel("Disease")
    plt.ylabel("Records")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "disease_chart.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.pie(
        [x[1] for x in ages],
        labels=[x[0] for x in ages],
        autopct="%1.1f%%"
    )
    plt.title("Age Group Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "age_chart.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.pie(
        [x[1] for x in genders],
        labels=[x[0] for x in genders],
        autopct="%1.1f%%"
    )
    plt.title("Gender Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "gender_chart.png"))
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.barh(
        [x[0] for x in regions],
        [x[1] for x in regions]
    )
    plt.title("Lesion Location Distribution")
    plt.xlabel("Records")
    plt.ylabel("Body Region")
    plt.tight_layout()
    plt.savefig(os.path.join(STATIC_DIR, "region_chart.png"))
    plt.close()

    return render_template(
        "index.html",
        total=total,
        patients=patients,
        disease_count=disease_count,
        diseases=diseases,
        accuracy=59.09
    )





@app.route("/predict", methods=["GET", "POST"])
def predict():

    result = None
    full_form = None
    confidence = None
    precautions = []

    disease_names = {
        "ACK": "Actinic Keratosis",
        "BCC": "Basal Cell Carcinoma",
        "MEL": "Melanoma",
        "NEV": "Melanocytic Nevus",
        "SCC": "Squamous Cell Carcinoma",
        "SEK": "Seborrheic Keratosis"
    }

    disease_precautions = {
        "ACK": [
            "Protect your skin from excessive sunlight.",
            "Use sunscreen and protective clothing.",
            "Consult a dermatologist."
        ],
        "BCC": [
            "Consult a dermatologist for evaluation.",
            "Protect the affected area from sunlight.",
            "Avoid scratching or removing the lesion."
        ],
        "MEL": [
            "Seek prompt evaluation from a dermatologist.",
            "Do not delay medical assessment.",
            "Avoid attempting self-treatment."
        ],
        "NEV": [
            "Monitor changes in size, shape or colour.",
            "Consult a dermatologist if changes occur.",
            "Avoid injuring the affected area."
        ],
        "SCC": [
            "Consult a dermatologist promptly.",
            "Protect your skin from sunlight.",
            "Avoid attempting self-treatment."
        ],
        "SEK": [
            "Consult a dermatologist if unsure about the lesion.",
            "Avoid scratching or removing it yourself.",
            "Seek evaluation if it changes or causes discomfort."
        ]
    }

    if request.method == "POST":

        age = int(request.form["age"])
        gender = request.form["gender"]
        region = request.form["region"]

        itch = request.form["itch"]
        grew = request.form["grew"]
        hurt = request.form["hurt"]
        changed = request.form["changed"]
        bleed = request.form["bleed"]
        elevation = request.form["elevation"]

        result, confidence = predict_disease(
            age, gender, region, itch, grew,
            hurt, changed, bleed, elevation
        )

        full_form = disease_names.get(result, result)
        precautions = disease_precautions.get(result, [])

        con = sqlite3.connect(DATABASE)

        con.execute("""
            INSERT INTO prediction_history
            (age, gender, region, itch, grew, hurt,
             changed, bleed, elevation, predicted_disease, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            age, gender, region, itch, grew, hurt,
            changed, bleed, elevation, result, confidence
        ))

        con.commit()
        con.close()

    return render_template(
        "predict.html",
        result=result,
        full_form=full_form,
        confidence=confidence,
        precautions=precautions
    )


    result = None
    confidence = None
    precautions = []

    disease_precautions = {
        "ACK": [
            "Protect your skin from excessive sunlight.",
            "Use sunscreen and protective clothing.",
            "Consult a dermatologist."
        ],
        "BCC": [
            "Consult a dermatologist for evaluation.",
            "Protect the affected area from sunlight.",
            "Avoid scratching or removing the lesion."
        ],
        "MEL": [
            "Seek prompt evaluation from a dermatologist.",
            "Do not delay medical assessment.",
            "Avoid attempting self-treatment."
        ],
        "NEV": [
            "Monitor changes in size, shape or colour.",
            "Consult a dermatologist if changes occur.",
            "Avoid injuring the affected area."
        ],
        "SCC": [
            "Consult a dermatologist promptly.",
            "Protect your skin from sunlight.",
            "Avoid attempting self-treatment."
        ],
        "SEK": [
            "Consult a dermatologist if unsure about the lesion.",
            "Avoid scratching or removing it yourself.",
            "Seek evaluation if it changes or causes discomfort."
        ]
    }

    if request.method == "POST":

        age = int(request.form["age"])
        gender = request.form["gender"]
        region = request.form["region"]

        itch = request.form["itch"]
        grew = request.form["grew"]
        hurt = request.form["hurt"]
        changed = request.form["changed"]
        bleed = request.form["bleed"]
        elevation = request.form["elevation"]

        result, confidence = predict_disease(
            age, gender, region, itch, grew,
            hurt, changed, bleed, elevation
        )

        precautions = disease_precautions.get(result, [])
        con = sqlite3.connect(DATABASE)

        con.execute("""
            INSERT INTO prediction_history
            (age, gender, region, itch, grew, hurt,
             changed, bleed, elevation, predicted_disease, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            age, gender, region, itch, grew, hurt,
            changed, bleed, elevation, result, confidence
        ))

        con.commit()
        con.close()

    return render_template(
        "predict.html",
        result=result,
        confidence=confidence,
        precautions=precautions
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()
            session["admin_logged_in"] = True
            return redirect("/admin")

        error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row

    records = con.execute(
        "SELECT * FROM skin_records"
    ).fetchall()

    con.close()

    return render_template("admin.html", records=records)

@app.route("/delete/<int:id>")
def delete_records(id):

    if not session.get("admin_logged_in"):
        return redirect("/login")

    con = sqlite3.connect(DATABASE)

    con.execute(
        "DELETE FROM skin_records WHERE id = ?", (id,)
    )

    con.commit()
    con.close()

    return redirect("/admin")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")

@app.route("/diseases")
def diseases():

    return render_template("diseases.html")

@app.route("/history")
def history():

    if not session.get("admin_logged_in"):
        return redirect("/login")

    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row

    records = con.execute("""
        SELECT * FROM prediction_history
        ORDER BY id DESC
    """).fetchall()
    con.close()
    return render_template("history.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
