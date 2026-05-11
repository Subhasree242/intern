# Spam Email Detection using Machine Learning

# Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load CSV Dataset
df = pd.read_csv("spam.csv")

# Convert labels into numbers
df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})

# Define features and target
X = df['message']
y = df['label_num']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convert text into vectors
vectorizer = CountVectorizer()

X_train_features = vectorizer.fit_transform(X_train)
X_test_features = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_features, y_train)

# Predictions
y_pred = model.predict(X_test_features)

# Accuracy
print("MODEL ACCURACY:\n")
print(accuracy_score(y_test, y_pred))

# Classification Report
print("\nCLASSIFICATION REPORT:\n")
print(classification_report(y_test, y_pred))

# Confusion Matrix
print("\nCONFUSION MATRIX:\n")
print(confusion_matrix(y_test, y_pred))

# Custom Prediction
sample_message = ["Congratulations! You won a free iPhone"]

sample_features = vectorizer.transform(sample_message)

prediction = model.predict(sample_features)

print("\nCUSTOM MESSAGE PREDICTION:\n")

if prediction[0] == 1:
    print("Spam Message")
else:
    print("Not Spam Message")