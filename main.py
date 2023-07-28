import logging
import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InputFile
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
import wikipedia
from keyboards import del_msg_btn, url_buttons, menu_buttons
from texts import *
from functions import rht_best_res, rht_info, top_teams_ru
from models import IsAdmin

os.makedirs('logs', exist_ok=True)
os.makedirs('notes', exist_ok=True)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

rht_info = rht_info()
rht_best = rht_best_res()
top_ru = top_teams_ru()


# Вызов inline кнопки удалить под сообщениями бота, кнопки в keyboards
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'delete_message')
async def delete_message(callback_query: types.CallbackQuery):
    message = callback_query.message
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        if IsAdmin(message):
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.answer_callback_query(callback_query.id)
        else:
            await bot.send_message(message.chat.id, "Недостаточно прав для удаления сообщения")


@dp.message_handler(Text(equals=del_cmds, ignore_case=True))
async def delete_messsage(message: types.Message):
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        if IsAdmin(message):
            await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.delete()
        else:
            await bot.send_message(message.chat.id, f"Не достаточно прав для удаление сообщения")


# Вызов кнопок меню, кнопки в keyboards
@dp.message_handler(Text(equals=menu_cmds, ignore_case=True))
async def handle_menu_buttons(message: types.Message):
    await menu_buttons(message)


@dp.message_handler(content_types=['new_chat_members'])
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    await bot.send_message(message.chat.id, f"Добро пожаловать в RHTeam 🖖, {new_member.mention}!")


@dp.message_handler(Text(equals=results_cmds, ignore_case=True))
async def rht_results(message: types.Message):
    await message.reply(top10_results, parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=info_cmds, ignore_case=True))
async def rht_information(message: types.Message):
    await message.reply(rht_summary, parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=flag_cmds, ignore_case=True))
async def rht_flagbot(message: types.Message):
    flags_bot = '@rhtflagsbot'
    await message.reply(f'Flags bot here: {flags_bot}', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=blacklist_cmds, ignore_case=True))
async def rht_get_blacklist(message: types.Message):
    with open('notes/blacklist', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.reply(f'''{content}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=user_id_cmds, ignore_case=True))
async def rht_get_userid(message: types.Message):
    user_id = message.from_user.id
    prem = message.from_user.is_premium
    await message.reply(f'ID: <b>{user_id}</b> Premium: <b>{prem}</b>', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=next_event_cmds, ignore_case=True))
async def rht_get_next_event(message: types.Message):
    with open('notes/next', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.reply(f'''{content}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=todo_cmds, ignore_case=True))
async def rht_todo(message: types.Message):
    with open('notes/todo', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.reply(f'''{content}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=git_cmds, ignore_case=True))
async def rht_github(message: types.Message):
    rht_git = 'https://github.com/RedHazzarTeam-CODEBY-GAMES/'
    await message.reply(f'''{rht_git}
''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=top_cmds, ignore_case=True))
async def rht_top_teams_ru(message: types.Message):
    nl = '\n'
    await message.reply(f'''🇷🇺🇷🇺🇷🇺
{nl.join(str(team) for team in top_ru)}
''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(startswith=wiki_cmds, ignore_case=True))
async def rht_art(message: types.Message):
    wikipedia.set_lang("ru")
    try:
        w = wikipedia.page(message.text[6:], auto_suggest=True)
        wiki_page = wikipedia.summary(message.text[6:], sentences=4, auto_suggest=True)
        wiki_url = w.url
        await message.reply(f'{wiki_page}\n{wiki_url}', disable_web_page_preview=True, reply_markup=await del_msg_btn())
    except wikipedia.exceptions.PageError:
        await message.reply('Страницы на русском не существует :(', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=buttons_cmds, ignore_case=True))
async def handle_url_buttons(message: types.Message):
    await url_buttons(message)


@dp.message_handler(Text(equals=brief_cmds, ignore_case=True))
async def rht_brief(message: types.Message):
    with open('notes/brief', encoding='UTF-8', newline='') as content:
        brief = content.read()
    await message.reply(f'''{brief}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=ngrok_cmds, ignore_case=True))
async def rht_ngrok(message: types.Message):
    await message.reply(ngrok[0], parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=commands_cmds, ignore_case=True))
async def rht_commands(message: types.Message):
    await message.reply(commands, parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.callback_query_handler(text="results_data")
async def results_data(callback: types.CallbackQuery):
    await callback.message.answer(top10_results, parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="info_data")
async def info_data(callback: types.CallbackQuery):
    await callback.message.answer(rht_summary, parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="flagbot_data")
async def flagbot_data(callback: types.CallbackQuery):
    flags_bot = '@rhtflagsbot'
    await callback.message.answer(f'Flags bot here: {flags_bot}', parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="todo_data")
async def todo_data(callback: types.CallbackQuery):
    with open('notes/todo', encoding='UTF-8', newline='') as todo:
        todo = todo.read()
    await callback.message.answer(todo, parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="brief_data")
async def brief_data(callback: types.CallbackQuery):
    with open('notes/brief', encoding='UTF-8', newline='') as content:
        brief = content.read()
    await callback.message.answer(f'''{brief}''', parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="next_event_data")
async def next_event_data(callback: types.CallbackQuery):
    with open('notes/next', encoding='UTF-8', newline='') as content:
        content = content.read()
    await callback.message.answer(content, parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="top_ru_data")
async def top_ru_data(callback: types.CallbackQuery):
    nl = '\n'
    await callback.message.answer(f'''🇷🇺🇷🇺🇷🇺
{nl.join(str(team) for team in top_ru)}
''', parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="links_data")
async def links_data(callback: types.CallbackQuery):
    await callback.message.answer(links, parse_mode='HTML', disable_web_page_preview=True, reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="blacklist_data")
async def blacklist_data(callback: types.CallbackQuery):
    with open('notes/blacklist', encoding='UTF-8', newline='') as content:
        bl = content.read()
    await callback.message.answer(bl, parse_mode='HTML', disable_web_page_preview=True, reply_markup=await del_msg_btn())
    await callback.answer()


@dp.message_handler(Text(equals=send_photo_cmds, ignore_case=True))
async def bot_send_sticker(message: types.Message):
    # photo = InputFile("last.png")
    cats = InputFile("static/sticker.webm")


    # await bot.send_sticker(chat_id=message.chat.id, sticker=r"CAACAgIAAxkBAAEJxCVkurxNbi3yUph4ZkiSoRGWn_BmJAACSCgAAtDiSUtQy_QmRSmjai8E")
    # await message.answer_photo(photo, caption='Последний результат', reply_markup=await del_msg_btn())
    await bot.send_animation(message.chat.id, cats)


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    logging.error(f'Ошибка при обработке запроса {update}: {exception}')


async def on_startup(dp):
    logging.info(dp)
    logging.info('RHTeam info bot starting...')


async def main():
    logging.info('Bot starting...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='logs/bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(main())
