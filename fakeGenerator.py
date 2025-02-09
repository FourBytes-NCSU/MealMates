import random
from faker import Faker
from datetime import datetime, timedelta, timezone
from app import db, app  # Import Flask app context
from models.order import Order  # Import Order model
from models.provider import Provider  # Import Provider model
from models.receiver import Receiver  # Import Receiver model

fake = Faker("en_US")

# Predefined diet types
diet_types = ["Vegan", "Vegetarian", "Gluten-Free", "Halal", "Kosher", "Nut-Free"]

# 40 Real Addresses Across the USA
us_addresses = [
    {
        "address": "1600 Pennsylvania Ave NW",
        "city": "Washington, DC",
        "lat": 38.897663,
        "lng": -77.036574
    },
    {
        "address": "350 Fifth Avenue",
        "city": "New York, NY",
        "lat": 40.748817,
        "lng": -73.985428
    },
    {
        "address": "Golden Gate Bridge",
        "city": "San Francisco, CA",
        "lat": 37.819929,
        "lng": -122.478255
    },
    {
        "address": "200 Santa Monica Pier",
        "city": "Santa Monica, CA",
        "lat": 34.009242,
        "lng": -118.497604
    },
    {
        "address": "233 S Wacker Dr (Willis Tower)",
        "city": "Chicago, IL",
        "lat": 41.878876,
        "lng": -87.635915
    },
    {
        "address": "875 N Michigan Ave (John Hancock Center)",
        "city": "Chicago, IL",
        "lat": 41.898776,
        "lng": -87.623384
    },
    {
        "address": "600 Congress Ave",
        "city": "Austin, TX",
        "lat": 30.268775,
        "lng": -97.742222
    },
    {
        "address": "400 Dallas St",
        "city": "Houston, TX",
        "lat": 29.760391,
        "lng": -95.369850
    },
    {
        "address": "24 Beacon St",
        "city": "Boston, MA",
        "lat": 42.358804,
        "lng": -71.063604
    },
    {
        "address": "139 Tremont St",
        "city": "Boston, MA",
        "lat": 42.356963,
        "lng": -71.062105
    },
    {
        "address": "400 South Orange Ave",
        "city": "Orlando, FL",
        "lat": 28.538336,
        "lng": -81.379234
    },
    {
        "address": "1700 Epcot Resorts Blvd",
        "city": "Lake Buena Vista, FL",
        "lat": 28.370970,
        "lng": -81.558123
    },
    {
        "address": "3600 S Las Vegas Blvd",
        "city": "Las Vegas, NV",
        "lat": 36.112698,
        "lng": -115.176197
    },
    {
        "address": "3799 S Las Vegas Blvd",
        "city": "Las Vegas, NV",
        "lat": 36.102375,
        "lng": -115.170232
    },
    {
        "address": "2255 Kalakaua Ave",
        "city": "Honolulu, HI",
        "lat": 21.276822,
        "lng": -157.827348
    },
    {
        "address": "99-500 Salt Lake Blvd",
        "city": "Aiea, HI",
        "lat": 21.372041,
        "lng": -157.933179
    },
    {
        "address": "200 E Colfax Ave",
        "city": "Denver, CO",
        "lat": 39.739236,
        "lng": -104.990251
    },
    {
        "address": "1001 16th St Mall",
        "city": "Denver, CO",
        "lat": 39.746963,
        "lng": -104.994177
    },
    {
        "address": "285 Andrew Young International Blvd NW",
        "city": "Atlanta, GA",
        "lat": 33.760347,
        "lng": -84.393496
    },
    {
        "address": "126 Ivan Allen Jr Blvd NW",
        "city": "Atlanta, GA",
        "lat": 33.767836,
        "lng": -84.394617
    },
    {
        "address": "400 Broad St (Space Needle)",
        "city": "Seattle, WA",
        "lat": 47.620506,
        "lng": -122.349277
    },
    {
        "address": "800 Occidental Ave S",
        "city": "Seattle, WA",
        "lat": 47.595154,
        "lng": -122.332078
    },
    {
        "address": "200 Renaissance Center",
        "city": "Detroit, MI",
        "lat": 42.329522,
        "lng": -83.039240
    },
    {
        "address": "2211 Woodward Ave",
        "city": "Detroit, MI",
        "lat": 42.338985,
        "lng": -83.055182
    },
    {
        "address": "1500 Sugar Bowl Dr",
        "city": "New Orleans, LA",
        "lat": 29.951065,
        "lng": -90.081797
    },
    {
        "address": "1419 Basin St",
        "city": "New Orleans, LA",
        "lat": 29.968057,
        "lng": -90.072618
    },
    {
        "address": "116 5th Ave N",
        "city": "Nashville, TN",
        "lat": 36.162245,
        "lng": -86.778402
    },
    {
        "address": "600 Opry Mills Dr",
        "city": "Nashville, TN",
        "lat": 36.202918,
        "lng": -86.694647
    },
    {
        "address": "600 E Market St (Independence Hall)",
        "city": "Philadelphia, PA",
        "lat": 39.952583,
        "lng": -75.165222
    },
    {
        "address": "1 S Broad St",
        "city": "Philadelphia, PA",
        "lat": 39.951495,
        "lng": -75.164611
    },
    {
        "address": "455 N Galvin Pkwy",
        "city": "Phoenix, AZ",
        "lat": 33.459914,
        "lng": -111.947170
    },
    {
        "address": "201 E Jefferson St",
        "city": "Phoenix, AZ",
        "lat": 33.445525,
        "lng": -112.071474
    },
    {
        "address": "725 Vineland Pl",
        "city": "Minneapolis, MN",
        "lat": 44.979534,
        "lng": -93.288754
    },
    {
        "address": "900 Nicollet Mall",
        "city": "Minneapolis, MN",
        "lat": 44.977753,
        "lng": -93.271009
    },
    {
        "address": "1 S Memorial Dr (Gateway Arch)",
        "city": "St. Louis, MO",
        "lat": 38.624691,
        "lng": -90.184776
    },
    {
        "address": "3550 Samuel Shepard Dr",
        "city": "St. Louis, MO",
        "lat": 38.639304,
        "lng": -90.230074
    },
    {
        "address": "400 W Kilbourn Ave",
        "city": "Milwaukee, WI",
        "lat": 43.041153,
        "lng": -87.916488
    },
    {
        "address": "1111 Vel R Phillips Ave",
        "city": "Milwaukee, WI",
        "lat": 43.044948,
        "lng": -87.917347
    },
    {
        "address": "50 E North Temple",
        "city": "Salt Lake City, UT",
        "lat": 40.770447,
        "lng": -111.891220
    },
    {
        "address": "32 S State St",
        "city": "Salt Lake City, UT",
        "lat": 40.767012,
        "lng": -111.888147
    }
]

# 20 Real Addresses in Raleigh, NC
raleigh_addresses = [
    {
        "address": "1 E Edenton St",
        "city": "Raleigh, NC",
        "lat": 35.780672,
        "lng": -78.639095
    },
    {
        "address": "300 Hillsborough St",
        "city": "Raleigh, NC",
        "lat": 35.779458,
        "lng": -78.643534
    },
    {
        "address": "11 W Jones St",
        "city": "Raleigh, NC",
        "lat": 35.781467,
        "lng": -78.639076
    },
    {
        "address": "400 S McDowell St",
        "city": "Raleigh, NC",
        "lat": 35.775148,
        "lng": -78.638067
    },
    {
        "address": "1 E Morgan St",
        "city": "Raleigh, NC",
        "lat": 35.779619,
        "lng": -78.639409
    },
    {
        "address": "123 Fayetteville St",
        "city": "Raleigh, NC",
        "lat": 35.778231,
        "lng": -78.639700
    },
    {
        "address": "17 W Hargett St",
        "city": "Raleigh, NC",
        "lat": 35.779699,
        "lng": -78.639457
    },
    {
        "address": "10 Glenwood Ave",
        "city": "Raleigh, NC",
        "lat": 35.779655,
        "lng": -78.646751
    },
    {
        "address": "205 E North St",
        "city": "Raleigh, NC",
        "lat": 35.784865,
        "lng": -78.637615
    },
    {
        "address": "501 S Person St",
        "city": "Raleigh, NC",
        "lat": 35.772004,
        "lng": -78.634656
    },
    {
        "address": "500 S Salisbury St",
        "city": "Raleigh, NC",
        "lat": 35.773395,
        "lng": -78.641613
    },
    {
        "address": "1 W Morgan St",
        "city": "Raleigh, NC",
        "lat": 35.779553,
        "lng": -78.639491
    },
    {
        "address": "301 W Jones St",
        "city": "Raleigh, NC",
        "lat": 35.782078,
        "lng": -78.641513
    },
    {
        "address": "16 W Martin St",
        "city": "Raleigh, NC",
        "lat": 35.776483,
        "lng": -78.639230
    },
    {
        "address": "549 N Person St",
        "city": "Raleigh, NC",
        "lat": 35.790088,
        "lng": -78.635733
    },
    {
        "address": "834 Wake Forest Rd",
        "city": "Raleigh, NC",
        "lat": 35.795671,
        "lng": -78.625942
    },
    {
        "address": "231 New Bern Ave",
        "city": "Raleigh, NC",
        "lat": 35.779609,
        "lng": -78.635978
    },
    {
        "address": "317 Blount St",
        "city": "Raleigh, NC",
        "lat": 35.781242,
        "lng": -78.635003
    },
    {
        "address": "720 W Johnson St",
        "city": "Raleigh, NC",
        "lat": 35.782894,
        "lng": -78.652356
    },
    {
        "address": "141 Park at N Hills St",
        "city": "Raleigh, NC",
        "lat": 35.837308,
        "lng": -78.642853
    }
]

def generate_fake_providers_receivers():
    """
    Creates 5 sample Providers and Receivers if they don't already exist.
    """
    with app.app_context():
        # Create 5 providers
        for i in range(1, 6):
            existing_provider = Provider.query.get(i)
            if not existing_provider:
                provider = Provider(
                    id=i,
                    username=f"provider{i}",
                    password=fake.password(),
                    name=fake.company(),
                    address=fake.street_address(),  # Just for provider’s personal record
                    city=fake.city()
                )
                db.session.add(provider)

        # Create 5 receivers
        for i in range(1, 6):
            existing_receiver = Receiver.query.get(i)
            if not existing_receiver:
                receiver = Receiver(
                    id=i,
                    username=f"receiver{i}",
                    password=fake.password(),
                    name=fake.name(),
                    city=fake.city()
                )
                db.session.add(receiver)

        db.session.commit()
        print("✅ Fake providers and receivers generated successfully!")

def generate_fake_orders():
    """
    Generates exactly 60 orders:
      - 40 "general" orders from the us_addresses list
      - 20 "Raleigh" orders from the raleigh_addresses list

    Only the address is fixed (via lists).
    Everything else (quantity, description, expiry date, diet, optional receiver) is randomized.
    """
    with app.app_context():
        generate_fake_providers_receivers()

        existing_providers = Provider.query.all()
        existing_receivers = Receiver.query.all()

        # 1) Generate 40 general orders (from the 40 curated US addresses)
        for i in range(40):
            address_data = us_addresses[i]
            address = address_data["address"]
            city = address_data["city"]
            lat = address_data["lat"]
            lng = address_data["lng"]

            # Random aspects
            food_quantity = random.randint(1, 10)
            food_description = fake.sentence()
            expiry_days = random.randint(-3, 7)  # can be negative for "expired"
            expiry_date = datetime.now(timezone.utc) + timedelta(days=expiry_days)
            diet_type = random.choice(diet_types)

            # 50% chance to have a receiver
            receiver = random.choice(existing_receivers) if random.choice([True, False]) else None
            receiver_id = receiver.id if receiver else None
            receiver_name = receiver.name if receiver else ""

            # Random provider
            provider = random.choice(existing_providers)
            provider_id = provider.id
            provider_name = provider.name

            # Determine status
            if expiry_days < 0 and not receiver_id:
                status = "expired"
            elif receiver_id:
                status = "claimed"
            else:
                status = "available"

            fake_order = Order(
                provider_id=provider_id,
                receiver_id=receiver_id,
                receiver_name=receiver_name,
                food_description=food_description,
                food_quantity=food_quantity,
                expiry_date=expiry_date,
                diet_type_name=diet_type,
                address=address,
                city=city,
                lat=lat,
                lng=lng,
                status=status,
                provider_name=provider_name
            )
            db.session.add(fake_order)

        # 2) Generate 20 Raleigh orders (from the 20 curated Raleigh addresses)
        for i in range(20):
            address_data = raleigh_addresses[i]
            address = address_data["address"]
            city = address_data["city"]
            lat = address_data["lat"]
            lng = address_data["lng"]

            # Random aspects
            food_quantity = random.randint(1, 10)
            food_description = fake.sentence()
            expiry_days = random.randint(-3, 7)
            expiry_date = datetime.now(timezone.utc) + timedelta(days=expiry_days)
            diet_type = random.choice(diet_types)

            # Optional receiver
            receiver = random.choice(existing_receivers) if random.choice([True, False]) else None
            receiver_id = receiver.id if receiver else None
            receiver_name = receiver.name if receiver else ""

            # Random provider
            provider = random.choice(existing_providers)
            provider_id = provider.id
            provider_name = provider.name

            # Determine status
            if expiry_days < 0 and not receiver_id:
                status = "expired"
            elif receiver_id:
                status = "claimed"
            else:
                status = "available"

            fake_order = Order(
                provider_id=provider_id,
                receiver_id=receiver_id,
                receiver_name=receiver_name,
                food_description=food_description,
                food_quantity=food_quantity,
                expiry_date=expiry_date,
                diet_type_name=diet_type,
                address=address,
                city=city,
                lat=lat,
                lng=lng,
                status=status,
                provider_name=provider_name
            )
            db.session.add(fake_order)

        db.session.commit()
        print("✅ 60 fake orders generated successfully (40 US + 20 Raleigh)!")

def display_orders():
    with app.app_context():
        orders = Order.query.all()
        if not orders:
            print("❌ No orders found!")
            return

        print("\n📌 **Current Orders:**\n")
        for order in orders:
            status_label = (
                "SAVED ✅" if order.status == "claimed"
                else "WASTED ❌" if order.status == "expired"
                else "AVAILABLE 🍽️"
            )
            print(
                f"ID: {order.id} | Provider: {order.provider_id} ({order.provider_name}) | "
                f"Quantity: {order.food_quantity} | Expiry: {order.expiry_date.strftime('%Y-%m-%d')} | "
                f"Diet: {order.diet_type_name} | Address: {order.address}, {order.city} | "
                f"Lat: {order.lat}, Lng: {order.lng} | Receiver: {order.receiver_name} | Status: {status_label}"
            )

def main():
    print("\n📌 **Database Utility for Orders**\n")
    print("1️⃣ Generate 60 Fake Orders (40 US + 20 Raleigh)")
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

if __name__ == "__main__":
    main()
