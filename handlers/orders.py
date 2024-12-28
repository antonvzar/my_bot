from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

cart = []

def back_to_main_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Back", callback_data="back_to_main")
    return builder.as_markup()

@router.callback_query(lambda c: c.data == "place_order")
async def place_order(callback: CallbackQuery):
    if cart:
        await callback.message.edit_text(
            "Thank you for your order! We will contact you shortly.",
            reply_markup=back_to_main_button()
        )
        cart.clear()
    else:
        await callback.message.edit_text(
            "Your cart is empty. Please add items before placing an order.",
            reply_markup=back_to_main_button()
        )


def register_order_handlers(dp):
    dp.include_router(router)