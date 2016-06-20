from . import mail
from flask.ext.mail import Message
from threading import Thread
from flask import render_template, current_app

# async send email
def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kw):
    """to: email recesiver
        subject: email subject
        template: without endpoint
    """
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX']+subject, sender=app.config['FLASK_MAIL_SENDER']
                  , recipients=[to])
    msg.body = render_template(template+'.txt', **kw)
    msg.html = render_template(template+".html", **kw)
    thr = Thread(target=send_mail_async, args=[app, msg])
    thr.start()
    return thr