from firebase_config import db

def populate_database():
    categories = {
        "shoes": {
            "item1": {"name": "Nike Air Max", "price": 120},
            "item2": {"name": "Adidas Ultraboost", "price": 150},
            "item3": {"name": "Puma Runner", "price": 99.99},
            "item4": {"name": "Reebok Classic", "price": 89.99},
        },
        "jackets": {
            "item1": {"name": "North Face Jacket", "price": 200},
            "item2": {"name": "Patagonia Down Sweater", "price": 250},
            "item3": {"name": "Columbia Windbreaker", "price": 120},
            "item4": {"name": "Levi's Denim Jacket", "price": 99.99},
        },
        "tshirts": {
            "item1": {"name": "Uniqlo Basic Tee", "price": 19.99},
            "item2": {"name": "H&M Cotton Shirt", "price": 15.99},
            "item3": {"name": "Adidas Sports Tee", "price": 29.99},
            "item4": {"name": "Nike Dri-FIT", "price": 34.99},
        },
        "jeans": {
            "item1": {"name": "Levi's 501 Original", "price": 69.99},
            "item2": {"name": "Wrangler Straight Fit", "price": 59.99},
            "item3": {"name": "Lee Modern Slim", "price": 49.99},
            "item4": {"name": "Uniqlo Skinny Jeans", "price": 39.99},
        },
        "accessories": {
            "item1": {"name": "Ray-Ban Sunglasses", "price": 150},
            "item2": {"name": "Fossil Leather Wallet", "price": 49.99},
            "item3": {"name": "Timex Classic Watch", "price": 79.99},
            "item4": {"name": "Casio Digital Watch", "price": 19.99},
        },
    }

    # Добавляем данные в базу
    for category, items in categories.items():
        ref = db.reference(f"categories/{category}")
        ref.set(items)

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_database()
