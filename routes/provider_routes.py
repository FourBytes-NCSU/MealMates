from datetime import datetime, timezone

from flask import request, jsonify
from flask_login import login_required, current_user, login_user

from models.order import Order
from models.provider import Provider
from models import db
from dateutil import parser
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


@provider_bp.route('/provider/add', methods=['POST'])
@login_required
def add_food():
    data = request.get_json()
    expiry_str = data.get('expiry_date')
    expiry_date = None
    if expiry_str:
        expiry_date = parser.parse(expiry_str)

    new_order = Order(
        provider_id=current_user.id,
        provider_name=current_user.name,
        food_description=data.get('food_description'),
        food_quantity=data.get('food_quantity', 1),
        expiry_date=expiry_date,
        diet_type_name=data.get('diet_type_name', 'Unknown'),
        address=current_user.address,
        city=current_user.city,
        lat=data.get('lat'),
        lng=data.get('lng'),
        status='available',
        created_at=datetime.now(timezone.utc)
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order added successfully!", "order_id": new_order.id}), 201