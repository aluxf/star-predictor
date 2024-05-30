import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from celery import Celery

from numpy import loadtxt
import numpy as np
import sklearn
import joblib
import requests

def load_model():
    # load json and create model
    best_model = joblib.load('best_model.pkl')
    #print("Loaded model from disk")
    return best_model

def github_request(url):
    response = requests.get(
        url=url,
    )
    data = response.json()
    return data

def parse_repo(repo):
    return {
        "stars": repo['stargazers_count'],
        "forks": repo['forks_count'],
        "open_issues": repo['open_issues_count'],
        "topics_count": len(repo['topics']),
        "topics": repo['topics'],
        "disk_usage": repo["size"],
        "created_at": repo['created_at'],
        #"followers": None,
        #"following": None,
        #"public_repos": None
    }

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task()
def add_nums(a, b):
   return a + b

@celery.task
def get_predictions(repo_link):
    api_link = repo_link.replace('github.com', 'api.github.com/repos')
    repo = github_request(api_link)
    repo = parse_repo(repo)

    topics = repo["topics"]

    mlb = MultiLabelBinarizer()
    topics_transformed = mlb.fit_transform(topics)
    topics_df = pd.DataFrame(topics_transformed, columns=mlb.classes_)

    df = pd.DataFrame(repo).drop(columns=["topics"])
    df = pd.concat([df, topics_df], axis=1)
    date = pd.to_datetime(df['created_at'])
    df['created_at'] = date.dt.year
    s = StandardScaler()
    y = df['stars']
    X = df.drop(columns=['stars'])

    X = s.fit_transform(X)

    model = load_model()
    results = model.predict(X)
    print(results)
    return results[0], y[0]

