from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import TOKEN
from handlers.start import register_start_handlers
from handlers.categories import register_category_handlers
from handlers.cart import register_cart_handlers
from handlers.orders import register_order_handlers
from handlers.help import register_help_handlers
from handlers.admin import router as admin_router

# initialisation
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# router defining
dp.include_router(admin_router)

# handlers defining
register_start_handlers(dp)
register_category_handlers(dp)
register_cart_handlers(dp)
register_order_handlers(dp)
register_help_handlers(dp)

# installation
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
