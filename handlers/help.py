from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Help message
HELP_MESSAGE = (
    "Welcome to the Help section! Here's what you can do:\n\n"
    "- **Select Category**: Browse and select items to add to your cart.\n"
    "- **Cart**: View items in your cart.\n"
    "- **Place Order**: Finalize your order.\n\n"
    "If you have further questions, contact support."
)

# Help menu with 3 buttons per row and a large Back button
def help_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="FAQ", callback_data="faq"),
                InlineKeyboardButton(text="Contact Support", callback_data="contact_support"),
                InlineKeyboardButton(text="Usage Tips", callback_data="usage_tips"),
            ],
            [
                InlineKeyboardButton(text="⬅ Back", callback_data="back_to_main")
            ],
        ]
    )
    return keyboard

# Help functionality
@router.callback_query(lambda c: c.data == "help")
async def show_help(callback: CallbackQuery):
    await callback.message.edit_text(HELP_MESSAGE, reply_markup=help_menu())

# Function to register handlers
def register_help_handlers(dp):
    dp.include_router(router)
