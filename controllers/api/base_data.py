import re
from flask import request, jsonify, session

def inject_controller(app):

    @app.route('/api/get_authenticated_user', methods=['GET'])
    @app.auth.authentication_required()
    def api_get_authenticated_user():
        username = app.auth.get_authenticated_user()['username']
        return jsonify({"username": username, "status": 200}), 200