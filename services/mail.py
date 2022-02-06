from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

from werkzeug.exceptions import ExpectationFailed

def inject_service(app):

    @app.service('mail')
    class SMTPService():

        def __init__(self):
            self._MAIL_SERVER = app.config_dict['MAIL_SERVER']
            self._MAIL_PORT = app.config_dict['MAIL_PORT']
            self._MAIL_CREDENTIALS = os.environ.get('MAIL_CREDENTIALS')

        def send_mail(self, subject, message, to):
            try:
                server = smtplib.SMTP(f'{self._MAIL_SERVER}: {self._MAIL_PORT}')
                server.starttls()
                user, pwd = app.auth.decrypt(self._MAIL_CREDENTIALS).split(':')
                server.login(user, pwd)
            except Exception as e:
                raise RuntimeError(f'Failed to login into mail server: {e}')

            try:
                msg = MIMEMultipart()
                msg['From'] = user
                msg['Subject'] = subject
                msg['To'] = to
                message = message
                msg.attach(MIMEText(message, 'html'))
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            except Exception as e:
                raise RuntimeError(f'Failed to send mail to destination: {e}')
            finally:
                server.quit()
