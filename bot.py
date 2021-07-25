import asyncio
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from datetime import datetime
import os
from setup_db import KVStorage

from services.epic_free_games import epicfreegames
from services.apkmirror import apkmirror
import service_twitor
import service_rss_reader
import service_leekduck


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
    await message.reply("pong")


@dp.message_handler(commands=["pong"])
async def pong_command(message: types.Message):
    await message.reply("ping")

# ############## TASKS ####################


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

            if boss[2]:
                requests.post('https://pogotools.pythonanywhere.com/08332471770749258', data=boss[0])
                await bot.send_message(chat, boss[0])

            await bot.send_message(chat, rsch[0]) if rsch[1] else ""
    await asyncio.sleep(700)
    await post_tweets()


async def check_apk_update():
    apps = [
        "niantic-inc/pokemon-go",
        "the-pokemon-company/pokemon-home"
    ]

    for app in apps:
        apk = apkmirror.ApkMirror(app)
        apk.parse()
        text = "".join([
            f"New #update for {apk.app_title()}\n",
            f"Update version is {apk.version()}\n",
            f"Download links:\n-> {apk.link()} <-"
        ])

        app_title = apk.app_title().replace(" ", "")
        try:
            kvs = KVStorage.select().where(KVStorage.key == app_title).get()
        except KVStorage.DoesNotExist:
            kvs = KVStorage(key=app_title, value="0")

        version = apk.version().replace(".", "")
        if(kvs.value < version):
            kvs.value = version
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
    epic = epicfreegames.EFG()
    nu = int(epic.next_update().timestamp())

    try:
        kvs = KVStorage.select().where(KVStorage.key == "epicgames").get()
    except KVStorage.DoesNotExist:
        kvs = KVStorage(key="epicgames", value="0")

    # явне краще не явного. ймовірно допоможе.
    if(int(kvs.value) != nu):
        kvs.value = nu
        kvs.save()
        await bot.send_message(privat_chat, f"{epic.get_games()}")

    slp = nu - datetime.utcnow().timestamp() + 60
    await asyncio.sleep(int(slp))
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
