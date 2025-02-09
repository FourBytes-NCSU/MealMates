from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from models.provider import Provider
from models.receiver import Receiver

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/provider/login', methods=['POST'])
def provider_login():
    data = request.json
    provider = Provider.query.filter_by(username=data.get('username'), password=data.get('password')).first()

    if provider:
        login_user(provider)
        return jsonify({"message": "Provider login successful!", "role": "provider"}), 200

    return jsonify({"error": "Invalid provider credentials"}), 401

@auth_bp.route('/receiver/login', methods=['POST'])
def receiver_login():
    data = request.json
    receiver = Receiver.query.filter_by(username=data.get('username'), password=data.get('password')).first()

    if receiver:
        login_user(receiver)
        return jsonify({"message": "Receiver login successful!", "role": "receiver"}), 200

    return jsonify({"error": "Invalid receiver credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200
