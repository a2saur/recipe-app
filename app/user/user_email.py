from flask_mail import Message
from app import mail
from flask import render_template, current_app

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_verification_email(user, code):
    send_email('[MealPlanner] Verification Code',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body="",
               html_body=render_template('certify_email.html',
                                         user=user, code=code))