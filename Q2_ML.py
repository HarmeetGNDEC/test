import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
import joblib

# Prepare the data for classification
labeled_data = pd.read_excel('violation_calls.xlsx')
labeled_data = labeled_data.fillna('')
labeled_data = labeled_data.to_dict(orient='records')
texts = [data['conversation'] for data in labeled_data]
labels = [data['label'] for data in labeled_data]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)
y = labels


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the classifier (Logistic Regression)
classifier = LogisticRegression(class_weight='balanced', random_state=42)

# Train the model
classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = classifier.predict(X_test)

# rf_model = RandomForestClassifier(class_weight='balanced', random_state=42)
# rf_model.fit(X_train, y_train)
# y_pred_rf = classifier.predict(X_test)

# Evaluate the model
print(f"Accuracy Logistic: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# print(f"Accuracy RandomForest: {accuracy_score(y_test, y_pred_rf)}")
# print(classification_report(y_test, y_pred_rf))
joblib.dump(classifier, './models/privacy_model.pkl')
joblib.dump(vectorizer, './models/privacy_vectorizer.pkl')
