from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Main menu with the "Help" button as the largest and at the bottom
def main_menu():
    # Create the keyboard layout
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Select Category", callback_data="select_category"),
                InlineKeyboardButton(text="Cart", callback_data="cart"),
                InlineKeyboardButton(text="Place Order", callback_data="place_order"),
            ],
            [
                InlineKeyboardButton(text="ℹ️ HELP", callback_data="help")  # Large Help button
            ],
        ]
    )
    return keyboard

# Handler for the /start command
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Welcome to our store! Please choose an option:", reply_markup=main_menu())

# Back to main menu functionality (if needed)
@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text("Welcome back to the main menu!", reply_markup=main_menu())


# Регистрация обработчиков
def register_start_handlers(dp):
    dp.include_router(router)



