from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

cart = []  # Временная корзина

def back_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="Back", callback_data="back_to_main")
    return builder.as_markup()

@router.callback_query(lambda c: c.data == "cart")
async def view_cart(callback: CallbackQuery):
    if cart:  # Assuming `cart` is a global or shared variable
        items = "\\n".join([item.capitalize() for item in cart])
        await callback.message.edit_text(f"Your cart contains:\\n{items}", reply_markup=back_button())
    else:
        await callback.message.edit_text("Your cart is empty.", reply_markup=back_button())

# Back button to main menu
def back_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Back", callback_data="back_to_main")
    return builder.as_markup()

# Функция для регистрации обработчиков
def register_cart_handlers(dp):
    dp.include_router(router)
