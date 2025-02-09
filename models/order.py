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
    diet_type_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    receiver_name = db.Column(db.String(100), nullable=True)
    provider_name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default="available")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
