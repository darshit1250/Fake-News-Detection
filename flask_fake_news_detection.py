# -*- coding: utf-8 -*-
"""flask_fake_news_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16-_wfdNbJqLNX3fGYOe8mLQ-lhNqsg2R
"""

import nltk
import re
nltk.download(['punkt','stopwords'])

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

wl = WordNetLemmatizer()
ps = PorterStemmer()

def make_corpus(title, text):
  corpus=[]
  review = re.sub('[^a-zA-Z]', ' ', title+text)
  review = review.lower()
  review = review.split()
  review = [ps.stem(words) for words in review if not words in stopwords.words('english')]
  review = ' '.join(review)
  corpus.append(review)
  return corpus

import pickle
from keras.models import load_model
pickle_in = open('logistic.pkl','rb')
classifier = pickle.load(pickle_in)
pickle_in.close()

pickle_tf = open('tfidf.pkl','rb')
tfidf = pickle.load(pickle_tf)
pickle_tf.close()

pickle_tokenizer = open('tokenizer.pkl', 'rb')
tokenizer_obj = pickle.load(pickle_tokenizer)
pickle_tokenizer.close()

pickle_naive = open('naive_bayes.pkl', 'rb')
classifier_NB = pickle.load(pickle_naive)
pickle_naive.close()

pickle_random = open('random_forest.pkl', 'rb')
classifier_RF = pickle.load(pickle_random)
pickle_random.close()

pickle_aggresive = open('passive_agressive_classifier.pkl', 'rb')
classifier_PA = pickle.load(pickle_aggresive)
pickle_aggresive.close()

classifier_LSTM = load_model('fake_news_lstm.h5')

def corpus_to_tfidf(corpus):
  tfidf_vector = tfidf.transform(corpus)
  return tfidf_vector


from keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, render_template
import pickle


app = Flask(__name__)

@app.route("/")
def hello():
  return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
  title = request.form['title']
  text = request.form['content']
  algo = request.form['algo']
  corpus = make_corpus(title,text)
  tfidf_vector = corpus_to_tfidf(corpus)
  corpus_token = tokenizer_obj.texts_to_sequences(corpus)
  embedded_doc = pad_sequences(corpus_token, maxlen=100)
  float_formatter = "{:.2f}".format
  if algo == 'naive_bayes':
    result_NB = classifier_NB.predict_proba(tfidf_vector)
    print(result_NB)
    result_str = "<h3>Using Naive Bayes : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter(result_NB[0][0]*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_NB[0][1]*100)) + "%"
    print(result_str)
    return result_str
  elif algo == 'logistic':
    result_LR = classifier.predict_proba(tfidf_vector)
    print(result_LR)
    return "<h3>Using Logistic Regression : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter(result_LR[0][0]*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_LR[0][1]*100)) + "%"
  elif algo == 'passive_agressive':
    result_PA = classifier_PA.predict(tfidf_vector)
    print(result_PA)
    return "<h3>Using Passive Agressive Classifier : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter((1-result_PA[0])*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_PA[0]*100)) +"%"
  elif algo == 'random_forest':
    result_RF = classifier_RF.predict_proba(tfidf_vector)
    return "<h3>Using Random Forest : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter(result_RF[0][0]*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_RF[0][1]*100)) + "%"
  elif algo == 'lstm':
    result_LSTM = classifier_LSTM.predict_proba(embedded_doc)
    print(result_LSTM)
    return "<h3>Using LSTM : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter((1 - result_LSTM[0][0])*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_LSTM[0][0]*100)) + "%" + "<p style='color:red;'>(Due to low computational power we've only used Title to train the LSTM! </br> Hence it might not give accurate result for whole News)</p>"
  else:
    result_NB = classifier_NB.predict_proba(tfidf_vector)
    result_LR = classifier.predict_proba(tfidf_vector)
    result_PA = classifier_PA.predict(tfidf_vector)
    result_RF = classifier_RF.predict_proba(tfidf_vector)
    result_LSTM = classifier_LSTM.predict_proba(embedded_doc)
    result_str = "<h3>Using Naive Bayes : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter(result_NB[0][0]*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_NB[0][1]*100)) + "%</br><h3>Using Logistic Regression : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter(result_LR[0][0]*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_LR[0][1]*100)) + "%</br><h3>Using Passive Agressive Classifier</h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter((1-result_PA[0])*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_PA[0]*100)) +"%" + "</br><h3>Using Random Forest : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter(result_RF[0][0]*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_RF[0][1]*100)) + "%</br><h3>Using LSTM : </h3>" + "</br>The probability of the News being Reliable is : " + str(float_formatter((1 - result_LSTM[0][0])*100)) + "%</br>The probability of the News being Fake is : " + str(float_formatter(result_LSTM[0][0]*100)) + "%" + "<p style='color:red;'>(Due to low computational power we've only used Title to train the LSTM! </br> Hence it might not give accurate result for whole News)</p>"
    return result_str



if __name__=='__main__':
  app.run()