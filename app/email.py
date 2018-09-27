from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from threading import Thread
from app import app

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def registration_notification(username, email):
    send_email("Welcome %s!" % username,
               ADMINS[0],
               [email],
               render_template("email/registration.txt", username=username),
               render_template("email/registration.html", username=username))