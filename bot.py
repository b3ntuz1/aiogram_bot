from aiogram import Bot, types
from aiogram.dispatcher import Dispacher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispacher(bot)

# webhook settings
WEBHOOK_HOST = 'https://aiogram-bot.heroku.com'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

@dp.message_handler(command="start")
async def start_command(message: types.Message):
	await message.reply("Hello")

@dp.message_handler(command="ping")
async def ping_command(message: types.Message):
	await message.reply("pong")

@dp.message_handler(command="pong")
async def ping_command(message: types.Message):
	await message.reply("ping")

if __name__ == "__main__":
	# executor.start_polling(dp)
	start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
