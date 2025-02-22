import joblib


def load_privacy(conv):
    input = [conv]
    model = joblib.load('./models/privacy_model.pkl')
    vectorizer = joblib.load('./models/privacy_vectorizer.pkl')
    X_new_vec = vectorizer.transform(input)
    new_pred = model.predict(X_new_vec)
    print("Predicted label:", new_pred[0])
    return new_pred[0]

def load_profanity(data):
    model = joblib.load('./models/profanity_model.pkl')
    vectorizer = joblib.load('./models/profanity_vectorizer.pkl')
    for convo in data:
        speaker = convo.get('speaker')
        text = convo.get('text')
        if speaker == 'Agent':
            X_new_vec = vectorizer.transform([text])
            new_pred = model.predict(X_new_vec)
            if new_pred[0]:
                return 'Agent'
        if speaker == 'Customer':
            X_new_vec = vectorizer.transform([text])
            new_pred = model.predict(X_new_vec)
            if new_pred[0]:
                return 'Customer'
    return ''