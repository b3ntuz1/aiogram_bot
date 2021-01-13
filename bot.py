import asyncio
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from config import TOKEN


loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, loop=loop)
dp = Dispatcher(bot)

# webhook settings
# WEBHOOK_HOST = 'https://d48b2f79236a.ngrok.io'
WEBHOOK_HOST = 'https://aiogram-bot.herokuapp.com'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Hello")

@dp.message_handler(commands=["ping"])
async def ping_command(message: types.Message):
	await message.reply("pong")

@dp.message_handler(commands=["pong"])
async def ping_command(message: types.Message):
	await message.reply("ping")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass

if __name__ == "__main__":
	# executor.start_polling(dp)
	start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
