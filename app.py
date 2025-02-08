from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_provider.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Food Listing Model
class FoodListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=False)
    food_quantity = db.Column(db.Integer, nullable=False)
    food_description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    accepted_by_receiver = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.expiry_date

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

# Home/Landing page with statistics
@app.route('/')
@login_required
def index():
    total_listings = FoodListing.query.count()
    total_saved = FoodListing.query.filter(FoodListing.accepted_by_receiver == True).count()
    total_wasted = FoodListing.query.filter(FoodListing.accepted_by_receiver == False, FoodListing.expiry_date < datetime.utcnow()).count()
    
    return render_template('index.html', total_listings=total_listings, total_saved=total_saved, total_wasted=total_wasted)

# Food Listing Page
@app.route('/food-listings')
@login_required
def food_listings():
    listings = FoodListing.query.all()
    return render_template('food_listings.html', listings=listings)

# Food Listing Form
@app.route('/add-food', methods=['GET', 'POST'])
@login_required
def add_food():
    if request.method == 'POST':
        provider_name = request.form['provider_name']
        food_quantity = request.form['food_quantity']
        food_description = request.form['food_description']
        address = request.form['address']
        city = request.form['city']
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d %H:%M:%S')

        new_food = FoodListing(
            provider_name=provider_name,
            food_quantity=food_quantity,
            food_description=food_description,
            address=address,
            city=city,
            expiry_date=expiry_date
        )
        db.session.add(new_food)
        db.session.commit()
        flash('Food added successfully!', 'success')
        return redirect(url_for('food_listings'))

    return render_template('add_food.html')

# API Endpoint for AI Service - Get Available Food Listings
@app.route('/api/available-food', methods=['GET'])
def available_food():
    available_food = FoodListing.query.filter(FoodListing.accepted_by_receiver == False, FoodListing.expiry_date > datetime.utcnow()).all()
    
    result = [
        {
            "id": food.id,
            "provider_name": food.provider_name,
            "food_quantity": food.food_quantity,
            "food_description": food.food_description,
            "address": food.address,
            "city": food.city,
            "expiry_date": food.expiry_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        for food in available_food
    ]
    return jsonify(result)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

# User Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
