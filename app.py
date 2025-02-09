from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db
from models.provider import Provider
from models.receiver import Receiver
from routes.provider_routes import provider_bp
from routes.receiver_routes import receiver_bp
from routes.order_routes import order_bp
from routes.main_routes import main_bp
from flask_cors import CORS


# Initialize Flask app
app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "http://localhost:3000"}}
)
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_provider.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "provider_bp.login_provider"


app.register_blueprint(provider_bp)
app.register_blueprint(receiver_bp)
app.register_blueprint(order_bp)
app.register_blueprint(main_bp)

@login_manager.user_loader
def load_user(user_id):
    user = Provider.query.get(int(user_id))
    if user:
        print(f"🔹 Loading Provider: {user}, ID: {user.id}")
        return user

    user = Receiver.query.get(int(user_id))
    if user:
        print(f"🔹 Loading Receiver: {user}, ID: {user.id}")
        return user

    print(f"❌ No user found with ID: {user_id}")
    return None


@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

# Run the Flask app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
