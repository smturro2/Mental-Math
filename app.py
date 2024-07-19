from flask import Flask, render_template, request, redirect, url_for, jsonify
from score_db import score_db
from games import game_dict
from helpers import generate_chart, get_active_game
from config import config
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

"""PAGES"""


@app.route('/')
def home():
    active_game = get_active_game()
    # generate_chart(active_game)  # todo
    high_scores = score_db.get_high_scores(active_game)
    return render_template('home.html',
                           theme_color=config["THEME_COLOR"],
                           high_scores=high_scores,
                           active_game=active_game,
                           games=game_dict)

@app.route('/game')
def game():
    active_game = get_active_game()
    current_score = score_db.get_current_score()
    score_db.reset_score()
    total_time = 30

    question, correct_answer = active_game.generate_question()
    return render_template('game.html',
                           theme_color=config["THEME_COLOR"],
                           active_game=active_game,
                           current_score=current_score,
                           question=question, 
                           correct_answer=correct_answer,
                           total_time=total_time)

@app.route('/end')
def end():
    active_game = get_active_game()
    current_score = score_db.get_current_score()
    score_db.save_score(active_game, current_score)
    high_scores = score_db.get_high_scores(active_game)

    return render_template('end.html',
                           theme_color=config["THEME_COLOR"],
                           active_game=active_game,
                           current_score=current_score,
                           high_scores=high_scores)


"""API CALLS"""


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    answer = data['answer']
    correct_answer = data['correct_answer']

    was_correct = abs(correct_answer - answer) < 0.001
    if was_correct:
        score_db.increment_score()
        new_score = score_db.get_current_score()
    else:
        new_score = score_db.get_current_score()

    return jsonify(correct=was_correct, new_score=new_score)

@app.route('/get_new_question')
def get_new_question():
    active_game = get_active_game()
    question, correct_answer = active_game.generate_question()
    return jsonify({'question': question, 'correct_answer': correct_answer})



if __name__ == '__main__':
    app.run(debug=True)
