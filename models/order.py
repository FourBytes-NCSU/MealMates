from . import db
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'), nullable=True)
    food_description = db.Column(db.Text, nullable=False)
    food_quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    diet_type_name = db.Column(db.String(50), nullable=False)  # Added diet type as a string
    address = db.Column(db.String(255), nullable=False)  # Added address field
    city = db.Column(db.String(100), nullable=False)  # Added city field
    lat = db.Column(db.Float, nullable=True)  # Latitude for exact location
    lng = db.Column(db.Float, nullable=True)  # Longitude for exact location
    receiver_name = db.Column(db.String(100), nullable=True)
    provider_name = db.Column(db.String(100), nullable=True)  # Receiver name field added
    status = db.Column(db.String(20), default="available")  # 'available', 'claimed', 'expired'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # Use timezone-aware datetime
