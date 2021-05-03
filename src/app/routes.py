from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'User'}
    return render_template('index.html', user=user)

@app.route('/analysis')
def analysis():
    user = {'username': 'User'}
    return render_template('analysis.html', user=user)

@app.route('/recommendation')
def recommendation():
    user = {'username': 'User'}
    return render_template('recommendation.html', user=user)