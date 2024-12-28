from firebase_config import db

def add_additional_series():
    try:
        # Fetch existing categories and their items
        ref = db.reference("categories")
        categories = ref.get()

        if not categories:
            print("No categories found in the database.")
            return

        # Predefined series for each brand
        additional_series = {
            "Ray-Ban": ["Wayfarer", "Aviator", "Clubmaster", "Round Metal", "Erika"],
            "Fossil": ["Minimalist Watch", "Grant Watch", "Chronograph", "Hybrid Smartwatch", "Georgia Wallet"],
            "Timex": ["Expedition Scout", "Ironman Classic", "Weekender", "Marlin", "Navi Harbor"],
            "Casio": ["G-Shock", "Pro Trek", "Edifice", "Data Bank", "Classic Quartz"],
            "North": ["Thermoball Vest", "Gotham Jacket", "Arctic Parka", "Aconcagua Vest", "Horizon Jacket"],
            "Patagonia": ["Nano Puff", "Micro Puff Hoody", "Down Sweater Vest", "Better Sweater", "Rainshadow Jacket"],
            "Columbia": ["Powder Lite", "Frost Fighter", "Delta Ridge", "Voodoo Falls", "Glennaker Lake"],
            "Levi's": ["711 Skinny", "720 High Rise", "Ribcage Straight", "Vintage Fit", "Wedgie Icon"],
            "Wrangler": ["Retro Slim Fit", "Cowboy Cut", "Relaxed Fit", "Riggs Workwear", "Bootcut Jean"],
            "Lee": ["Extreme Motion", "Relaxed Fit", "Slim Straight", "Modern Bootcut", "Performance Series"],
            "Uniqlo": ["Ultra Stretch Skinny", "U Crew Neck Tee", "Supima Cotton Shirt", "Flannel Check Shirt", "Heattech Turtleneck"],
            "Nike": ["Metcon 7", "ZoomX Vaporfly", "Blazer Mid", "React Infinity Run", "Court Legacy"],
            "Puma": ["Rider FV", "Basket Classic", "Tazon 6", "Ignite Limitless", "Cell Surin"],
            "Reebok": ["Nano X2", "Classic Leather", "Floatride Energy", "Club C Revenge", "Zig Kinetica"],
            "Adidas": ["Gazelle", "Solar Glide", "Ozweego", "Terrex Free Hiker", "Copa Mundial"],
            "Asics": ["Gel-Kayano", "Gel-Nimbus", "Gel-Cumulus", "GlideRide", "Noosa Tri"]
        }

        for category, items in categories.items():
            print(f"Processing category: {category}")

            for item_id, item_data in items.items():
                brand = item_data.get("brand")
                if brand in additional_series:
                    for series in additional_series[brand]:
                        # Generate unique item ID
                        new_item_id = f"item_{hash(series) % 100000}"

                        # Add the new item
                        ref.child(category).child(new_item_id).set({
                            "brand": brand,
                            "series": series,
                            "price": round(50 + (hash(series) % 150), 2)  # Random price between $50 and $200
                        })
                        print(f"Added series '{series}' for brand '{brand}' in category '{category}'.")

    except Exception as e:
        print(f"Error updating database: {e}")

# Execute the function to update the database
add_additional_series()
