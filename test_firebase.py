from firebase_config import db

def test_read_categories():
    ref = db.reference("categories")
    categories = ref.get()
    print("Categories:", categories)

if __name__ == "__main__":
    test_read_categories()
