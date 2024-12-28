import random
from firebase_config import db

def populate_database_randomly():
    try:
        # Define the structure of the items to be added
        genders = ["Male", "Female", "Unisex", "Boys", "Girls"]
        seasons = ["Winter", "Summer", "Spring", "Autumn", "Demi-season"]
        categories = ["Boots", "Sneakers", "Slippers", "Sandals", "Flip-flops"]
        brands_with_series = {
            "Nike": ["Air Max", "Blazer", "React Infinity", "Zoom Pegasus", "Metcon"],
            "Adidas": ["Ultraboost", "Gazelle", "NMD R1", "Ozweego", "Terrex"],
            "Puma": ["RS-X", "Future Rider", "Cali Star", "Tazon", "Ignite"],
            "Reebok": ["Nano X", "Classic Leather", "Floatride", "Club C", "Zig Kinetica"],
            "Timberland": ["6-Inch Premium", "Chukka", "Euro Sprint", "Field Boot", "PRO Series"],
            "Vans": ["Old Skool", "Authentic", "Era", "Sk8-Hi", "Slip-On"],
            "Converse": ["Chuck Taylor", "All Star", "One Star", "Run Star Hike", "Weapon"],
            "New Balance": ["574", "990v5", "Fresh Foam", "FuelCell", "1080"],
            "ASICS": ["Gel-Kayano", "Gel-Nimbus", "Gel-Cumulus", "GlideRide", "Noosa Tri"],
            "Fila": ["Disruptor", "Ray Tracer", "Memory Workshift", "Strada", "Grant Hill"]
        }

        ref = db.reference("shoes")

        for brand, series_list in brands_with_series.items():
            for gender in genders:
                # Randomly select series for this gender
                selected_series = random.sample(series_list, random.randint(2, 4))

                for series in selected_series:
                    # Randomly assign this series to a season
                    season = random.choice(seasons)
                    # Randomly select sizes (1 to 10 unique values between 30 and 50)
                    sizes = random.sample(range(30, 51), random.randint(1, 10))
                    # Randomly select a category
                    category = random.choice(categories)
                    # Generate a price between $50 and $200
                    price = round(random.uniform(50, 200), 2)

                    # Generate unique ID for the item
                    item_id = f"{brand}_{series}_{gender}_{season}_{category}"

                    # Add item to the database
                    ref.child(item_id).set({
                        "gender": gender,
                        "season": season,
                        "category": category,
                        "brand": brand,
                        "series": series,
                        "sizes": sizes,
                        "price": price
                    })
                    print(f"Added item: {item_id}")

    except Exception as e:
        print(f"Error populating the database: {e}")

# Populate the database with the randomized structure
populate_database_randomly()
