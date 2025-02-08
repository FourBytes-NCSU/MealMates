from . import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'), nullable=True)
    food_description = db.Column(db.Text, nullable=False)
    food_quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="available")  # 'available', 'claimed', 'expired'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
