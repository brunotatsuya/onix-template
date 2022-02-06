import hmac
import hashlib
import base64
import json
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from flask import jsonify, session, url_for, redirect, abort

def inject_service(app):

    @app.service('auth')
    class AuthenticationService():
        def __init__(self):
            self._SECRET_KEY = app.config_dict['SECRET_KEY']

        def crypt(self, token):
            f = Fernet(self._SECRET_KEY.encode("utf-8"))
            cypher = f.encrypt(token.encode("utf-8")).decode("utf-8")
            return cypher

        def decrypt(self, cypher):
            f = Fernet(self._SECRET_KEY.encode("utf-8"))
            token = f.decrypt(cypher.encode("utf-8")).decode("utf-8")
            return token

        def create_jwt(self, custom_payload, duration=None, custom_key=None):
            if duration:
                custom_payload['exp'] = (datetime.now() + timedelta(minutes=duration)).timestamp()
            payload = json.dumps(custom_payload).encode()
            header = json.dumps({
                'typ': 'JWT',
                'alg': 'HS256'
            }).encode()
            b64_header = base64.urlsafe_b64encode(header).decode()
            b64_payload = base64.urlsafe_b64encode(payload).decode()
            signature = hmac.new(
                key=custom_key.encode() if custom_key else self._SECRET_KEY.encode(),
                msg=f'{b64_header}.{b64_payload}'.encode(),
                digestmod=hashlib.sha256
            ).digest()
            jwt = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
            return jwt

        def validate_jwt(self, jwt, custom_key=None):
            b64_header, b64_payload, b64_signature = jwt.split('.')
            b64_signature_checker = base64.urlsafe_b64encode(
                hmac.new(
                    key=custom_key.encode() if custom_key else self._SECRET_KEY.encode(),
                    msg=f'{b64_header}.{b64_payload}'.encode(),
                    digestmod=hashlib.sha256
                ).digest()
            ).decode()
            payload = json.loads(base64.urlsafe_b64decode(b64_payload))
            unix_time_now = datetime.now().timestamp()
            if payload.get('exp') and payload['exp'] < unix_time_now:
                raise Exception('Expired token')
            if b64_signature_checker != b64_signature:
                raise Exception('Invalid signature')
            return payload

        def is_authenticated(self):
            if not session.get('auth_token'):
                return False
            try:
                self.validate_jwt(session['auth_token'])
            except:
                return False
            return True

        def get_authenticated_user(self):
            if not session.get('auth_token'):
                return None
            try:
                payload = self.validate_jwt(session['auth_token'])
            except:
                return None
            return payload      

        def authentication_required(self, role=None, redir=False):
            def wrapper(route_function):
                def decorated_function(*args, **kwargs):
                    if not self.is_authenticated():
                        if redir:
                            return redirect(url_for('login'))
                        else:
                            return jsonify({"message": "Authentication required", "status": 401}), 401
                    elif role:
                        if role not in self.get_authenticated_user()['roles']:
                            if redir:
                                abort(404, description="Not Found")
                            else:
                                return jsonify({"message": "Authorization required", "status": 403}), 403
                    return route_function(*args, **kwargs)
                decorated_function.__name__ = route_function.__name__
                return decorated_function
            return wrapper
