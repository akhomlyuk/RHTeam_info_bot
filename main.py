import asyncio
import threading
import logging
from webserver import app
from werkzeug.serving import run_simple
from contextlib import suppress
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text, BoundFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputFile
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
import wikipedia
from config import *
from functions import rht_best_res, rht_info, top_teams_ru
from brief import *

os.makedirs('logs', exist_ok=True)
os.makedirs('notes', exist_ok=True)
logging.basicConfig(level=logging.INFO, filename='logs/bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

rht_info = ic(rht_info())
rht_best = rht_best_res()
top_ru = top_teams_ru()


# @dp.message_handler(commands=['start', 'go', 'run'])
# async def cmd_start(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Results", "Info", 'Flagbot', 'Cmds', 'RHT-git']
#     keyboard.add(*buttons)
#     await message.answer("Choose action:", reply_markup=keyboard)


class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


@dp.message_handler(Text(equals=del_cmds, ignore_case=True))
async def delete_messsage(message: types.Message):
    # try:
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        if IsAdmin(message):
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()
        else:
            await bot.send_message(message.chat.id, f"Не достаточно прав для удаление сообщения")
    # except MessageCantBeDeleted:
    #     await bot.send_message(message.chat.id, f"Не достаточно прав на удаление сообщения")


@dp.message_handler(content_types=['new_chat_members'])
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    await bot.send_message(message.chat.id, f"Добро пожаловать в RHTeam 🖖, {new_member.mention}!")


@dp.message_handler(Text(equals=results_cmds, ignore_case=True))
async def rht_results(message: types.Message):
    await message.reply(f'''Best 9 results: {rht_best[1]} + CODEBY org(45.82) = <b>{rht_info["rating"]["2023"]["rating_points"]}</b>\n
{rht_best[2][0]}
{rht_best[2][1]}
{rht_best[2][2]}
{rht_best[2][3]}
{rht_best[2][4]}
{rht_best[2][5]}
{rht_best[2][6]}
{rht_best[2][7]}
{rht_best[2][8]}''', parse_mode='HTML')


@dp.message_handler(Text(equals=info_cmds, ignore_case=True))
async def rht_information(message: types.Message):
    rating_place = rht_info["rating"]["2023"]["rating_place"]
    await message.reply(f'''🌍 Worldwide position: <b>{rating_place}</b>
🇷🇺 RU position: <b>{rht_info["rating"]["2023"]["country_place"]}</b>
🎯 Rating points: <b>{rht_info["rating"]["2023"]["rating_points"]}</b>
🚩 Team ID: <b>{rht_info["id"]}</b>
https://ctftime.org/team/186788''', parse_mode='HTML')


@dp.message_handler(Text(equals=flag_cmds, ignore_case=True))
async def rht_flagbot(message: types.Message):
    flags_bot = '@rhtflagsbot'
    await message.reply(f'Flags bot here: {flags_bot}', parse_mode='HTML')


@dp.message_handler(Text(equals=user_id_cmds, ignore_case=True))
async def rht_get_userid(message: types.Message):
    await message.reply(f'Твой telegram ID: <b>{message.from_user.id}</b>', parse_mode='HTML')


@dp.message_handler(Text(equals=next_event_cmds, ignore_case=True))
async def rht_get_next_event(message: types.Message):
    with open('notes/next', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.reply(f'''{content}''', parse_mode='HTML')


@dp.message_handler(Text(equals=todo_cmds, ignore_case=True))
async def rht_todo(message: types.Message):
    await message.reply(todo, parse_mode='HTML')


@dp.message_handler(Text(equals=git_cmds, ignore_case=True))
async def rht_github(message: types.Message):
    rht_git = 'https://github.com/RedHazzarTeam-CODEBY-GAMES/'
    await message.reply(f'''{rht_git}
''', parse_mode='HTML')


@dp.message_handler(Text(equals=top_cmds, ignore_case=True))
async def rht_top_teams_ru(message: types.Message):
    nl = '\n'
    await message.reply(f'''🇷🇺🇷🇺🇷🇺
{nl.join(str(team) for team in top_ru)}
''', parse_mode='HTML')


@dp.message_handler(Text(startswith=wiki_cmds, ignore_case=True))
async def rht_art(message: types.Message):
    wikipedia.set_lang("ru")
    try:
        w = wikipedia.page(message.text[6:], auto_suggest=True)
        wiki_page = wikipedia.summary(message.text[6:], sentences=4, auto_suggest=True)
        wiki_url = w.url
        await message.reply(f'{wiki_page}\n{wiki_url}', disable_web_page_preview=True)
    except wikipedia.exceptions.PageError:
        await message.reply('Страницы на русском не существует :(')


@dp.message_handler(Text(equals=buttons_cmds, ignore_case=True))
async def url_buttons(message: types.Message):
    kb_buttons = InlineKeyboardMarkup(row_width=2)
    url_button = InlineKeyboardButton(text='⚙️ RHT github', url='https://github.com/RedHazzarTeam-CODEBY-GAMES/')
    url_button2 = InlineKeyboardButton(text='🃏  RHT ctftime', url='https://ctftime.org/team/186788')
    url_button3 = InlineKeyboardButton(text='🏁  RHT flagbot', url='tg://resolve?domain=rhtflagsbot')
    url_button4 = InlineKeyboardButton(text='☎️  RHT Discord', url='https://discord.gg/V6Ba8qf2')
    kb_buttons.add(url_button, url_button2, url_button3, url_button4)
    await message.answer('Полезные ссылки:\n', reply_markup=kb_buttons)


@dp.message_handler(Text(equals=brief_cmds, ignore_case=True))
async def rht_brief(message: types.Message):
    await message.reply(brief, parse_mode='HTML')


@dp.message_handler(Text(equals=ngrok_cmds, ignore_case=True))
async def rht_ngrok(message: types.Message):
    await message.reply(ngrok[0], parse_mode='HTML')


@dp.message_handler(Text(equals=commands_cmds, ignore_case=True))
async def rht_commands(message: types.Message):
    await message.reply(f'''📜 Information: <b>{' : '.join(str(c) for c in info_cmds)}</b>
📈 Results: <b>{' : '.join(str(c) for c in results_cmds)}</b>
🔖 Menu: <b>{' : '.join(str(c) for c in menu_cmds)}</b>
📝 Список дел: <b>{' : '.join(str(c) for c in todo_cmds)}</b>
🏁 Flag bot: <b>{' : '.join(str(c) for c in flag_cmds)}</b>
⚙️ RHT git: <b>{' : '.join(str(c) for c in git_cmds)}</b>
📌 URLs: <b>{' : '.join(str(c) for c in buttons_cmds)}</b>
👨‍🚀 Brief: <b>{' : '.join(str(c) for c in brief_cmds)}</b>
🔝 Top RU: <b>{' : '.join(str(c) for c in top_cmds)}</b>
📚 Wiki: <b>{' : '.join(str(c) for c in wiki_cmds)}</b> пример: !wiki linux
⛓ Ngrok: <b>{' : '.join(str(c) for c in ngrok_cmds)}</b>
⌨️ Commands: <b>{' : '.join(str(c) for c in commands_cmds)}</b>''', parse_mode='HTML')


@dp.message_handler(Text(equals=menu_cmds, ignore_case=True))
async def menu_buttons(message: types.Message):
    kb_buttons = InlineKeyboardMarkup(row_width=2)
    info_button = InlineKeyboardButton(text='📰  Информация', callback_data='info_data')
    results_button = InlineKeyboardButton(text='🏆  Результаты', callback_data='results_data')
    todo_button = InlineKeyboardButton(text='📝  Список дел', callback_data='todo_data')
    flagbot_button = InlineKeyboardButton(text='🤖  Флаг бот', callback_data='flagbot_data')
    brief_button = InlineKeyboardButton(text='📣  Брифинг', callback_data='brief_data')
    links_button = InlineKeyboardButton(text='💬  Ссылки', callback_data='links_data')
    top_teams_ru_button = InlineKeyboardButton(text='🇷🇺  Top RU', callback_data='top_ru_data')
    kb_buttons.add(brief_button, results_button, info_button, flagbot_button, links_button, top_teams_ru_button, todo_button)
    await message.answer('Меню', reply_markup=kb_buttons, disable_notification=True)


@dp.callback_query_handler(text="results_data")
async def results_data(callback: types.CallbackQuery):
    await callback.message.answer(f'''Best 9 results: {rht_best[1]} + CODEBY org(45.82) = <b>{rht_info["rating"]["2023"]["rating_points"]}</b>\n
{rht_best[2][0]}
{rht_best[2][1]}
{rht_best[2][2]}
{rht_best[2][3]}
{rht_best[2][4]}
{rht_best[2][5]}
{rht_best[2][6]}
{rht_best[2][7]}
{rht_best[2][8]}''', parse_mode='HTML')
    await callback.answer()


@dp.callback_query_handler(text="info_data")
async def info_data(callback: types.CallbackQuery):
    await callback.message.answer(f'''🌍 Worldwide position: <b>{rht_info["rating"]["2023"]["rating_place"]}</b>
🇷🇺 RU position: <b>{rht_info["rating"]["2023"]["country_place"]}</b>
🎯 Rating points: <b>{rht_info["rating"]["2023"]["rating_points"]}</b>
🚩 Team ID: <b>{rht_info["id"]}</b>
https://ctftime.org/team/186788''', parse_mode='HTML')
    await callback.answer()


@dp.callback_query_handler(text="flagbot_data")
async def flagbot_data(callback: types.CallbackQuery):
    flags_bot = '@rhtflagsbot'
    await callback.message.answer(f'Flags bot here: {flags_bot}', parse_mode='HTML')
    await callback.answer()


@dp.callback_query_handler(text="todo_data")
async def todo_data(callback: types.CallbackQuery):
    await callback.message.answer(todo, parse_mode='HTML')
    await callback.answer()


@dp.callback_query_handler(text="brief_data")
async def brief_data(callback: types.CallbackQuery):
    await callback.message.answer(brief, parse_mode='HTML')
    await callback.answer()


@dp.callback_query_handler(text="top_ru_data")
async def top_ru_data(callback: types.CallbackQuery):
    nl = '\n'
    await callback.message.answer(f'''🇷🇺🇷🇺🇷🇺
{nl.join(str(team) for team in top_ru)}
''', parse_mode='HTML')
    await callback.answer()


@dp.callback_query_handler(text="links_data")
async def links_data(callback: types.CallbackQuery):
    await callback.message.answer(f'''Ссылки:
⚙️ <a href="https://github.com/RedHazzarTeam-CODEBY-GAMES/">Github</a>
🃏 <a href="https://ctftime.org/team/186788">Ctftime</a>
🏁 <a href="tg://resolve?domain=rhtflagsbot">Flagbot</a>
☎️ <a href="https://discord.gg/V6Ba8qf2">Discord</a>
''', parse_mode='HTML', disable_web_page_preview=True)
    await callback.answer()


@dp.message_handler(Text(equals=send_photo_cmds, ignore_case=True))
async def bot_send_sticker(message: types.Message):
    photo = InputFile("last.png")
    # await bot.send_sticker(chat_id=message.chat.id, sticker=r"CAACAgIAAxkBAAEJxCVkurxNbi3yUph4ZkiSoRGWn_BmJAACSCgAAtDiSUtQy_QmRSmjai8E")
    # await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer_photo(photo, caption='Последний результат')


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    logging.error(f'Ошибка при обработке запроса {update}: {exception}')


async def main():
    await dp.start_polling(bot)


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


if __name__ == "__main__":
    # asyncio.run(main())
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    run_simple('0.0.0.0', 3000, app, use_reloader=True, threaded=True)
