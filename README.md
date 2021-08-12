# Fake News Detection
  This NLP project is still in initial stage. I've completed the EDA part of the project and working on it.
  
# Overview
  News media has gotten to be a channel to pass on the data of what’s happening within the world to the individuals living. Regularly people perceive anything passed on within the news to be genuine. There were circumstances where even the news channels recognized that their news isn't genuine as they composed. But a few news incorporates a noteworthy affect not as it were on the individuals or government but too on the economy.
  
  The data science community has reacted by taking activity to battle the issue. There’s a Kaggle-style competition called the “Fake News” and numerous social media platform using AI to channel fake news stories out of users’ nourishes.

# Problem Statement
  One news can move the bends up and down depending on the feelings of individuals and political situation. The issue isn't as it were programmers, going into accounts, and sending untrue data. The greater issue here is what we call “Fake News”. A fake are those news stories that are wrong: the story itself is manufactured, with no unquestionable realities, sources, or cites.
  
# Objectives:
  1.	Our sole objective is to classify the news from the dataset as fake or true news.
  2.	Extensive EDA of news.
  3.	Selecting and building a powerful model.
  4.	Using the model to classify the news.

# Data Set Source
  * https://www.kaggle.com/c/fake-news/data

# Files overview
  * FakeNewsClassifier_Capstone_Project_whole_text.ipynb
    * EDA has been performed on the dataset.
    * Then we removed data with other languages than English as we found different languages using detectTheLanguageAndAppendInCSV.ipynb.
    * TF-IDF vectorizer has been used to generate data that can be fed to the machine.
    * Fitted all total of 5 algorithm (Naive bayes, Passive Aggressive Classifier, Logistic Regression, Random Forest, and LSTM).
    * Dumped all the necessary .pkl files of the objects (tfidf, tokenizer) and models (all).
  * detectTheLanguageAndAppendInCSV.ipynb
    * After generating word cloud we found that english is not the only language used in the dataset, so we wrote a code to detect the language used and diversify the dataset. For this we added one column named 'Language' in the dataset and set it by default to 'e'. Now we used nltk library - more specifically TextCat - to identify the language and replaced the newly created column values.
  * merge_language.ipynb
    * So, the 20800 rows were diveded into 4 parts and processed to identify the language.
    * This file merges all 4 parts into one and adds one column at the end of the dataset named "Language"
  * flask_fake_news_detection.py
    * This file has the API code using flask.
    * It has the routes ("/", "/predict" POST) to handle queries from user.
    * In "/predict" route, it handles users input and performs pre-processing on it.
    * It transforms the preprecessed text into TF-IDF vectors that will be passed to particular model for prediction.
  * requirements.txt
    * All the required libraries are mentioned with the versions.
  * Pickle/model files
    1. tfidf.pkl
    2. tokenizer.pkl
    3. naive_bayes.pkl
    4. passive_agressive_classifier.pkl
    5. random_forest.pkl
    6. logistic.pkl
    7. fake_news_lstm.h5
  * Procfile
    * This file has the command to run the application on heroku.

# Liberaries used in the project
  * ScikitLearn (https://github.com/scikit-learn/scikit-learn)
  * MatplotLib (https://github.com/matplotlib/matplotlib)
  * NumPy (https://github.com/numpy/numpy)
  * wordcloud (https://github.com/amueller/word_cloud)
  * nltk (https://github.com/nltk/nltk)
  * Flask (https://github.com/pallets/flask)
  * pickleshare (https://github.com/pickleshare/pickleshare)
  * regex (https://github.com/ziishaned/learn-regex)
  * gunicorn (https://github.com/benoitc/gunicorn)
  * pip-tools (https://github.com/jazzband/pip-tools)
