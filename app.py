from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db
from routes.provider_routes import provider_bp
from routes.receiver_routes import receiver_bp
from routes.order_routes import order_bp
from routes.main_routes import main_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_provider.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register Blueprints
app.register_blueprint(provider_bp)
app.register_blueprint(receiver_bp)
app.register_blueprint(order_bp)
app.register_blueprint(main_bp)

# Create tables before first request
@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
