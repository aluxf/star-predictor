import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import requests


# Fetch the data

GITHUB_TOPREPO_URL = lambda page: f"https://api.github.com/search/repositories?q=stars:%3E50&sort=stars&page={page}&per_page=100"
GITHUB_RATELIMIT_URL = 'https://api.github.com/rate_limit'

def github_request(url):
    response = requests.get(
        url=url,
        headers={
            f"Authorization": "Token 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"
        }
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
        "owner_url": repo['owner']['url'],
        #"followers": None,
        #"following": None,
        #"public_repos": None
    }

def create_dataset(save_path=None):
    all_repos = []
    # 100 Repos per page
    for i in range(1, 11):
        # Fetch the data
        repos = github_request(GITHUB_TOPREPO_URL(i))['items']
        parsed_repos = [parse_repo(repo) for repo in repos]
        all_repos.extend(parsed_repos)

    #for repo in all_repos:
    #    data = github_request(repo['owner_url'])
    #    repo['followers'] = data['followers']
    #    repo['following'] = data['following']
    #    repo['public_repos'] = data['public_repos']
        
    topics = [repo["topics"] for repo in all_repos]

    mlb = MultiLabelBinarizer()
    topics_transformed = mlb.fit_transform(topics)
    topics_df = pd.DataFrame(topics_transformed, columns=mlb.classes_)

    df = pd.DataFrame(all_repos).drop(columns=["topics", "owner_url"])
    df = pd.concat([df, topics_df], axis=1)
    date = pd.to_datetime(df['created_at'])
    df['created_at'] = date.dt.year
    if save_path:
        df.to_csv(save_path, index=False)
    return df

