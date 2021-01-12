from aiogram import Bot, types
from aiogram.dispatcher import Dispacher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispacher(bot)

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
	executor.start_polling(dp)
