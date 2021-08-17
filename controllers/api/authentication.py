import re
from flask import request, jsonify, session

def inject_controller(app):

    @app.route('/api/auth', methods=['POST'])
    def auth():
        if not request.form.get('username') or not request.form.get('password'):
            return jsonify({"message": "Credentials required", "status": 400}), 400
        dbSession = app.db.create_session()
        user = dbSession.query(app.User).filter(
            app.User.iduser == request.form.get('username').lower()).first()
        dbSession.close()
        if user:
            if app.auth.decrypt(user.cypher) == request.form.get('password'):
                payload = {
                    "username": request.form.get('username').lower()
                }
                session['auth_token'] = app.auth.create_jwt(payload)
                return jsonify({"message": "Authentication successful", "status": 200}), 200
        return jsonify({"message": "Invalid credentials", "status": 401}), 401

    @app.route('/api/logout', methods=['GET'])
    def logout():
        session.clear()
        return jsonify({"message": "Logout successful", "status": 200}), 200

    @app.route('/api/register', methods=['POST'])
    def api_register():
        if not request.form.get('username') or not request.form.get('email') or not request.form.get('password') or not request.form.get('confirmPassword'):
            return jsonify({"message": "Input data missing", "status": 400}), 400
        if request.form.get('password') != request.form.get('confirmPassword'):
            return jsonify({"message": "Password confirmation failed", "status": 400}), 400
        email_mask = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_mask, request.form.get('email')):
            return jsonify({"message": "Invalid input email format", "status": 400}), 400
        dbSession = app.db.create_session()
        user = dbSession.query(app.User).filter(
            app.User.iduser == request.form.get('username').lower()).first()
        if user:
            dbSession.close()
            return jsonify({"message": "Username already exists", "status": 400}), 400
        user = app.User(
            iduser = request.form.get('username').lower(),
            email = request.form.get('email'),
            cypher = app.auth.crypt(request.form.get('password'))
        )
        try:
            dbSession.add(user)
            dbSession.commit()
        except Exception as e:
            return jsonify({"message": "Unable to complete registration", "status": 500}), 500
        finally: 
            dbSession.close()
        payload = {
                    "username": request.form.get('username').lower()
                }
        session['auth_token'] = app.auth.create_jwt(payload)
        return jsonify({"message": "Registration successful", "status": 200}), 200