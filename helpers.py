from flask import request
import matplotlib.pyplot as plt
import os
import datetime as dt


from score_db import score_db
from config import config
from games import game_dict


def generate_chart(game_type):
    df_scores = score_db.get_scores(game_type)
    today = dt.datetime.today().date()

    plt.figure(figsize=(10, 5))

    # Initialize the plot
    for i in range(1, len(df_scores)):
        # Determine the color based on the date of the current and previous point
        if df_scores["date"].iloc[i].date() == today and df_scores["date"].iloc[i - 1].date() == today:
            color = config["THEME_COLOR"]
        else:
            color = 'black'

        # Plot line segment
        plt.plot(df_scores["date"].iloc[i - 1:i + 1], df_scores["score"].iloc[i - 1:i + 1], marker='o', color=color)

    plt.xlabel('Date')
    plt.ylabel('Score')
    plt.title(f'Scores Over Time for {game_type.pretty_name}')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = os.path.join('static', 'temp', f'{game_type}_chart.png')
    if not os.path.exists(os.path.dirname(chart_path)):
        os.makedirs(os.path.dirname(chart_path))
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def get_active_game():
    default_game_var = list(game_dict.keys())[0]
    active_game = request.args.get('active_game', default_game_var)
    return game_dict[active_game]
