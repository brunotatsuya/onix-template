import re
from flask import request, jsonify, session

def inject_controller(app):

    def validate_email_mask(email):
        EMAIL_MASK = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.fullmatch(EMAIL_MASK, request.form.get('email'))

    @app.route('/api/auth', methods=['POST'])
    def api_auth():
        if not request.form.get('login') or not request.form.get('password'):
            return jsonify({"message": "Credentials required", "status": 400}), 400

        dbSession = app.db.create_session()
        user = dbSession.query(app.User).filter(
            app.User.username == request.form.get('login').lower()).first()
        if not user:
            user = dbSession.query(app.User).filter(
                app.User.email == request.form.get('login').lower()).first()

        if user:
            if app.auth.decrypt(user.cypher) == request.form.get('password'):
                payload = {
                    "username": user.username,
                    "roles": ["admin"]
                }
                session['auth_token'] = app.auth.create_jwt(payload)
                dbSession.close()
                return jsonify({"message": "Authentication successful", "status": 200}), 200

        dbSession.close()
        return jsonify({"message": "Invalid credentials", "status": 400}), 400

    @app.route('/api/logout', methods=['GET'])
    def api_logout():
        session.clear()
        return jsonify({"message": "Logout successful", "status": 200}), 200

    @app.route('/api/register', methods=['POST'])
    def api_register():
        if not request.form.get('username') or not request.form.get('email') or not request.form.get('password') or not request.form.get('confirmPassword'):
            return jsonify({"message": "Please, fill all fields", "status": 400}), 400

        dbSession = app.db.create_session()
        user = dbSession.query(app.User).filter(
            app.User.username == request.form.get('username').lower()).first()

        if user:
            dbSession.close()
            return jsonify({"message": "Username already exists", "status": 400}), 400

        if not validate_email_mask(request.form.get('email')):
            dbSession.close()
            return jsonify({"message": "Invalid input email format", "status": 400}), 400

        email_user = dbSession.query(app.User).filter(
            app.User.email == request.form.get('email').lower()).first()
        if email_user:
            dbSession.close()
            return jsonify({"message": "Email is already associated with another account", "status": 400}), 400

        if request.form.get('password') != request.form.get('confirmPassword'):
            dbSession.close()
            return jsonify({"message": "Passwords don't match", "status": 400}), 400

        user = app.User(
            username = request.form.get('username').lower(),
            email = request.form.get('email').lower(),
            cypher = app.auth.crypt(request.form.get('password'))
        )

        try:
            dbSession.add(user)
            dbSession.commit()
            payload = {
                    "username": user.username
            }
            session['auth_token'] = app.auth.create_jwt(payload)    
        except Exception as e:
            return jsonify({"message": "Unable to complete registration", "status": 500}), 500
        finally: 
            dbSession.close()

        return jsonify({"message": "Registration successful", "status": 200}), 200

    @app.route('/api/request_password_reset', methods=['POST'])
    def api_request_password_reset():
        if not request.form.get('email'):
            return jsonify({"message": "Please, fill email field", "status": 400}), 400

        if not validate_email_mask(request.form.get('email')):
            return jsonify({"message": "Invalid input email format", "status": 400}), 400

        dbSession = app.db.create_session()

        user = dbSession.query(app.User).filter(
            app.User.email == request.form.get('email').lower()).first()

        if not user:
            dbSession.close()
            return jsonify({"message": "Provided email is not registered", "status": 400}), 400

        try:
            token = app.auth.create_jwt({"iduser": user.iduser}, duration=60, custom_key=user.cypher)
            app.mail.send_mail('Password Reset', f'https://127.0.0.1:5000/reset_password/{user.iduser}/{token}', user.email)
        except Exception as e:
            return jsonify({"message": "Failed to send password reset mail", "status": 500}), 500
        finally:
            dbSession.close()
        
        return jsonify({"message": "Password reset mail generated and sent", "status": 200}), 200

    @app.route('/api/perform_password_reset', methods=['POST'])
    def api_perform_password_reset():

        if not request.form.get('iduser'):
            return jsonify({"message": "Please, provide id of user", "status": 400}), 400

        if not request.form.get('token'):
            return jsonify({"message": "Please, provide token", "status": 400}), 400

        if not request.form.get('new_password'):
            return jsonify({"message": "Please, provide new password", "status": 400}), 400

        dbSession = app.db.create_session()

        user = dbSession.query(app.User).filter(app.User.iduser == request.form.get('iduser')).first()
        if not user:
            dbSession.close()
            return jsonify({"message": "Requested user is invalid", "status": 400}), 400

        try:
            payload = app.auth.validate_jwt(request.form.get('token'), custom_key=user.cypher)
        except Exception as e:
            dbSession.close()
            return jsonify({"message": "Provided token is invalid", "status": 400}), 400

        if int(payload['iduser']) != int(request.form.get('iduser')):
            dbSession.close()
            return jsonify({"message": "Divergence of requested user", "status": 400}), 400

        try:
            user.cypher = app.auth.crypt('123')
            dbSession.add(user)
            dbSession.commit()
        except Exception as e:
            return jsonify({"message": "Unable to complete password reset", "status": 500}), 500
        finally: 
            dbSession.close()

        return jsonify({"message": "Password reset successfully", "status": 200}), 200