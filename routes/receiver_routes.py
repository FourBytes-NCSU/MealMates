from flask import request, jsonify
from flask_login import login_user, login_required , current_user
from flask_cors import cross_origin

from models.order import Order
from models.receiver import Receiver
from models import db
from . import receiver_bp

@receiver_bp.route('/receiver/register', methods=['POST'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
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
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def login_receiver():
    data = request.json
    receiver = Receiver.query.filter_by(username=data['username']).first()

    if receiver and receiver.password == data['password']:
        login_user(receiver)
        return jsonify({"message": "Receiver login successful!", "user_type": "receiver"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@receiver_bp.route('/receiver/available-food', methods=['GET'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
@login_required
def receiver_available_food():
    print("🔹 Current User:", current_user)
    print("🔹 Current User Type:", type(current_user))
    print("🔹 Is Authenticated:", current_user.is_authenticated)

    if not isinstance(current_user, Receiver):
        return jsonify({"error": "Only receivers can view available food"}), 403

    available_orders = Order.query.filter_by(status="available").all()
    result = []
    for order in available_orders:
        result.append({
            "id": order.id,
            "provider_id": order.provider_id,
            "provider_name": order.provider_name,
            "food_description": order.food_description,
            "food_quantity": order.food_quantity,
            "expiry_date": order.expiry_date.strftime('%Y-%m-%d'),
            "diet_type_name": order.diet_type_name,
            "address": order.address,
            "city": order.city,
            "lat": order.lat,
            "lng": order.lng,
            "receiver_id": order.receiver_id,
            "receiver_name": order.receiver_name,
            "status": order.status,
            "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)


@receiver_bp.route('/receiver/claim/<int:order_id>', methods=['POST'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
@login_required
def claim_order_receiver(order_id):
    if not isinstance(current_user, Receiver):
        return jsonify({"error": "Only receivers can claim an order"}), 403

    order = Order.query.get(order_id)
    if not order or order.status != "available":
        return jsonify({"error": "Order not available or does not exist"}), 404

    order.receiver_id = current_user.id
    order.receiver_name = current_user.username
    order.status = "claimed"

    db.session.commit()
    return jsonify({"message": "Order claimed successfully!", "order_id": order.id}), 200