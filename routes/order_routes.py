from datetime import datetime, timezone, timedelta
from flask import request, jsonify
from flask_login import login_required, current_user
from models.order import Order
from models import db
from . import order_bp

@order_bp.route('/order/add', methods=['POST'])
def add_food():
    data = request.json
    new_order = Order(
        provider_id=data.get('provider_id'),
        provider_name=data.get('provider_name', 'Unknown'),
        food_description=data['food_description'],
        food_quantity=data['food_quantity'],
        expiry_date=data['expiry_date'],
        diet_type_name=data.get('diet_type_name', 'Unknown'),
        address=data.get('address', 'Unknown'),
        city=data.get('city', 'Unknown'),
        lat=data.get('lat'),  # Include latitude
        lng=data.get('lng'),  # Include longitude
        receiver_id=data.get('receiver_id'),
        receiver_name=data.get('receiver_name'),
        status='available'
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Food listing added successfully!"}), 201

@order_bp.route('/order/available-food', methods=['GET'])
def available_food():
    available_orders = Order.query.filter_by(status="available").all()
    result = [
        {
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
        }
        for order in available_orders
    ]
    return jsonify(result)

@order_bp.route('/order/all', methods=['GET'])
def all_orders():
    all_orders = Order.query.all()
    result = [
        {
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
        }
        for order in all_orders
    ]
    return jsonify(result)

@order_bp.route('/order/wasted', methods=['GET'])
def wasted_food():
    wasted_orders = Order.query.filter_by(status="expired").all()
    result = [
        {
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
        }
        for order in wasted_orders
    ]
    return jsonify(result)

@order_bp.route('/order/delete/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully!"}), 200

@order_bp.route('/order/update/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.json
    order.provider_name = data.get('provider_name', order.provider_name)
    order.food_description = data.get('food_description', order.food_description)
    order.food_quantity = data.get('food_quantity', order.food_quantity)
    order.expiry_date = data.get('expiry_date', order.expiry_date)
    order.diet_type_name = data.get('diet_type_name', order.diet_type_name)
    order.address = data.get('address', order.address)
    order.city = data.get('city', order.city)
    order.lat = data.get('lat', order.lat)
    order.lng = data.get('lng', order.lng)
    order.status = data.get('status', order.status)

    db.session.commit()
    return jsonify({"message": "Order updated successfully!"}), 200

@order_bp.route('/order/claim/<int:order_id>', methods=['POST'])
def claim_order(order_id):
    order = Order.query.get(order_id)
    if not order or order.status != "available":
        return jsonify({"error": "Order not available or does not exist"}), 404

    order.receiver_id = current_user.id
    order.receiver_name = current_user.username
    order.status = "claimed"

    db.session.commit()
    return jsonify({"message": "Order claimed successfully!"}), 200

@order_bp.route('/order/confirm/<int:order_id>', methods=['POST'])
def confirm_order(order_id):
    order = Order.query.get(order_id)
    if not order or order.status != "claimed":
        return jsonify({"error": "Order not claimed or does not exist"}), 404

    order.status = "saved"
    db.session.commit()
    return jsonify({"message": "Order confirmed as completed!"}), 200

@order_bp.route('/order/check-expiry', methods=['POST'])
def check_expired_orders():
    now = datetime.now(timezone.utc)
    expired_orders = Order.query.filter(Order.expiry_date < now, Order.status == "available" or Order.status == "claimed").all()

    for order in expired_orders:
        order.status = "expired"

    db.session.commit()
    return jsonify({"message": "Expired orders updated successfully!", "expired_count": len(expired_orders)})


@order_bp.route('/order/daily-stats', methods=['GET'])
def daily_stats():
    from datetime import datetime, timedelta, timezone
    now_utc = datetime.now(timezone.utc)
    today = now_utc.date()
    start_date = today - timedelta(days=30)
    result = []

    for i in range(31):
        d = start_date + timedelta(days=i)
        start_time = datetime.combine(d, datetime.min.time(), tzinfo=timezone.utc)
        end_time = start_time + timedelta(days=1)

        saved_count = (
            Order.query
                 .filter(Order.status == "saved",
                         Order.created_at >= start_time,
                         Order.created_at < end_time)
                 .count()
        )

        wasted_count = (
            Order.query
                 .filter(Order.status == "expired",
                         Order.created_at >= start_time,
                         Order.created_at < end_time)
                 .count()
        )

        result.append({
            "date": str(d),
            "meals_saved": saved_count,
            "meals_wasted": wasted_count
        })

    return jsonify(result)