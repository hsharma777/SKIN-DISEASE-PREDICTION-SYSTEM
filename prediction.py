import pandas as pd
import joblib

data = joblib.load("skin_disease_model.pkl")

model = data["model"]
columns = data["columns"]

def predict_disease(age, gender, region, itch, grew,
                    hurt, changed, bleed, elevation):

    values = {
        "age": age,
        "gender": gender,
        "region": region,
        "itch": itch,
        "grew": grew,
        "hurt": hurt,
        "changed": changed,
        "bleed": bleed,
        "elevation": elevation
    }

    for key in ["itch", "grew", "hurt", "changed", "bleed", "elevation"]:
        if values[key] == "YES":
            values[key] = "TRUE"
        elif values[key] == "NO":
            values[key] = "FALSE"

    input_data = pd.DataFrame([values])

    input_data = pd.get_dummies(input_data)
    input_data = input_data.reindex(columns=columns, fill_value=0)

    probabilities = model.predict_proba(input_data)[0]
    result = model.classes_[probabilities.argmax()]

    confidence = round(max(probabilities) * 100, 2)

    print("Prediction:", result)
    print("Probabilities:")

    for disease, probability in zip(model.classes_, probabilities):
        print(disease, round(probability * 100, 2), "%")

    return result, confidence
