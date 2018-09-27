import os
from datetime import datetime, timedelta
from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, models, login_manager, login_serializer, recaptcha
from config import LEAGUES
from models import User, Bet, Tip, BetTip
from email import registration_notification
from sqlalchemy import func
from importio import extractor
from tips import get_home_win_tips, get_away_win_tips, get_goals_over_tips


# Accounts
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.token_loader
def load_token(token):
    max_age = timedelta(days=14).total_seconds()
    data = login_serializer.loads(token, max_age=max_age)
    user = User.query.filter_by(username=data[0])

    if user and data[1] == user.password_hash:
        return user
    return None


@app.route('/api/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username}), 200

@app.route('/api/de-authenticate')
def deauthenticate():
    logout_user()
    return jsonify({}), 200

@app.route('/api/user', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    recaptcha_response = request.json.get('recaptcha')

    if username is None or password is None or email is None:
        abort(400)    # missing arguments

    if not recaptcha.confirm(recaptcha_response):
        abort(403)    # recaptcha forbidden

    if User.query.filter_by(username=username).first() is not None:
        abort(409)    # existing username

    if User.query.filter_by(email=email).first() is not None:
        abort(409)    # existing email

    user = User(username=username, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    registration_notification(username, email)

    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    remember_me = request.json.get('remember_me')
    user = User.query.filter_by(username=username).first()

    if user is None or not user.verify_password(password):
        abort(401)

    login_user(user, remember=remember_me)

    return jsonify({'username': user.username}), 200, {'Location': url_for('get_user', id=user.id, _external=True)}


#Bets
@app.route('/api/bet', methods=['GET'])
@login_required
def bet_get():
    bets = Bet.query.filter_by(user_id=current_user.get_id()).all()
    result = []
    for b in bets:
        item = {col: getattr(b, col) for col in Bet.json_attributes}
        item['lines'] = [{col: getattr(bt.tip, col) for col in Tip.json_attributes} for bt in b.lines.all()]
        result.append(item)

    return jsonify(bets=result)

@app.route('/api/bet', methods=['POST'])
@login_required
def bet_add():
    if not request.json or not 'stake' in request.json or len(request.json['lines']) == 0:
        abort(400)

    bet = Bet()
    bet.user_id = current_user.get_id()
    bet.stake = request.json['stake']
    bet.timestamp = datetime.utcnow()

    db.session.add(bet)
    db.session.commit()

    for line in request.json['lines']:
        bt = BetTip(bet_id=bet.id, tip_id=line['id'])
        db.session.add(bt)

    db.session.commit()

    return jsonify({'success': True})

@app.route('/api/bet/<int:id>', methods=['DELETE'])
@login_required
def bet_delete(id):
    bet = Bet.query.filter_by(id=id,user_id=current_user.get_id()).first()
    bet_exists = not bet is None

    if bet:
        db.session.delete(bet)
        db.session.commit()

    return jsonify({'success': bet_exists})


#Tips
@app.route('/api/tip', methods=['GET'])
def tips_get():
    if not is_admin():
        abort(403)

    tips = Tip.query.order_by(Tip.KickOff).all()
    result = [{col: getattr(t, col) for col in Tip.json_attributes} for t in tips]
    return jsonify(tips=result)

@app.route('/api/tip/<int:id>', methods=['PUT'])
@login_required
def tips_update(id):
    if not is_admin():
        abort(403)

    tip = Tip.query.filter_by(id=id).first()
    tip_exists = not tip is None

    if tip_exists:
        tip.MarketType = request.json['MarketType']
        tip.MarketParticipantType = request.json['MarketParticipantType']
        tip.MarketParticipantThreshold = request.json['MarketParticipantThreshold']
        tip.OddsDecimal = request.json['OddsDecimal']
        tip.Status = request.json['Status']

        db.session.add(tip)
        db.session.commit()

    return jsonify({'success': tip_exists})

@app.route('/api/tip/<int:id>', methods=['DELETE'])
@login_required
def tips_delete(id):
    if not is_admin():
        abort(403)

    tip = Tip.query.filter_by(id=id).first()
    tip_exists = not tip is None

    if tip:
        db.session.delete(tip)
        db.session.commit()

    return jsonify({'success': tip_exists})


#Predictions
@app.route('/api/predictions', methods=['GET'])
def predictions_get():
    tips = db.session.query(Tip).filter(Tip.Status == 1)\
                                .filter(func.datetime(Tip.KickOff) >= datetime.utcnow())\
                                .all()

    result = [{col: getattr(t, col) for col in Tip.json_attributes} for t in tips]
    return jsonify(predictions=result)


#Extract
@app.route('/api/leagues', methods=['GET'])
def extract_get():
    if not is_admin():
        abort(403)

    return jsonify(extracts=LEAGUES)

@app.route('/api/leagues/<int:id>', methods=['PUT'])
@login_required
def extract_league(id=0):
    if not is_admin():
        abort(403)

    league = [x for x in LEAGUES if x["id"] == id][0]
    url = league["url"]
    tips = []

    extractor.reset_data("fixture")
    extractor.reset_data("log")

    fixtures = [f for f in extractor.extract("fixture", [url]) if not get_kickoff(f) < datetime.utcnow()]
    history = extractor.extract("history",[h['hometeam'] + 'matches/' for h in fixtures] +
                                          [a['awayteam'] + 'matches/' for a in fixtures])

    for fixture in fixtures:
        #extractor.reset_data("history")

        home = fixture['hometeam/_title']
        away = fixture['awayteam/_title']
        league_id = league['soccerway_id']
        kickoff_time = get_kickoff(fixture)

        tips += get_home_win_tips(home, away, league_id, kickoff_time, history)
        tips += get_away_win_tips(home, away, league_id, kickoff_time, history)
        tips += get_goals_over_tips(home, away, league_id, kickoff_time, history)


    for tip in tips:
        if db.session.query(Tip).filter(Tip.HomeTeamName == tip.HomeTeamName) \
                                .filter(Tip.AwayTeamName == tip.AwayTeamName) \
                                .filter(Tip.KickOff == tip.KickOff) \
                                .filter(Tip.MarketType == tip.MarketType).first() is None:
            db.session.add(tip)

    db.session.commit()

    result = [{col: getattr(t, col) for col in Tip.json_attributes} for t in tips]
    return jsonify(predictions=result, log=extractor.data["log"])

def get_kickoff(fixture):
    if 'kickoff' in fixture:
        time = [int(x) for x in fixture['kickoff'].split(':')]
        return datetime.fromtimestamp(fixture['date'] / 1000).replace(hour=time[0] - 1, minute=time[1])
    return datetime.min

def is_admin():
    return current_user.username == "DJ" # fix this