import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.shortcuts import render
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from spam_detection.forms import FormData

# ===========Helper function============
def Preprocess(text):
    #Remove punctations & numbers
    text = re.sub(r"[^a-zA-Z]", " ", text)
    
    #tokenize sentence into words 
    words = word_tokenize(text)
    
    #Remove stopwords
    stop_words=set(stopwords.words("english"))
    words=[word for word in words if word not in stop_words]
    
    return words

def home_view(request):
    return render(request, 'index.html')


def predict_spam(request):
    context = {}

    if request.method == 'POST':
        form = FormData(request.POST)

        model_path = os.path.abspath('trainedModels')
        # print(model_path)

        # ======== Ensure form is not empty =======
        if form.is_valid():
            # ========Import the saved model=========
            load_classifier = joblib.load('/home/goodisoft/Documents/Dev/email_spam_detection/trainedModels/classifier_model.pkl')
            load_vectorizer = joblib.load('/home/goodisoft/Documents/Dev/email_spam_detection/trainedModels/email_vectorizer.pkl')

            processed_email = Preprocess(form.cleaned_data['email_content'])

            # ============Check spam==========
            vc_email = load_vectorizer.transform(processed_email)
            prediction = load_classifier.predict(vc_email)
            print(prediction)

            # ========0- no spam, 1 - spam=======
            if prediction[0] == 1:
                context['prediction'] = 'Spam'
            else:
                context['prediction'] = 'Not Spam'

        else:
            context['form'] = form
    else:
        form = FormData()
        context['form'] = form

    return render(request, 'index.html', context)