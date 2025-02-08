import random
from faker import Faker
from datetime import datetime, timedelta
from app import db, app  # Import Flask app context
from models.order import Order  # Import Order model

# Initialize Faker for fake data generation
fake = Faker()

# Predefined diet types
diet_types = ["Vegan", "Vegetarian", "Gluten-Free", "Halal", "Kosher", "Nut-Free"]

# Function to generate 50 fake orders
def generate_fake_orders():
    with app.app_context():
        for _ in range(50):
            food_quantity = random.randint(1, 10)
            food_description = fake.sentence()
            expiry_date = datetime.utcnow() + timedelta(days=random.randint(1, 7))
            diet_type = random.choice(diet_types)  # Assign a random diet type

            fake_order = Order(
                provider_id=random.randint(1, 5),  # Assuming providers exist
                food_description=food_description,
                food_quantity=food_quantity,
                expiry_date=expiry_date,
                diet_type_name=diet_type,  # Assign diet type as string
                status="available" if random.choice([True, False]) else "claimed"
            )

            db.session.add(fake_order)

        db.session.commit()
        print("✅ 50 fake orders generated successfully!")

# Function to display all orders
def display_orders():
    with app.app_context():
        orders = Order.query.all()
        if not orders:
            print("❌ No orders found!")
            return

        print("\n📌 **Current Orders:**\n")
        for order in orders:
            status = "SAVED ✅" if order.status == "claimed" else "AVAILABLE 🍽️"
            diet_type = order.diet_type_name if order.diet_type_name else "None"
            print(f"ID: {order.id} | Provider: {order.provider_id} | Quantity: {order.food_quantity} | Expiry: {order.expiry_date.strftime('%Y-%m-%d')} | Diet: {diet_type} | Status: {status}")

# Main menu
def main():
    print("\n📌 **Database Utility for Orders**\n")
    print("1️⃣ Generate 50 Fake Orders")
    print("2️⃣ Display All Orders")
    print("3️⃣ Exit")

    choice = input("\nSelect an option: ")

    if choice == "1":
        generate_fake_orders()
    elif choice == "2":
        display_orders()
    elif choice == "3":
        print("🚀 Exiting...")
        exit()
    else:
        print("❌ Invalid choice, try again.")

# Run the script
if __name__ == "__main__":
    main()
