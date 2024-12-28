from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from firebase_config import db
import time

router = Router()

# Command to add a new item with separated Brand and Series
@router.message(Command("additem"))
async def add_item_via_bot(message: Message):
    try:
        # Split the user's message into arguments
        args = message.text.split(maxsplit=4)

        # Ensure the correct number of arguments is provided
        if len(args) != 5:
            await message.answer("Usage: /additem <category> <brand> <series> <price>")
            return

        category, brand, series, price = args[1], args[2], args[3], args[4]

        # Validate price
        try:
            price = float(price)
        except ValueError:
            await message.answer("❌ Invalid price. Please enter a valid number.")
            return

        # Generate a unique item ID based on time
        item_id = f"item{int(time.time())}"
        
        # Reference to the specific category in Firebase
        ref = db.reference(f"categories/{category}/{item_id}")
        
        # Save the new item in the database
        ref.set({
            "brand": brand,
            "series": series,
            "price": price
        })

        await message.answer(f"✅ Item added:\n- Category: {category}\n- Brand: {brand}\n- Series: {series}\n- Price: ${price}")
    except Exception as e:
        await message.answer(f"❌ Failed to add item. Error: {e}")
        print(f"Error adding item: {e}")
