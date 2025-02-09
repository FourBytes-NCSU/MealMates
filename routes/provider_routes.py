from flask import request, jsonify
from flask_login import login_user, login_required
from models.provider import Provider
from models import db
from . import provider_bp

@provider_bp.route('/provider/register', methods=['POST'])
def register_provider():
    data = request.json
    provider = Provider(
        username=data['username'],
        password=data['password'],
        name=data['name'],
        address=data['address'],
        city=data['city']
    )
    db.session.add(provider)
    db.session.commit()
    return jsonify({"message": "Provider registered successfully!"}), 201

@provider_bp.route('/provider/login', methods=['POST'])
def login_provider():
    data = request.json
    provider = Provider.query.filter_by(username=data['username'], password=data['password']).first()
    if provider:
        login_user(provider)
        return jsonify({"message": "Provider login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401
