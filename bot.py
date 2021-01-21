import asyncio
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import os

import get_apk
import tweepy_app


loop = asyncio.get_event_loop()
bot = Bot(token=os.getenv("TG_TOKEN"), loop=loop)
dp = Dispatcher(bot)

# webhook settings
# WEBHOOK_HOST = 'https://83f71a7c2b84.ngrok.io'
WEBHOOK_HOST = 'https://aiogram-bot.herokuapp.com'
WEBHOOK_PATH = '/aiogram-bot'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))
# WEBAPP_HOST = 'localhost'
# WEBAPP_PORT = 5000


tw = tweepy_app.Twitor()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Hello")

@dp.message_handler(commands=["ping"])
async def ping_command(message: types.Message):
	await message.reply("pong")

@dp.message_handler(commands=["pong"])
async def ping_command(message: types.Message):
	await message.reply("ping")
	print(message)


async def post_tweets():
	twits = tw.getTweets()
	for t in twits:
		await bot.send_message('-1001311550479', t)
	await asyncio.sleep(900)
	await post_tweets()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass

if __name__ == "__main__":
	# executor.start_polling(dp)
	loop.create_task(post_tweets())
	start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
