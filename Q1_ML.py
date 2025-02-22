import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import joblib


df = pd.read_excel('profanity_calls.xlsx')

X = df['text']
y = df['label']

# Vectorize the text
vectorizer = TfidfVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(X)   # (number of documents, number of unique words)

# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Apply SMOTE to oversample the minority class  Synthetic Minority Over-sampling Technique
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Train your model with the balanced data
model = LogisticRegression()
model.fit(X_train_smote, y_train_smote)

# Evaluate your model on the test set
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
joblib.dump(model, './models/profanity_model.pkl')
joblib.dump(vectorizer, './models/profanity_vectorizer.pkl')
