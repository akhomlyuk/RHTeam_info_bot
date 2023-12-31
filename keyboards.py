from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def del_msg_btn():
    del_kb_markup = InlineKeyboardMarkup(row_width=1)
    del_btn = InlineKeyboardButton(text='🗑️', callback_data='delete_message')
    del_kb_markup.add(del_btn)
    return del_kb_markup


async def url_buttons(message: types.Message):
    kb_buttons = InlineKeyboardMarkup(row_width=2)
    url_button = InlineKeyboardButton(text='⚙️ RHT github', url='https://github.com/RedHazzarTeam-CODEBY-GAMES/')
    url_button2 = InlineKeyboardButton(text='🃏  RHT ctftime', url='https://ctftime.org/team/186788')
    url_button3 = InlineKeyboardButton(text='🏁  RHT flagbot', url='tg://resolve?domain=rhtflagsbot')
    url_button4 = InlineKeyboardButton(text='☎️  RHT Discord', url='https://discord.gg/52amEYzC')
    kb_buttons.add(url_button, url_button2, url_button3, url_button4)
    await message.answer('🔖 Полезные ссылки:\n', reply_markup=kb_buttons)


async def menu_buttons(message: types.Message):
    kb_buttons = InlineKeyboardMarkup(row_width=2)
    info_btn = InlineKeyboardButton(text='📰  Информация', callback_data='info_data')
    results_btn = InlineKeyboardButton(text='🏆  Результаты', callback_data='results_data')
    todo_btn = InlineKeyboardButton(text='📝  Список дел', callback_data='todo_data')
    flagbot_btn = InlineKeyboardButton(text='🤖  Флаг бот', callback_data='flagbot_data')
    brief_btn = InlineKeyboardButton(text='📣  Брифинг', callback_data='brief_data')
    links_btn = InlineKeyboardButton(text='💬  Ссылки', callback_data='links_data')
    top_teams_ru_btn = InlineKeyboardButton(text='🇷🇺  Top RU', callback_data='top_ru_data')
    next_btn = InlineKeyboardButton(text='🔜 След. ивент', callback_data='next_event_data')
    blacklist_btn = InlineKeyboardButton(text='👎 Blacklist', callback_data='blacklist_data')
    proxy_btn = InlineKeyboardButton(text='⚙️ Proxy', callback_data='proxy_data')
    kb_buttons.add(brief_btn, results_btn, info_btn, flagbot_btn, links_btn,
                   top_teams_ru_btn, todo_btn, next_btn, blacklist_btn, proxy_btn)
    await message.answer('📌 Меню 📌', reply_markup=kb_buttons, disable_notification=True)
