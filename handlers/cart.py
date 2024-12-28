from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Temporary storage for carts
cart_storage = {}

# Add item to cart
def add_to_cart(user_id, item):
    if user_id not in cart_storage:
        cart_storage[user_id] = []
    cart_storage[user_id].append(item)

# Generate cart view
def generate_cart_view(user_id):
    cart = cart_storage.get(user_id, [])
    if not cart:
        return "Your cart is empty.", InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅ Back", callback_data="filter_menu")]])

    details = "\n".join(
        [f"{item['brand']} - {item['series']} (Size {item['size']}) - ${item['price']}" for item in cart]
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Back", callback_data="filter_menu")],
        ]
    )
    return f"Your cart:\n\n{details}", keyboard

# Handler for adding to cart
@router.callback_query(lambda c: c.data.startswith("add_to_cart_"))
async def add_to_cart_handler(callback: CallbackQuery):
    try:
        _, item_id, size = callback.data.split("_", 2)  # Extract item ID and size
        data = callback.message.bot["data"]  # Assuming the data is stored in the bot context
        item = data.get(item_id)

        if not item:
            await callback.message.edit_text("Item not found.", reply_markup=None)
            return

        # Add the selected item to the cart
        user_id = callback.from_user.id
        add_to_cart(user_id, {
            "brand": item["brand"],
            "series": item["series"],
            "size": size,
            "price": item["price"]
        })

        await callback.message.edit_text(
            f"Added {item['brand']} - {item['series']} (Size {size}) to your cart.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="⬅ Back", callback_data="filter_menu")]]
            )
        )
    except Exception as e:
        print(f"Error in add_to_cart_handler: {e}")
        await callback.message.edit_text("An error occurred. Please try again later.")

# Handler for viewing cart
@router.callback_query(lambda c: c.data == "view_cart")
async def view_cart(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        message, keyboard = generate_cart_view(user_id)
        await callback.message.edit_text(message, reply_markup=keyboard)
    except Exception as e:
        print(f"Error in view_cart: {e}")
        await callback.message.edit_text("An error occurred. Please try again later.")

def register_cart_handlers(dp):
    dp.include_router(router)
