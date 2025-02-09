from flask import request, jsonify
from flask_login import login_user, login_required, current_user
from models.provider import Provider
from models import db
from . import provider_bp
from routes.order_routes import add_food, available_food, update_order
from models.order import Order

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

@provider_bp.route('/providers', methods=['GET'])
@login_required
def get_providers():
    providers = Provider.query.all()
    result = [
        {
            "id": provider.id,
            "username": provider.username,
            "name": provider.name,
            "address": provider.address,
            "city": provider.city
        }
        for provider in providers
    ]
    return jsonify(result)

@provider_bp.route('/provider/add', methods=['POST'])
@login_required
def provider_add_food():
    if not isinstance(current_user, Provider):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    provider = Provider.query.filter_by(id=current_user.id).first()

    if not provider:
        return jsonify({"error": "Provider not found"}), 404

    # ✅ Call add_food() from order_routes.py
    response, status_code = add_food(provider, data)
    return jsonify(response), status_code

@provider_bp.route('/provider/confirm-order/<int:order_id>', methods=['POST'])
@login_required
def confirm_order(order_id):
    if not isinstance(current_user, Provider):
        return jsonify({"error": "Unauthorized"}), 403

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.status != "claimed":
        return jsonify({"error": "Order not claimed or does not exist"}), 400

    # Ensure only the provider who created the order can confirm it
    if order.provider_id != current_user.id:
        return jsonify({"error": "You can only confirm orders you created"}), 403

    order.status = "saved"
    db.session.commit()
    return jsonify({"message": "Order confirmed as completed!"}), 200


@provider_bp.route('/provider/update-order/<int:order_id>', methods=['PUT'])
@login_required
def provider_update_order(order_id):
    return update_order(order_id)

@provider_bp.route('/provider/delete-order/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    if not isinstance(current_user, Provider):
        return jsonify({"error": "Unauthorized"}), 403

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Ensure the logged-in provider is the owner of the order
    if order.provider_id != current_user.id:
        return jsonify({"error": "You can only delete your own orders"}), 403

    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400