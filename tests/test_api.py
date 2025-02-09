import pytest
from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    """Set up a test client and database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for tests

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()  # Clean up DB after tests

# ✅ Test Registration
def test_register_provider(client):
    response = client.post('/provider/register', json={
        "username": "testprovider",
        "password": "securepassword",
        "name": "Test Provider",
        "address": "123 Test St",
        "city": "Test City"
    })
    assert response.status_code == 201
    assert response.json["message"] == "Provider registered successfully!"

# ✅ Test Login
def test_login(client):
    # Add a test user manually
    with app.app_context():
        user = User(username="testuser", password=generate_password_hash("securepassword"), role="provider")
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', json={
        "username": "testuser",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "Login successful!" in response.json["message"]

# ✅ Test Creating an Order
def test_create_order(client):
    # Log in to get session
    client.post('/login', json={"username": "testuser", "password": "securepassword"})

    response = client.post('/provider/add', json={
        "food_description": "Fresh Apples",
        "food_quantity": 5,
        "expiry_date": "2025-03-10",
        "diet_type_name": "Vegan",
        "lat": 40.7128,
        "lng": -74.0060
    })
    assert response.status_code == 201
    assert response.json["message"] == "Food order created successfully!"

# ✅ Test Logout
def test_logout(client):
    response = client.post('/logout')
    assert response.status_code == 200
    assert response.json["message"] == "Logged out successfully!"
