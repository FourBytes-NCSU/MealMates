from flask import request, jsonify
from flask_login import login_user, login_required, current_user
from models.receiver import Receiver
from models import db
from . import receiver_bp
from routes.order_routes import available_food
from models.order import Order

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

@receiver_bp.route('/receivers', methods=['GET'])
def get_receivers():
    receivers = Receiver.query.all()
    result = [
        {
            "id": receiver.id,
            "username": receiver.username,
            "name": receiver.name,
            "city": receiver.city
        }
        for receiver in receivers
    ]
    return jsonify(result)

@receiver_bp.route('/receiver/available-food', methods=['GET'])
@login_required
def provider_available_food():
    return jsonify(available_food()), 200

@receiver_bp.route('/receiver/claim-order/<int:order_id>', methods=['POST'])
@login_required
def claim_order(order_id):
    if not isinstance(current_user, Receiver):
        return jsonify({"error": "Unauthorized"}), 403

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.status != "available":
        return jsonify({"error": "Order not available or already claimed"}), 400

    order.receiver_id = current_user.id
    order.receiver_name = current_user.username
    order.status = "claimed"

    db.session.commit()
    return jsonify({"message": "Order claimed successfully!"}), 200