from app import db, login_serializer
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    HomeTeamName = db.Column(db.String(50))
    AwayTeamName = db.Column(db.String(50))
    KickOff = db.Column(db.DateTime)
    MarketType = db.Column(db.Integer)
    MarketParticipantType = db.Column(db.Integer)
    MarketParticipantThreshold = db.Column(db.Float)
    OddsDecimal = db.Column(db.Float)
    LastUpdate = db.Column(db.DateTime, onupdate=datetime.utcnow)
    Status = db.Column(db.Integer)
    HomeMatches = db.Column(db.String(255))
    AwayMatches = db.Column(db.String(255))
    Competition = db.Column(db.String(3))
    usages = db.relationship('BetTip', backref='tip', lazy='dynamic', cascade="all, delete-orphan", passive_deletes=True)

    json_attributes = ['id',
                       'HomeTeamName',
                       'AwayTeamName',
                       'KickOff',
                       'MarketType',
                       'MarketParticipantType',
                       'MarketParticipantThreshold',
                       'OddsDecimal',
                       'Competition',
                       'HomeMatches',
                       'AwayMatches',
                       'Status']


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    bets = db.relationship('Bet', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def get_auth_token(self):
        data = [str(self.id), self.password_hash]
        return login_serializer.dumps(data)

    def __repr__(self):
        return '<User %r>' % self.username


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stake = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    lines = db.relationship('BetTip', backref='bet', lazy='dynamic', cascade="all, delete-orphan", passive_deletes=True)

    json_attributes = ['id', 'stake', 'timestamp']


class BetTip(db.Model):
    bet_id = db.Column(db.Integer, db.ForeignKey('bet.id', ondelete='CASCADE'), primary_key=True)
    tip_id = db.Column(db.Integer, db.ForeignKey('tip.id', ondelete='CASCADE'), primary_key=True)