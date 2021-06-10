import asyncio
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import os

import service_apkmirror
import service_twitor
import service_rss_reader
import service_leekduck
import service_epicfreegames


loop = asyncio.get_event_loop()
bot = Bot(token=os.getenv("TG_TOKEN"), loop=loop)
dp = Dispatcher(bot)
privat_chat = '-1001311550479'
chat = "@pokenews_channel"

# webhook setting
# WEBHOOK_HOST = 'https://9aedfbbb9ab9.ngrok.io'
WEBHOOK_HOST = 'https://aiogram-bot.herokuapp.com'
WEBHOOK_PATH = '/aiogram-bot'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))
# WEBAPP_HOST = 'localhost'
# WEBAPP_PORT = 5000


tw = service_twitor.Twitor()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Hello")

@dp.message_handler(commands=["ping"])
async def ping_command(message: types.Message):
	print(message)
	await message.reply("pong")

@dp.message_handler(commands=["pong"])
async def ping_command(message: types.Message):
	await message.reply("ping")
	print(message)

############### TASKS ####################

async def post_tweets():
	twits = tw.getTweets()
	# print("Posting tweets...")
	for t in twits:
		if t[1] == "public":
			await bot.send_message(chat, t[0])
		else:
			await bot.send_message(privat_chat, t[0])

		if t[2] == "LeekDuck":
			boss = service_leekduck.get_raid_bosses()
			rsch = service_leekduck.get_research()

			await bot.send_message(chat, boss[0]) if boss[2] else ""
			await bot.send_message(chat, rsch[0]) if rsch[1] else ""
	await asyncio.sleep(700)
	await post_tweets()


async def check_apk_update():
	text = service_apkmirror.html_parse()
	# print("Check latest version...")
	if text != "":
		await bot.send_message(chat, text)
	await asyncio.sleep(7200)
	await check_apk_update()


async def check_rss():
	text = service_rss_reader.main()
	if(len(text) > 0):
		await bot.send_message(privat_chat, text)
	await asyncio.sleep(3600)
	await check_rss()

	
async def check_free_games():
	text = service_epicfreegames.service()
	if(text):
		await bot.send_message(privat_chat, text, parse_mode='MarkdownV2', disable_web_page_preview=False)
	print("check free games: not new")
	await asyncio.sleep(86400)
	await check_free_games()

##########################################

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # insert code here to run it before shutdown
    pass

if __name__ == "__main__":
	loop.create_task(post_tweets())
	loop.create_task(check_apk_update())
	loop.create_task(check_rss())
	loop.create_task(check_free_games())
	start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
