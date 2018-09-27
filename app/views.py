from flask import render_template, g
from flask.ext.login import current_user, login_required

from app import app

@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html',
                           title='Home',
                           styles=['/static/css/index.css'],
                           scripts=['//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-539f422908b31527'])

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html', scripts=['/static/js/register.js',
                                                     '/static/js/initialise/register.js',
                                                     'https://www.google.com/recaptcha/api.js'])

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', scripts=['/static/js/login.js', '/static/js/initialise/login.js'])

@app.route('/predictions', methods=['GET'])
def predictions():
    return render_template('predictions.html',
                           title='Predictions',
                           styles=['/static/css/predictions.css'],
                           scripts=['//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-539f422908b31527',
                                    '/static/js/selections.js',
                                    '/static/js/bet.js',
                                    '/static/js/prediction-model.js',
                                    '/static/js/prediction-view.js',
                                    '/static/js/initialise/prediction.js'])

@app.route('/extract', methods=['GET'])
@login_required
def extract():
    return render_template('extract.html',
                           title='Data Extract',
                           styles=['/static/css/extract.css'],
                           scripts=['/static/js/extract.js',
                                    '/static/js/initialise/extract.js'])

@app.route('/tips', methods=['GET'])
@login_required
def tips():
    return render_template('tips.html',
                           title='Tips Administration',
                           styles=['/static/css/tips.css'],
                           scripts=['/static/js/tips.js',
                                    '/static/js/initialise/tips.js'])

@app.route('/mybets', methods=['GET'])
@login_required
def my_bets():
    return render_template('bets.html',
                           title='My Bets',
                           scripts=['/static/js/prediction-model.js',
                                    '/static/js/bet.js',
                                    '/static/js/initialise/bet.js'])