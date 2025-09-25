import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, balanced_accuracy_score
import joblib


# ------------------------------
# Blood Pressure split function
# ------------------------------
def split_blood_pressure(bp_string):
    try:
        systolic, diastolic = map(int, bp_string.split('/'))
        return systolic, diastolic
    except:
        return None, None


# -----------------------
# Load dataset
# -----------------------
dataset = pd.read_csv('../ss.csv')


# ------------------------------
# Blood Pressure split
# ------------------------------
dataset[['Systolic', 'Diastolic']] = dataset['Blood Pressure'].apply(
    lambda x: pd.Series(split_blood_pressure(x))
)
dataset.drop(columns=['Blood Pressure'], inplace=True)

# -----------------------
# Drop missing values
# -----------------------
dataset.dropna(inplace=True)

# -----------------------
# Encode categorical features
# -----------------------
le_sleep_disorder = LabelEncoder()
le_gender = LabelEncoder()
le_occupation = LabelEncoder()
le_bmi = LabelEncoder()

dataset['Sleep Disorder'] = le_sleep_disorder.fit_transform(dataset['Sleep Disorder'])
dataset['Gender'] = le_gender.fit_transform(dataset['Gender'])
dataset['Occupation'] = le_occupation.fit_transform(dataset['Occupation'])
dataset['BMI Category'] = le_bmi.fit_transform(dataset['BMI Category'])

# -----------------------
# Split into features and target
# -----------------------
X = dataset[['Sleep Duration', 'Quality of Sleep', 'Stress Level',
             'Physical Activity Level', 'Age', 'BMI Category',
             'Systolic', 'Diastolic', 'Heart Rate', 'Daily Steps',
             'Gender', 'Occupation']]
y = dataset['Sleep Disorder']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------
# Train model
# -----------------------
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train, y_train)

# -----------------------
# Evaluate model (optional, console only)
# -----------------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Balanced Accuracy:", balanced_accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# -----------------------
# Save model + encoders
# -----------------------
joblib.dump(model, "model.joblib")
joblib.dump(le_sleep_disorder, "le_sleep_disorder.joblib")
joblib.dump(le_gender, "le_gender.joblib")
joblib.dump(le_occupation, "le_occupation.joblib")
joblib.dump(le_bmi, "le_bmi.joblib")

print("✅ Model and encoders saved!")
