from flask_mail import Mail, Message

class FlaskMail:
    def __init__(self):
        self.mail = Mail()
        self.user = None

    def send_mail(self, subject, recipients, body):
        try:
            msg = Message(subject=subject,
                          sender=self.user,
                          recipients=recipients,
                          body=body)
            self.mail.send(msg)
            return True
        except:
            return False

m = FlaskMail()

def init_app(app):
    m.user = app.config.MAIL_USERNAME
    m.mail.init_app(app)
