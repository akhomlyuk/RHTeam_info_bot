from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from aiogram import Bot
from config import bot_token

bot = Bot(token=bot_token)


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()
