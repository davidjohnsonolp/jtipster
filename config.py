# -*- coding: UTF-8 -*-

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess-07796'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# import io
IMPORT_IO_GUID = "d133b9b6-1253-4568-b727-425c7181ed93"
IMPORT_IO_API_KEY = "xCSj76J7NK+PaXi5foAzbIjgyo+Y+Xpu1+oS+OpngOor8gYN/johObwTLAUaQSoGTGzmSCxVMJQU3mXbICU6SQ=="

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'davidj.skyscanner@gmail.com'
MAIL_PASSWORD = 'Numark1ne!'

# administrator list
ADMINS = ['davidj@skyscanner.net']

# leagues
LEAGUES = [
            {
                 "id": 10001,
                 "soccerway_id": "PRL",
                 "name": "English Premier League",
                 "url": "http://uk.soccerway.com/national/england/premier-league/20162017/regular-season/r35992/",
                 "enabled": True
            },
            {
                 "id": 10002,
                 "soccerway_id": "CHA",
                 "name": "English Championship",
                 "url": "http://uk.soccerway.com/national/england/championship/20162017/regular-season/r36638/",
                 "enabled": True
            },
            {
                 "id": 10003,
                 "soccerway_id": "LEO",
                 "name": "English League One",
                 "url": "http://uk.soccerway.com/national/england/league-one/20162017/regular-season/r36641/",
                 "enabled": True
            },
            {
                 "id": 10004,
                 "soccerway_id": "LET",
                 "name": "English League Two",
                 "url": "http://uk.soccerway.com/national/england/league-two/20162017/regular-season/r36644/",
                 "enabled": True
            },
            {
                 "id": 10005,
                 "soccerway_id": "CON",
                 "name": "English National Conference",
                 "url": "http://uk.soccerway.com/national/england/conference-national/20162017/regular-season/r35949/",
                 "enabled": True
            },
            {
                 "id": 10006,
                 "soccerway_id": "PRE",
                 "name": "Scottish Premier League",
                 "url": "http://uk.soccerway.com/national/scotland/premier-league/20162017/1st-phase/r35877/",
                 "enabled": True
            },
            {
                 "id": 10007,
                 "soccerway_id": "CHA",
                 "name": "Scottish Championship",
                 "url": "http://uk.soccerway.com/national/scotland/first-division/20162017/regular-season/r35425/",
                 "enabled": True
            },
            {
                 "id": 10009,
                 "soccerway_id": "SEA",
                 "name": "Italian Serie A",
                 "url": "http://uk.soccerway.com/national/italy/serie-a/20162017/regular-season/r36003/",
                 "enabled": True
            },
            {
                 "id": 10010,
                 "soccerway_id": "SEB",
                 "name": "Italian Serie B",
                 "url": "http://uk.soccerway.com/national/italy/serie-b/20162017/regular-season/r37192/",
                 "enabled": True
            },
            {
                 "id": 10011,
                 "soccerway_id": "PRD",
                 "name": "Spanish Primera División",
                 "url": "http://uk.soccerway.com/national/spain/primera-division/20162017/regular-season/r35880/",
                 "enabled": True
            },
            {
                 "id": 10012,
                 "soccerway_id": "SED",
                 "name": "Spanish Segunda División",
                 "url": "http://uk.soccerway.com/national/spain/segunda-division/20162017/regular-season/r37748/",
                 "enabled": True
            },
            {
                 "id": 10013,
                 "soccerway_id": "BUN",
                 "name": "German Bundesliga",
                 "url": "http://uk.soccerway.com/national/germany/bundesliga/20162017/regular-season/r35823/",
                 "enabled": True
            },
            {
                 "id": 10014,
                 "soccerway_id": "2.B",
                 "name": "2. German Bundesliga",
                 "url": "http://uk.soccerway.com/national/germany/2-bundesliga/20162017/regular-season/r35824/",
                 "enabled": True
            },
            {
                 "id": 10015,
                 "soccerway_id": "LI1",
                 "name": "French Ligue 1",
                 "url": "http://uk.soccerway.com/national/france/ligue-1/20162017/regular-season/r35879/",
                 "enabled": True
            },
            {
                 "id": 10016,
                 "soccerway_id": "LI2",
                 "name": "French Ligue 2",
                 "url": "http://uk.soccerway.com/national/france/ligue-2/20162017/regular-season/r35875/",
                 "enabled": True
            },
            {
                 "id": 10017,
                 "soccerway_id": "ERE",
                 "name": "Dutch Eredivisie",
                 "url": "http://uk.soccerway.com/national/netherlands/eredivisie/20162017/regular-season/r36385/",
                 "enabled": True
            },
            {
                 "id": 10018,
                 "soccerway_id": "PRL",
                 "name": "Portuguese Primera Liga",
                 "url": "http://uk.soccerway.com/national/portugal/portuguese-liga-/20162017/regular-season/r35881/",
                 "enabled": True
            },
            {
                 "id": 10019,
                 "soccerway_id": "PRL",
                 "name": "Belgian Pro League",
                 "url": "http://uk.soccerway.com/national/belgium/pro-league/20162017/regular-season/r36668/",
                 "enabled": True
            },
            {
                 "id": 10020,
                 "soccerway_id": "SUL",
                 "name": "Greek Super League",
                 "url": "http://uk.soccerway.com/national/greece/super-league/20162017/regular-season/r36670/",
                 "enabled": True
            },
            {
                 "id": 10021,
                 "soccerway_id": "ALL",
                 "name": "Swedish Allsvenskan",
                 "url": "http://uk.soccerway.com/national/sweden/allsvenskan/2014/regular-season/r23311/",
                 "enabled": False
            },
            {
                 "id": 10022,
                 "soccerway_id": "SUP",
                 "name": "Swedish Superettan",
                 "url": "http://uk.soccerway.com/national/sweden/superettan/2014/regular-season/r23312/",
                 "enabled": False
            },
            {
                 "id": 10023,
                 "soccerway_id": "SUP",
                 "name": "Danish Superliga",
                 "url": "http://uk.soccerway.com/national/denmark/superliga/20142015/regular-season/r25425/",
                 "enabled": False
            },
            {
                 "id": 10024,
                 "soccerway_id": "ELI",
                 "name": "Norwegian Eliteserien",
                 "url": "http://uk.soccerway.com/national/norway/eliteserien/2014/regular-season/r23260/",
                 "enabled": False
            },
            {
                 "id": 10025,
                 "soccerway_id": "VEI",
                 "name": "Finnish Veikkausliiga",
                 "url": "http://uk.soccerway.com/national/finland/veikkausliiga/2014/regular-season/r23927/",
                 "enabled": False
            }
]