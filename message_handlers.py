from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from config import currencies, CBU_URL

message_router = Router()


@message_router.message(F.text.isdigit())
async def exchange(message: Message):
    print(message.text, message.from_user.username, message.from_user.first_name)
    x = int(message.text)
    s = f"{x} sums: \n"
    s += f"\t- {x / currencies['USD']['rate']: .2f}US Dollars\n"
    s += f"\t- {x / currencies['EUR']['rate']: .2f}Euros\n"
    s += f"\t- {x / currencies['RUB']['rate']: .2f}Rubles\n\n"
    s += f"Currency rates are taken from <a href='{CBU_URL}'>CBU API </a>"
    await message.reply(
        text=s,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text='Source',
                    url=CBU_URL
                )
            ], [
                InlineKeyboardButton(
                    text='Author',
                    url=CBU_URL
                )
            ]]
        )
    )


@message_router.message(F.text)
async def usd_handler(message: Message):
    print(message.text, message.from_user.username, message.from_user.first_name)
    amount_str = ''.join(c for c in message.text if c.isdigit())
    if amount_str:
        x = int(amount_str)
        usd_rate = currencies['USD']['rate']
        s = f"${x} is approximately:\n"
        s += f"\t- {x * usd_rate:,.2f}Sums\n"
        s += f"Currency rates are taken from <a href='{CBU_URL}'>CBU API </a>"
        await message.reply(
            text=s,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Source',
                        url=CBU_URL
                    )
                ], [
                    InlineKeyboardButton(
                        text='Author',
                        url=CBU_URL
                    )
                ]]
            )
        )
