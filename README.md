🩺 Skin Disease Prediction System

A web-based Skin Disease Prediction System developed using Python Flask, SQLite, and Machine Learning. The system predicts six skin disease categories using patient and lesion metadata from the PAD-UFES-20 dataset.

━━━━━━━━━━━━━━━━━━━━

📌 PROJECT OVERVIEW

The Skin Disease Prediction System is an academic MCA project designed to demonstrate how machine learning can be used to classify skin diseases based on patient information and lesion-related symptoms.

The system uses a Decision Tree Classifier to predict the possible disease category from the provided metadata.

🎯 OBJECTIVES

- 🧠 Predict skin disease categories using machine learning.
- 👤 Manage patient records.
- 📊 Display dataset statistics through charts.
- 📝 Store and view previous prediction records.
- 🔐 Provide an admin login and dashboard.
- 📚 Display information about six skin disease categories.

🛠️ TECHNOLOGIES USED

| Technology | Purpose |
|---|---|
| 🐍 Python | Main programming language |
| 🌐 Flask | Web application framework |
| 🗄️ SQLite | Database management |
| 🤖 Scikit-learn | Machine learning |
| 🐼 Pandas | Dataset processing |
| 📈 Matplotlib | Data visualization |
| 🎨 HTML & Bootstrap 5 | User interface |
| 📦 Joblib | Saving the trained model |

📂 DATASET INFORMATION

Dataset: PAD-UFES-20

The project uses patient and lesion metadata only. It does not use skin images for machine learning prediction.

The system predicts the following six categories:

| Code | Disease Name |
|---|---|
| ACK | Actinic Keratosis |
| BCC | Basal Cell Carcinoma |
| MEL | Melanoma |
| NEV | Melanocytic Nevus |
| SCC | Squamous Cell Carcinoma |
| SEK | Seborrheic Keratosis |

⚙️ MACHINE LEARNING MODEL

- Algorithm: Decision Tree Classifier
- Data preprocessing: Missing-value cleaning and categorical encoding
- Class balancing: Balanced class weights
- Model evaluation: Accuracy and classification report
- Reported test accuracy: 59.09%

✨ FEATURES

- 🏠 Dashboard with dataset statistics and charts
- 👨‍⚕️ Patient record management
- 🔍 Metadata-based skin disease prediction
- 📊 Prediction result with probability score
- 📖 Information about six skin disease categories
- 🔐 Admin login system
- 📋 Prediction history
- 🗑️ Admin option to delete patient records

📁 PROJECT STRUCTURE

```text
skin-disease-prediction-system/
│
├── data/
│   ├── metadata.csv
│   └── cleaned_metadata.csv
│
├── static/
│   ├── disease_chart.png
│   ├── age_chart.png
│   ├── gender_chart.png
│   └── region_chart.png
│
├── templates/
│   ├── index.html
│   ├── predict.html
│   ├── diseases.html
│   ├── login.html
│   ├── admin.html
│   └── history.html
│
├── app.py
├── clean_data.py
├── load_data.py
├── prediction.py
├── train_model.py
├── schema
