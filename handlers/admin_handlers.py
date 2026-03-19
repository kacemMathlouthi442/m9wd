from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import get_admin
from utils import set_user_value, show_valid_keys, generate_bulk_keys

def keys_type():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="1 Day", callback_data="1 day"),
        InlineKeyboardButton(text="2 Days", callback_data="2 days")],
        [InlineKeyboardButton(text="1 Week", callback_data="1 week"),
        InlineKeyboardButton(text="1 Month", callback_data="1 month")],
        [InlineKeyboardButton(text="3 Months", callback_data="3 months")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]])

async def ban_command(message: Message):
    if message.from_user.id != 6974962502: return
    parts = message.text.split()
    if len(parts)<2: return
    await set_user_value(int(parts[1]), 'banned', True)
    await message.answer(f"User {parts[1]} banned ✅")

async def unban_command(message: Message):
    if message.from_user.id != 6974962502: return
    parts = message.text.split()
    if len(parts)<2: return
    await set_user_value(int(parts[1]), 'banned', False)
    await message.answer(f"User {parts[1]} unbanned ✅")

async def keys_command(message: Message):
    if message.from_user.id not in get_admin()['id']: return
    await message.answer("🔑 Select the keys type.",reply_markup=keys_type())

async def keys_callback(callback:CallbackQuery):
    if callback.from_user.id not in get_admin()['id']: return
    await callback.message.delete()
    await callback.message.answer("🔑 Select the keys type.",reply_markup=keys_type())

async def get_keys_callback(callback:CallbackQuery):
    if callback.from_user.id not in get_admin()['id']: return
    await callback.message.delete()
    await callback.message.answer("\n".join(await show_valid_keys(callback.data)),parse_mode='MarkdownV2')

async def generate_keys_callback(callback:CallbackQuery):
    if callback.from_user.id != 6974962502: return
    await callback.message.delete()
    await callback.message.answer("⏳ Generating keys...")
    await callback.message.answer(await generate_bulk_keys())

async def generate_keys_command(message: Message):
    if message.from_user.id != 6974962502: return
    await message.answer("⏳ Generating keys...")
    await message.answer(await generate_bulk_keys())
