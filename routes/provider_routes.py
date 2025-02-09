from datetime import datetime, timezone

from flask import request, jsonify
from flask_login import login_required, current_user, login_user

from models.order import Order
from models.provider import Provider
from flask_cors import cross_origin
from models import db
from dateutil import parser
from . import provider_bp

@provider_bp.route('/provider/register', methods=['POST'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
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
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def login_provider():
    data = request.json
    provider = Provider.query.filter_by(username=data['username'], password=data['password']).first()
    if provider:
        login_user(provider)
        return jsonify({"message": "Provider login successful!"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@provider_bp.route('/provider/add', methods=['POST', 'PUT'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def add_food():
    hardcoded_provider = Provider.query.filter_by(username="myProvider").first()

    if not hardcoded_provider:
        return jsonify({"error": "Hardcoded provider not found"}), 500

    print("🔹 Using Hardcoded Provider:", hardcoded_provider.username)

    try:
        data = request.get_json(force=True)

        if data is None:
            return jsonify({"error": "Received empty JSON payload"}), 400

        expiry_str = data.get('expiry_date')
        expiry_date = parser.parse(expiry_str) if expiry_str else None

        new_order = Order(
            provider_id=hardcoded_provider.id,
            provider_name=hardcoded_provider.name,
            food_description=data.get('food_description'),
            food_quantity=int(data.get('food_quantity', 1)),
            expiry_date=expiry_date,
            diet_type_name=data.get('diet_type_name', 'Unknown'),
            address=hardcoded_provider.address,
            city=hardcoded_provider.city,
            lat=float(data.get('lat', 0)),
            lng=float(data.get('lng', 0)),
            status='available',
            created_at=datetime.now(timezone.utc)
        )

        db.session.add(new_order)
        db.session.commit()

        print("✅ Order Created Successfully!")
        return jsonify({"message": "Order added successfully!", "order_id": new_order.id}), 201

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": "Invalid JSON request", "details": str(e)}), 400