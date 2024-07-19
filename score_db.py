import csv
import datetime as dt
from flask import session
from functools import wraps
import pandas as pd
import os

def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class ScoreDB:
    scores_path = "data/scores.csv"

    def __init__(self):
        self.df_scores = self.load_scores()

    def load_scores(self):
        # Create file if not there
        if not os.path.isfile(self.scores_path):
            with open(self.scores_path, mode='a') as file:
                writer = csv.writer(file)
                writer.writerow(["game", "score", "date"])

        df = pd.read_csv(self.scores_path)
        df["date"] = pd.to_datetime(df["date"])
        return df


    def save_score(self, game, score):
        row = [game, score, dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]

        with open('data/scores.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        self.df_scores = pd.concat([self.df_scores,
                                    pd.DataFrame([row], columns=self.df_scores.columns)
                                    ],
                                   ignore_index=True)
        self.df_scores["date"] = pd.to_datetime(self.df_scores["date"])

    def get_scores(self, game=None):
        df = self.df_scores.copy()
        if game is not None:
            df = df[df["game"] == str(game)]
        return df

    def get_high_scores(self, game):
        df = self.get_scores(game)
        df = df.sort_values("score", ascending=False).head(5)

        # Get time from date
        date_today = dt.datetime.now()
        df["date"] = (df["date"] - date_today).dt.days
        df["date"] = df["date"].apply(lambda x: f"{abs(x)} days ago")

        # Clean
        df = df.drop(columns=["game"])
        while len(df) < 5:
            df = pd.concat([df,
                            pd.DataFrame([["", ""]], columns=df.columns)
                            ],
                           ignore_index=True)

        return df.to_dict(orient='records')


    '''Current Score'''

    def get_current_score(self):
        return session.get('current_score', 0)

    # Increment the score in the session or database
    def increment_score(self):
        if 'current_score' in session:
            session['current_score'] += 1
        else:
            session['current_score'] = 1

    def reset_score(self):
        session['current_score'] = 0

score_db = ScoreDB()