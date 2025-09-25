import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, balanced_accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
dataset = pd.read_csv('../ss.csv')


# Split Blood Pressure into Systolic and Diastolic values
def split_blood_pressure(bp_string):
    try:
        systolic, diastolic = map(int, bp_string.split('/'))
        return systolic, diastolic
    except:
        return None, None  # In case of invalid format

# Apply the function to the Blood Pressure column
dataset[['Systolic', 'Diastolic']] = dataset['Blood Pressure'].apply(lambda x: pd.Series(split_blood_pressure(x)))

# Now drop the original 'Blood Pressure' column
dataset.drop(columns=['Blood Pressure'], inplace=True)


# Data Preprocessing
dataset.dropna(inplace=True)  # Remove rows with missing values

# Label Encoding for categorical variables
le = LabelEncoder()
dataset['Sleep Disorder'] = le.fit_transform(dataset['Sleep Disorder'])
dataset['Gender'] = le.fit_transform(dataset['Gender'])
dataset['Occupation'] = le.fit_transform(dataset['Occupation'])
dataset['BMI Category'] = le.fit_transform(dataset['BMI Category'])

# Split the data into features (X) and target (y)
X = dataset[['Sleep Duration', 'Quality of Sleep', 'Stress Level', 'Physical Activity Level', 'Age', 
             'BMI Category', 'Systolic', 'Diastolic', 'Heart Rate', 'Daily Steps', 'Gender', 'Occupation']]
y = dataset['Sleep Disorder']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the multinomial logistic regression model
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# # Display Confusion Matrix with Seaborn Heatmap
# sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Confusion Matrix')
# plt.show()

# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Classification Report for different metrics
print("Classification Report:\n", classification_report(y_test, y_pred))

# Balanced Accuracy
balanced_accuracy = balanced_accuracy_score(y_test, y_pred)
print(f"Balanced Accuracy: {balanced_accuracy:.4f}")



import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from itertools import cycle

# Line graph of actual vs predicted
plt.figure(figsize=(12,6))
plt.plot(range(len(y_test)), y_test.values, label='Actual', marker='o')
plt.plot(range(len(y_pred)), y_pred, label='Predicted', marker='x')
plt.title('Actual vs Predicted Sleep Disorder')
plt.xlabel('Sample Index')
plt.ylabel('Sleep Disorder Class')
plt.legend()
plt.grid(True)
plt.savefig('line_chart.png')
plt.show()





import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
dataset = pd.read_csv('../ss.csv')  # adjust path as needed
print(dataset["Sleep Disorder"].unique())


dataset['Sleep Disorder'] = dataset['Sleep Disorder'].fillna('No Disorder')
# Count the number of people in each sleep disorder category
sleep_disorder_counts = dataset['Sleep Disorder'].value_counts()

# Plotting the bar chart
plt.figure(figsize=(12,6))
# plt.bar(sleep_disorder_counts.index, sleep_disorder_counts.values, color=['green', 'orange', 'red'])
sleep_disorder_counts.plot(kind='bar', color=['gray', 'orange', 'skyblue'])
plt.title('Distribution of Sleep Disorders')
plt.xlabel('Sleep Disorder Type')
plt.ylabel('Number of People')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the chart
plt.savefig('bar_chart.png')
plt.show()