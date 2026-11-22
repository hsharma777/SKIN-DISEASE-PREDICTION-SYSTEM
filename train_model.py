import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("data/cleaned_metadata.csv")

features = [
    "age", "gender", "region", "itch", "grew",
    "hurt", "changed", "bleed", "elevation"
]

X = df[features]
y = df["diagnostic"]

X = pd.get_dummies(X)
train, test = train_test_split(
    df["patient_id"].unique(),
    test_size=0.2,
    random_state=42
)

train_data = df[df["patient_id"].isin(train)]
test_data = df[df["patient_id"].isin(test)]

X_train = pd.get_dummies(train_data[features])
X_test = pd.get_dummies(test_data[features])

X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

y_train = train_data["diagnostic"]
y_test = test_data["diagnostic"]

model = DecisionTreeClassifier(
    max_depth=5,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", round(
    accuracy_score(y_test, predictions) * 100, 2
), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

model.fit(X, y)
joblib.dump(
    {"model": model, "columns": X.columns.tolist()},
    "skin_disease_model.pkl"
)

print("\nModel trained and saved successfully!")
