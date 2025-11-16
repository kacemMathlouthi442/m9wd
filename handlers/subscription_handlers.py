from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from utils import get_user_info, escape_markdown, check_subscription, redeem_key, get_wallet_message
from config import get_admin, get_groups
from aiogram import Bot

def subscription_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
         InlineKeyboardButton(text="🆘 Support", url=get_admin()['link'])]
    ])

def pricing_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📞 Support", url=get_admin()['link'])
            ],
            [
                InlineKeyboardButton(text="LTC", callback_data="ltc"),
                InlineKeyboardButton(text="USDT", callback_data="usdt")
            ],
            [
                
                InlineKeyboardButton(text="BTC", callback_data="btc")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )

def pricing_message():
    return r"""💬 Please select your desired plan.
                                                                                                       
  • 1 Day plan    ➜ 22$ + ( 60 PayPal logs + 5 CC gift )
  • 2 Days plan   ➜ 35$ + ( 150 Paypal logs + 10 CC gift )
  • 1 Week plan   ➜ 60$ + ( 1k Paypal logs + 30 CC gift )
  • 1 Month plan  ➜ 135$ + ( 5k Paypal logs + 60 CC gift )
  • 3 Months plan ➜ 600$ + ( 10k Paypal logs + 250 CC gift  )"""

def subscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]
    ])

def unsubscriber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Buy Now", callback_data="purchase")],
        [InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]
    ])

async def purchase_command(message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    await message.answer(pricing_message(), reply_markup=pricing_keyboard())

async def purchase_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    await callback.message.delete()
    await callback.message.answer(pricing_message(), reply_markup=pricing_keyboard())

async def my_profile_command(message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    if await get_user_info(user_id, 'expiry_date') == 'N/A':
        await message.answer("🚫 You didn't subscribe yet.",reply_markup=unsubscriber_keyboard())
        return
    if check_subscription(await get_user_info(user_id, 'expiry_date')) == True:
        expiry_date = await get_user_info(user_id, 'expiry_date')
        date = expiry_date[0:16]
        await message.answer("🕜 Your subscription expire in "+date, reply_markup=subscriber_keyboard())
        return
    await message.answer('🚫 Your subscription has expired.', reply_markup=unsubscriber_keyboard())

async def redeem_keys(message,bot:Bot):
    user_id = message.from_user.id
    if await get_user_info(user_id, 'banned'): return
    parts = message.text.split()
    if len(parts)<2:
        await message.answer("❌ No Activation Key\nUse /redeem <key> to activate your access.")
        return
    msg = await redeem_key(user_id, parts[1])
    await message.answer(msg)
    duration_text = msg[2:msg.find('K')-1]
    if message.from_user.username:
        username = "@"+message.from_user.username
    else:
        username = 'N/A'
    name = message.from_user.first_name
    await bot.send_message(chat_id=get_groups()['redeemed_keys_ID'],text=fr'''*Key For {duration_text}*
Redeemed by {escape_markdown(username)}
Name: `{escape_markdown(name)}`
Chat Id: `{user_id}`
Key: `{parts[1]}`''',parse_mode='MarkdownV2')

async def wallet_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned') == True: return
    symbol = callback.data
    await callback.message.delete()
    await callback.message.answer(get_wallet_message(symbol), reply_markup=subscription_keyboard(), parse_mode='MarkdownV2')