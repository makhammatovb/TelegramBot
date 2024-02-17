import requests
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram.utils.chat_action import ChatActionSender
from datetime import datetime, timedelta

from config import currencies, CBU_URL

command_router = Router()


@command_router.message(CommandStart())
async def start_handler(message: Message):
    s = "Welcome to <b>currency converter bot</b>\n"
    s += "For more information select /help command\n"
    await message.answer(text=s, reply_markup=ReplyKeyboardRemove())


@command_router.message(Command('help', prefix='!/#'))
async def help_handler(message: Message):
    s = "For using this bot use these commands:\n\n"
    s += "/courses - to get all courses\n"
    s += "/usd - to get <b>USD</b> course\n"
    s += "/eur - to get <b>Euro</b> courses\n"
    s += "/rub - to get <b>Ruble</b> course\n"
    s += "/week - to get this <b>Week's</b> courses\n"

    s += "If you want to convert <b>Uzbek</b> sums, send the amount (only digits)"

    await message.reply(text=s)


@command_router.message(Command('courses', prefix='!/#'))
async def course_handler(message: Message):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.from_user.id):
        response = requests.get(CBU_URL)

        s = "Today's currency rates: \n\n"

        for course in response.json():
            if course['Ccy'] in currencies.keys():
                currencies[course['Ccy']]['rate'] = course['Rate']
                s += f"\t- 1 {course['CcyNm_EN']} is {course['Rate']} sums\n"
        s += '\n\n'
        await message.answer(text=s)


@command_router.message(Command('usd', prefix='!/#$'))
async def usd_handler(message: Message):
    response = requests.get(f"{CBU_URL}USD/")
    res = response.json()[0]
    s = f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    await message.reply(s)


@command_router.message(Command('eur', prefix='!/#'))
async def eur_handler(message: Message):
    response = requests.get(f"{CBU_URL}EUR/")
    res = response.json()[0]
    s = f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    await message.reply(s)


@command_router.message(Command('rub', prefix='!/#'))
async def rub_handler(message: Message):
    response = requests.get(f"{CBU_URL}RUB/")
    res = response.json()[0]
    s = f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    await message.reply(s)


@command_router.message(Command('week', prefix='!/#'))
async def week_handler(message: Message):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.from_user.id):
        today = datetime.now().date()

        # Calculate the start and end dates of the current week
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

        start_date_str = start_date.strftime("%d.%m.%Y")
        end_date_str = end_date.strftime("%d.%m.%Y")

        url = f"{CBU_URL}?date_req1={start_date_str}&date_req2={end_date_str}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            s = f"Currency rates for the week ({start_date_str} to {end_date_str}):\n\n"

            if data:
                for course in data:
                    if course['Ccy'] in currencies.keys():
                        currencies[course['Ccy']]['rate'] = course['Rate']
                        s += f"\t- 1 {course['CcyNm_EN']} is {course['Rate']} sums\n"
            else:
                s = "No currency rates available for the week."
        else:
            s = "Failed to retrieve currency rates for the week."

        s += '\n\n'
        await message.answer(text=s)
