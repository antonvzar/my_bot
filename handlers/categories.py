from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from firebase_config import db
import traceback

router = Router()

# Retrieve list of categories from Firebase
def get_categories():
    ref = db.reference("categories")
    categories = ref.get()
    print("Fetched categories:", categories)  # Debugging output
    if categories and isinstance(categories, dict):
        return list(categories.keys())  # Return category names
    return []

# Generate a keyboard with categories
def categories_menu():
    try:
        categories = get_categories()
        print("Generating menu for categories:", categories)  # Debugging output

        # Проверяем, есть ли категории
        if not categories:
            print("No categories found!")
            return InlineKeyboardMarkup(inline_keyboard=[])

        # Генерируем клавиатуру
        keyboard = []
        for category in categories:
            keyboard.append([InlineKeyboardButton(text=category.capitalize(), callback_data=f"category_{category}")])

        # Добавляем кнопку "Back"
        keyboard.append([InlineKeyboardButton(text="⬅ Back", callback_data="back_to_main")])

        # Возвращаем InlineKeyboardMarkup с заполненным inline_keyboard
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    except Exception as e:
        print(f"Error in categories_menu: {e}")
        traceback.print_exc()
        return InlineKeyboardMarkup(inline_keyboard=[])

# Handler for the "Select Category" button
@router.callback_query(lambda c: c.data == "select_category")
async def show_categories(callback: CallbackQuery):
    try:
        keyboard = categories_menu()
        print("Generated keyboard:", keyboard.inline_keyboard)  # Debugging output
        if keyboard.inline_keyboard:  # Проверяем, есть ли кнопки
            await callback.message.edit_text("Please select a category:", reply_markup=keyboard)
        else:
            await callback.message.edit_text(
                "No categories available at the moment.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅ Back", callback_data="back_to_main")]]
                )
            )
    except Exception as e:
        print(f"Error in show_categories: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred while loading categories. Please try again later.")

# Handler for displaying brands in a selected category
@router.callback_query(lambda c: c.data.startswith("category_"))
async def show_brands(callback: CallbackQuery):
    try:
        category = callback.data.split("_")[1]  # Extract category name
        ref = db.reference(f"categories/{category}")
        items = ref.get()
        print(f"Fetched items for category {category}:", items)  # Debugging output

        if items and isinstance(items, dict):
            # Extract unique brands from the category
            brands = {item_data['brand'] for item_data in items.values()}
            print(f"Brands in category {category}:", brands)

            # Generate keyboard for brands
            keyboard = []
            for brand in brands:
                keyboard.append([InlineKeyboardButton(text=brand, callback_data=f"brand_{category}_{brand}")])

            # Add "Back" button
            keyboard.append([InlineKeyboardButton(text="⬅ Back", callback_data="select_category")])

            # Send the message with the keyboard
            await callback.message.edit_text(
                f"Brands in {category.capitalize()}:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        else:
            # No items in category
            await callback.message.edit_text(
                "No brands available in this category.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅ Back", callback_data="select_category")]]
                )
            )
    except Exception as e:
        print(f"Error in show_brands: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred while loading brands. Please try again later.")

# Handler for displaying series in a selected brand
@router.callback_query(lambda c: c.data.startswith("brand_"))
async def show_series(callback: CallbackQuery):
    try:
        _, category, brand = callback.data.split("_")  # Extract category and brand
        ref = db.reference(f"categories/{category}")
        items = ref.get()
        print(f"Fetched items for brand {brand} in category {category}:", items)  # Debugging output

        if items and isinstance(items, dict):
            # Extract series for the selected brand
            series_list = [item_data['series'] for item_data in items.values() if item_data['brand'] == brand]
            print(f"Series for brand {brand}:", series_list)

            # Generate keyboard for series
            keyboard = []
            for series in series_list:
                keyboard.append([InlineKeyboardButton(text=series, callback_data=f"series_{category}_{brand}_{series}")])

            # Add "Back" button
            keyboard.append([InlineKeyboardButton(text="⬅ Back", callback_data=f"category_{category}")])

            # Send the message with the keyboard
            await callback.message.edit_text(
                f"Series for {brand} in {category.capitalize()}:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        else:
            # No series for this brand
            await callback.message.edit_text(
                f"No series available for {brand}.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅ Back", callback_data=f"category_{category}")]]
                )
            )
    except Exception as e:
        print(f"Error in show_series: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred while loading series. Please try again later.")

# Function to register handlers
def register_category_handlers(dp):
    dp.include_router(router)
