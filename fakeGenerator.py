import random
from faker import Faker
from datetime import datetime, timedelta, timezone
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
            expiry_days = random.randint(-3, 7)  # Some orders will have expired dates
            expiry_date = datetime.now(timezone.utc) + timedelta(days=expiry_days)
            diet_type = random.choice(diet_types)  # Assign a random diet type
            receiver_id = random.randint(1, 5) if random.choice([True, False]) else None  # Assign receiver ID sometimes

            if expiry_days < 0 and receiver_id is None:
                status = "expired"  # Explicitly mark as wasted
            elif receiver_id:
                status = "claimed"
            else:
                status = "available"

            fake_order = Order(
                provider_id=random.randint(1, 5),  # Assuming providers exist
                receiver_id=receiver_id,  # Assign receiver ID
                food_description=food_description,
                food_quantity=food_quantity,
                expiry_date=expiry_date,
                diet_type_name=diet_type,  # Assign diet type as string
                status=status
            )

            db.session.add(fake_order)

        db.session.commit()
        print("✅ 50 fake orders generated successfully, including wasted orders!")


# Function to display all orders
def display_orders():
    with app.app_context():
        orders = Order.query.all()
        if not orders:
            print("❌ No orders found!")
            return

        print("\n📌 **Current Orders:**\n")
        for order in orders:
            if order.status == "claimed":
                status = "SAVED ✅"
            elif order.status == "expired":
                status = "WASTED ❌"
            else:
                status = "AVAILABLE 🍽️"

            diet_type = order.diet_type_name if order.diet_type_name else "None"
            receiver_display = f"Receiver ID: {order.receiver_id}" if order.receiver_id else "No receiver yet"
            print(
                f"ID: {order.id} | Provider: {order.provider_id} | Quantity: {order.food_quantity} | Expiry: {order.expiry_date.strftime('%Y-%m-%d')} | Diet: {diet_type} | {receiver_display} | Status: {status}")


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
