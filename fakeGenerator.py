import random
from faker import Faker
from datetime import datetime, timedelta
from app import db, FoodListing, User, app  # Import Flask app context

# Initialize Faker for fake data generation
fake = Faker()

# Function to create a single user inside an application context
def create_user():
    with app.app_context():
        existing_user = User.query.first()
        if not existing_user:
            user = User(username="testuser", password="testpassword")  # Change as needed
            db.session.add(user)
            db.session.commit()
            print("✅ Default user 'testuser' created!")

# Function to generate 50 fake food listings
def generate_fake_data():
    with app.app_context():
        create_user()  # Ensure at least one user exists

        for _ in range(50):
            provider_name = fake.name()
            food_quantity = random.randint(1, 10)
            food_description = fake.sentence()
            address = fake.address()
            city = fake.city()
            expiry_date = datetime.utcnow() + timedelta(days=random.randint(1, 7))
            accepted_by_receiver = random.choice([True, False])

            fake_food = FoodListing(
                provider_name=provider_name,
                food_quantity=food_quantity,
                food_description=food_description,
                address=address,
                city=city,
                expiry_date=expiry_date,
                accepted_by_receiver=accepted_by_receiver
            )

            db.session.add(fake_food)

        db.session.commit()
        print("✅ 50 fake food listings generated successfully!")

# Function to display all food listings
def display_data():
    with app.app_context():
        listings = FoodListing.query.all()
        if not listings:
            print("❌ No food listings found!")
            return

        print("\n📌 **Current Food Listings:**\n")
        for food in listings:
            status = "SAVED ✅" if food.accepted_by_receiver else "WASTED ❌"
            print(f"ID: {food.id} | Provider: {food.provider_name} | Quantity: {food.food_quantity} | City: {food.city} | Expiry: {food.expiry_date.strftime('%Y-%m-%d')} | Status: {status}")

# Main menu
def main():
    print("\n📌 **Database Utility for Food Listings**\n")
    print("1️⃣ Generate 50 Fake Food Listings")
    print("2️⃣ Display All Food Listings")
    print("3️⃣ Exit")

    choice = input("\nSelect an option: ")

    if choice == "1":
        generate_fake_data()
    elif choice == "2":
        display_data()
    elif choice == "3":
        print("🚀 Exiting...")
        exit()
    else:
        print("❌ Invalid choice, try again.")

# Run the script
if __name__ == "__main__":
    main()
