from flask import request, jsonify
from flask_login import login_required, current_user
from models.order import Order
from models import db
from . import order_bp

@order_bp.route('/order/add', methods=['POST'])
@login_required
def add_food():
    data = request.json
    new_order = Order(
        provider_id=current_user.id,
        food_description=data['food_description'],
        food_quantity=data['food_quantity'],
        expiry_date=data['expiry_date']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Food listing added successfully!"}), 201

@order_bp.route('/order/available', methods=['GET'])
@login_required
def available_food():
    available_orders = Order.query.filter_by(status="available").all()
    result = [
        {
            "id": order.id,
            "food_description": order.food_description,
            "food_quantity": order.food_quantity,
            "expiry_date": order.expiry_date.strftime('%Y-%m-%d'),
            "provider_id": order.provider_id
        }
        for order in available_orders
    ]
    return jsonify(result)

@order_bp.route('/order/claim/<int:order_id>', methods=['POST'])
@login_required
def claim_food(order_id):
    order = Order.query.get(order_id)
    if not order or order.status != "available":
        return jsonify({"error": "Food not available"}), 404

    order.receiver_id = current_user.id
    order.status = "claimed"
    db.session.commit()
    return jsonify({"message": "Food claimed successfully!"}), 200
