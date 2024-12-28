from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from firebase_config import db
import traceback

router = Router()

# Global variables to store filters
filters = {
    "gender": [],
    "season": [],
    "category": [],
    "brand": [],
}

# Temporary cart storage
cart = {}

# Retrieve data from Firebase
def get_data():
    try:
        ref = db.reference("shoes")
        data = ref.get()
        print("Fetched shoes data:", data)  # Debugging output
        return data if data and isinstance(data, dict) else {}
    except Exception as e:
        print(f"Error fetching data from Firebase: {e}")
        traceback.print_exc()
        return {}

# Generate filter menu
def filter_menu():
    keyboard = [
        [InlineKeyboardButton(text="Category", callback_data="filter_category")],
        [InlineKeyboardButton(text="Gender", callback_data="filter_gender")],
        [InlineKeyboardButton(text="Season", callback_data="filter_season")],
        [InlineKeyboardButton(text="Brand", callback_data="filter_brand")],
        [InlineKeyboardButton(text="View Cart", callback_data="view_cart")],
        [InlineKeyboardButton(text="🔄 Reset Filters", callback_data="reset_filters")],
        [InlineKeyboardButton(text="🔍 Search", callback_data="apply_filters")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Show filter menu
@router.callback_query(lambda c: c.data == "filter_menu")
async def show_filter_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Select a filter to apply:", reply_markup=filter_menu())
    except Exception as e:
        print(f"Error in show_filter_menu: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred. Please try again later.")

# Reset filters
@router.callback_query(lambda c: c.data == "reset_filters")
async def reset_filters(callback: CallbackQuery):
    global filters
    filters = {key: [] for key in filters}
    await callback.message.edit_text("Filters have been reset.", reply_markup=filter_menu())

# Generic filter handler
def create_filter_handler(filter_type, options):
    @router.callback_query(lambda c: c.data == f"filter_{filter_type}")
    async def show_filter(callback: CallbackQuery):
        keyboard = [
            [InlineKeyboardButton(text=option, callback_data=f"toggle_{filter_type}_{option}")] for option in options
        ]
        keyboard.append([InlineKeyboardButton(text="⬅ Back", callback_data="filter_menu")])
        await callback.message.edit_text(
            f"Select {filter_type.capitalize()}:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )

    @router.callback_query(lambda c: c.data.startswith(f"toggle_{filter_type}_"))
    async def toggle_filter(callback: CallbackQuery):
        global filters
        value = callback.data.split("_")[2]
        if value in filters[filter_type]:
            filters[filter_type].remove(value)  # Deselect
        else:
            filters[filter_type].append(value)  # Select
        await callback.message.edit_text(
            f"Selected {filter_type.capitalize()}: {', '.join(filters[filter_type])}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="⬅ Back", callback_data="filter_menu")]]
            )
        )

# Create handlers for each filter type
create_filter_handler("gender", ["Male", "Female", "Unisex", "Boys", "Girls"])
create_filter_handler("season", ["Winter", "Summer", "Spring", "Autumn", "Demi-season"])
create_filter_handler("category", ["Boots", "Sneakers", "Slippers", "Sandals", "Flip-flops"])
create_filter_handler("brand", ["Nike", "Adidas", "Puma", "Reebok", "Timberland"])  # Replace with dynamic data if needed

# Apply filters
@router.callback_query(lambda c: c.data == "apply_filters")
async def apply_filters(callback: CallbackQuery):
    try:
        data = get_data()

        # Apply filters to data
        filtered_data = {key: item for key, item in data.items() if
                         (not filters["gender"] or item.get("gender") in filters["gender"]) and
                         (not filters["season"] or item.get("season") in filters["season"]) and
                         (not filters["category"] or item.get("category") in filters["category"]) and
                         (not filters["brand"] or item.get("brand") in filters["brand"])}

        if not filtered_data:
            await callback.message.edit_text("No items found for the applied filters.", reply_markup=filter_menu())
            return

        # Generate buttons for filtered items
        keyboard = []
        for item_id, item in filtered_data.items():
            button_text = f"{item['brand']} - {item['series']} - ${item['price']}"
            # Use full item_id from the database as the callback data
            keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"item_{item_id}")])

        keyboard.append([InlineKeyboardButton(text="⬅ Back", callback_data="filter_menu")])

        await callback.message.edit_text(
            "Filtered items:\nSelect an item:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    except Exception as e:
        print(f"Error in apply_filters: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred while searching. Please try again later.")


@router.callback_query(lambda c: c.data.startswith("item_"))
async def show_item_sizes(callback: CallbackQuery):
    try:
        # Extract item ID from the callback data
        item_id = callback.data.split("_", 1)[1]  # Extract item ID
        print(f"Received item_id: {item_id}")  # Debugging callback data

        data = get_data()
        print(f"Fetched data for item ID {item_id}: {data.get(item_id)}")  # Debugging database lookup

        item = data.get(item_id)

        if not item:
            print(f"Item ID {item_id} not found in data.")  # Debugging output
            await callback.message.edit_text("Item not found.", reply_markup=filter_menu())
            return

        # Generate buttons for available sizes
        sizes = sorted(item["sizes"])  # Extract sizes and sort them
        keyboard = [
            [InlineKeyboardButton(text=str(size), callback_data=f"size_{item_id}_{size}")] for size in sizes
        ]
        keyboard.append([InlineKeyboardButton(text="⬅ Back", callback_data="apply_filters")])

        await callback.message.edit_text(
            f"Available sizes for {item['brand']} - {item['series']}:\nSelect a size:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    except Exception as e:
        print(f"Error in show_item_sizes: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred. Please try again later.")


@router.callback_query(lambda c: c.data.startswith("size_"))
async def show_item_details(callback: CallbackQuery):
    try:
        print(f"Received callback data for size: {callback.data}")  # Debugging callback data
        _, item_id, size = callback.data.split("_", 2)  # Extract item ID and selected size
        data = get_data()
        print(f"Fetched data for item ID {item_id}: {data.get(item_id)}")  # Log database lookup
        item = data.get(item_id)

        if not item:
            print(f"Item ID {item_id} not found in data.")  # Debugging output
            await callback.message.edit_text("Item not found.", reply_markup=filter_menu())
            return

        # Add item details
        details = (
            f"**Brand:** {item['brand']}\n"
            f"**Series:** {item['series']}\n"
            f"**Category:** {item['category']}\n"
            f"**Season:** {item['season']}\n"
            f"**Selected Size:** {size}\n"
            f"**Price:** ${item['price']}\n"
            f"**Available Sizes:** {', '.join(map(str, item['sizes']))}"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Add to Cart", callback_data=f"add_to_cart_{item_id}_{size}")],
            [InlineKeyboardButton(text="⬅ Back", callback_data=f"item_{item_id}")]
        ])
        await callback.message.edit_text(details, reply_markup=keyboard, parse_mode="Markdown")
    except Exception as e:
        print(f"Error in show_item_details: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred. Please try again later.")

@router.callback_query(lambda c: c.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    try:
        print(f"Received callback data for cart: {callback.data}")  # Debugging callback data
        _, item_id, size = callback.data.split("_", 2)  # Extract item ID and size
        data = get_data()
        item = data.get(item_id)

        if not item:
            await callback.message.edit_text("Item not found.", reply_markup=filter_menu())
            return

        # Add item to cart
        user_id = callback.from_user.id
        if user_id not in cart:
            cart[user_id] = []
        cart[user_id].append({
            "item_id": item_id,
            "brand": item["brand"],
            "series": item["series"],
            "size": size,
            "price": item["price"]
        })

        # Confirm addition to cart
        await callback.message.edit_text(
            f"Added {item['brand']} - {item['series']} (Size {size}) to your cart.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="⬅ Back to Filters", callback_data="filter_menu")]]
            )
        )
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        traceback.print_exc()
        await callback.message.edit_text("An error occurred. Please try again later.")


# View Cart
@router.callback_query(lambda c: c.data == "view_cart")
async def view_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_cart = cart.get(user_id, [])
    if not user_cart:
        await callback.message.edit_text("Your cart is empty.", reply_markup=filter_menu())
        return

    cart_details = "\n".join([f"{item['brand']} {item['series']} (Size {item['size']}) - ${item['price']}" for item in user_cart])
    await callback.message.edit_text(f"Your cart:\n\n{cart_details}", reply_markup=filter_menu())


# Function to register handlers
def register_category_handlers(dp):
    dp.include_router(router)
