from firebase_config import db

def update_database():
    try:
        # Получаем все категории
        ref = db.reference("categories")
        categories = ref.get()

        if not categories:
            print("No categories found in the database.")
            return

        for category, items in categories.items():
            print(f"Processing category: {category}")
            for item_id, item_data in items.items():
                # Проверяем наличие поля 'name'
                if "name" in item_data:
                    name = item_data["name"]
                    # Разделяем 'name' на 'brand' и 'series'
                    parts = name.split(" ", 1)  # Разделяем по первому пробелу
                    brand = parts[0]
                    series = parts[1] if len(parts) > 1 else "Unknown"

                    # Обновляем данные
                    ref.child(category).child(item_id).update({
                        "brand": brand,
                        "series": series
                    })

                    # Удаляем старое поле 'name'
                    ref.child(category).child(item_id).child("name").delete()

                    print(f"Updated item {item_id}: brand={brand}, series={series}")
                else:
                    print(f"Item {item_id} in category {category} does not have a 'name' field.")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
    update_database()
