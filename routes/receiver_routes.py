from flask import request, jsonify
from flask_login import login_user, login_required
from models.receiver import Receiver
from models import db
from . import receiver_bp

@receiver_bp.route('/receiver/register', methods=['POST'])
def register_receiver():
    data = request.json
    receiver = Receiver(
        username=data['username'],
        password=data['password'],
        name=data['name'],
        city=data['city']
    )
    db.session.add(receiver)
    db.session.commit()
    return jsonify({"message": "Receiver registered successfully!"}), 201

@receiver_bp.route('/receiver/login', methods=['POST'])
def login_receiver():
    data = request.json
    receiver = Receiver.query.filter_by(username=data['username'], password=data['password']).first()
    if receiver:
        login_user(receiver)
        return jsonify({"message": "Receiver login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401
