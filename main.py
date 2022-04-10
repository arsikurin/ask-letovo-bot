import asyncio
import logging
import os

import aiorun
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=False), override=True)
TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_BOT_TOKEN, parse_mode="markdownv2")
dp = Dispatcher(bot)


@dp.message_handler(regexp="(?i).*(start|help)")
async def handle_start_help(message: types.Message):
    payload = f'{fn if (fn := message.from_user.first_name) else ""} {ln if (ln := message.from_user.last_name) else ""}'.strip()
    await message.answer(f"Greetings, *{payload}*\!")
    await message.answer("Ask me a question related to @LetovoAnalyticsBot\n_It will be resent to the developer_")


@dp.message_handler()
async def handle_messages(message: types.Message):
    await bot.forward_message(606336225, from_chat_id=message.from_user.id, message_id=message.message_id)
    await message.reply("Got it\!")


async def pinger():
    while True:
        logging.info("ping!")
        await asyncio.sleep(60 * 10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(pinger())
    aiorun.run(executor.start_polling(dp, skip_updates=False), use_uvloop=True)
