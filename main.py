import logging
import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InputFile
import random
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
import wikipedia
from keyboards import del_msg_btn, url_buttons, menu_buttons
from texts import *
from functions import rht_best_res, rht_info, rating, hash_analyze
from models import IsAdmin

os.makedirs('logs', exist_ok=True)
os.makedirs('notes', exist_ok=True)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

rht_info = rht_info()
rht_best = rht_best_res()
# top_ru = top_teams_ru()


# Вызов inline кнопки удалить под сообщениями бота, кнопки в keyboards
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'delete_message')
async def delete_message(callback_query: types.CallbackQuery):
    message = callback_query.message
    try:
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            if IsAdmin(message):
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.answer_callback_query(callback_query.id)
            else:
                await bot.send_message(message.chat.id, "Недостаточно прав для удаления сообщения")
    except Exception as e:
        logging.warning(e)
        await message.answer(str(e))


@dp.message_handler(Text(equals=del_cmds, ignore_case=True))
async def delete_messsage(message: types.Message):
    try:
        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            if IsAdmin(message):
                await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                await message.delete()
            else:
                await bot.send_message(message.chat.id, f"Не достаточно прав для удаление сообщения")
    except Exception as e:
        logging.warning(e)
        await message.answer(str(e))


# Вызов кнопок меню, кнопки в keyboards
@dp.message_handler(Text(equals=menu_cmds, ignore_case=True))
async def handle_menu_buttons(message: types.Message):
    await menu_buttons(message)


@dp.message_handler(Text(equals=socks_cmds, ignore_case=True))
async def proxy_info(message: types.Message):
    await message.answer(dante_socks, parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(content_types=['new_chat_members'])
async def new_members_handler(message: Message):
    new_member = message.new_chat_members[0]
    await bot.send_message(message.chat.id, f"Добро пожаловать в RHTeam 🖖, {new_member.mention}!")


@dp.message_handler(Text(equals=results_cmds, ignore_case=True))
async def rht_results(message: types.Message):
    await message.answer(top10_results, parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=info_cmds, ignore_case=True))
async def rht_information(message: types.Message):
    await message.answer(rht_summary, parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=flag_cmds, ignore_case=True))
async def rht_flagbot(message: types.Message):
    flags_bot = '@rhtflagsbot'
    await message.answer(f'Flags bot here: {flags_bot}', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=blacklist_cmds, ignore_case=True))
async def rht_get_blacklist(message: types.Message):
    with open('notes/blacklist', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.answer(f'''{content}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=user_id_cmds, ignore_case=True))
async def rht_get_userid(message: types.Message):
    user_id = message.from_user.id
    prem = message.from_user.is_premium
    await message.answer(f'ID: <b>{user_id}</b> Premium: <b>{prem}</b>', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=next_event_cmds, ignore_case=True))
async def rht_get_next_event(message: types.Message):
    with open('notes/next', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.answer(f'''{content}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=todo_cmds, ignore_case=True))
async def rht_todo(message: types.Message):
    with open('notes/todo', encoding='UTF-8', newline='') as content:
        content = content.read()
    await message.answer(f'''{content}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=git_cmds, ignore_case=True))
async def rht_github(message: types.Message):
    rht_git = 'https://github.com/RedHazzarTeam-CODEBY-GAMES/'
    await message.answer(f'''{rht_git}
''', parse_mode='HTML', reply_markup=await del_msg_btn())


# @dp.message_handler(Text(equals=top_cmds, ignore_case=True))
# async def rht_top_teams_ru(message: types.Message):
#     nl = '\n'
#     await message.answer(f'''🇷🇺🇷🇺🇷🇺
# {nl.join(str(team) for team in top_ru)}
# ''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(startswith=wiki_cmds, ignore_case=True))
async def rht_art(message: types.Message):
    wikipedia.set_lang("ru")
    try:
        w = wikipedia.page(message.text[6:], auto_suggest=True)
        wiki_page = wikipedia.summary(message.text[6:], sentences=4, auto_suggest=True)
        wiki_url = w.url
        await message.answer(f'{wiki_page}\n{wiki_url}', disable_web_page_preview=True, reply_markup=await del_msg_btn())
    except wikipedia.exceptions.PageError:
        await message.answer('Страницы на русском не существует :(', reply_markup=await del_msg_btn())


@dp.message_handler(Text(startswith='!rate', ignore_case=True))
async def rht_rate(message: types.Message):
    try:
        w = message.text[6:].split(' ')
        w = [int(item) for item in w]
        result = round(rating(w), 3)
        await message.answer(f'Рейтинг на данный момент: <b>{result}</b>', parse_mode='HTML')
    except Exception as e:
        logging.warning(e)
        logging(e)
        await message.answer(str(e))


@dp.message_handler(Text(equals=buttons_cmds, ignore_case=True))
async def handle_url_buttons(message: types.Message):
    await url_buttons(message)


@dp.message_handler(Text(equals=brief_cmds, ignore_case=True))
async def rht_brief(message: types.Message):
    with open('notes/brief', encoding='UTF-8', newline='') as content:
        brief = content.read()
    await message.answer(f'''{brief}''', parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=ngrok_cmds, ignore_case=True))
async def rht_ngrok(message: types.Message):
    await message.answer(ngrok[0], parse_mode='HTML', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=commands_cmds, ignore_case=True))
async def rht_commands(message: types.Message):
    await message.answer(commands, parse_mode='HTML', reply_markup=await del_msg_btn())


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
    try:
        await callback.message.answer(f'Flags bot here: {flags_bot}', parse_mode='HTML', reply_markup=await del_msg_btn())
        await callback.answer()
    except Exception as e:
        logging(e)


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


# @dp.callback_query_handler(text="top_ru_data")
# async def top_ru_data(callback: types.CallbackQuery):
#     nl = '\n'
#     await callback.message.answer(f'''🇷🇺🇷🇺🇷🇺
# {nl.join(str(team) for team in top_ru)}
# ''', parse_mode='HTML', reply_markup=await del_msg_btn())
#     await callback.answer()


@dp.callback_query_handler(text="links_data")
async def links_data(callback: types.CallbackQuery):
    await callback.message.answer(links, parse_mode='HTML', disable_web_page_preview=True, reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="proxy_data")
async def proxy_data(callback: types.CallbackQuery):
    await callback.message.answer(dante_socks, parse_mode='HTML', reply_markup=await del_msg_btn())
    await callback.answer()


@dp.callback_query_handler(text="blacklist_data")
async def blacklist_data(callback: types.CallbackQuery):
    with open('notes/blacklist', encoding='UTF-8', newline='') as content:
        bl = content.read()
    await callback.message.answer(bl, parse_mode='HTML', disable_web_page_preview=True, reply_markup=await del_msg_btn())
    await callback.answer()


@dp.message_handler(Text(equals=send_photo_cmds, ignore_case=True))
async def bot_send_picture(message: types.Message):
    photo = InputFile("last.png")
    await message.answer_photo(photo, caption='Последний результат', reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals=send_gif_cmds, ignore_case=True))
async def bot_send_sticker(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEJ111kw-91FqVfDb307irgHaTtl8f1RgACDBUAAp6r-Uj_wGLs34VHvy8E')


@dp.message_handler(Text(equals=send_pzd_cmds, ignore_case=True))
async def bot_send_sticker(message: types.Message):
    await message.answer_sticker('CAACAgIAAxUAAWTGQH4UwxNH_WDAMyLMm_tDm4haAAKaLwACYqQxSrM6sLKvmqTYLwQ')


@dp.message_handler(Text(equals='!pzd2', ignore_case=True))
async def bot_send_sticker(message: types.Message):
    await message.answer_sticker('CAACAgIAAxUAAWTaEgABF6qmr1JJFDjaypM-SuWZcgACIzUAApo6yEqXMkvOzDYhxTAE')


@dp.message_handler(Text(equals=pandas_rng_cmds, ignore_case=True))
async def bot_send_sticker(message: types.Message):
    await message.answer_sticker(random.choice(pandas_rng), reply_markup=await del_msg_btn())


@dp.message_handler(Text(equals='!uptime', ignore_case=True))
async def uptime_info(message: Message):
    t = os.popen('uptime -p').read()[:-1]
    await message.answer(f'{t}')


@dp.message_handler(Text(startswith='!hash'))
async def hash_identify(message: types.Message):
    try:
        msg = message.text.split()
        if len(msg) == 1:
            await message.answer(f'Пример:\n<code>!hash a6105c0a611b41b08f1209506350279e</code>', parse_mode='html')
        else:
            hash_string = message.text[6:]
            text = f''''''
            for item in hash_analyze(hash_string):
                text += "<b>Hash type: </b>" + "<code>" + item['name'] + "</code>" + '\n'
                text += "<b>John format: </b>" + "<code>" + str(item['john']) + "</code>" + '\n'
                text += "<b>Hashcat format: </b>" + "<code>" + str(item['hashcat']) + "</code>" + '\n'
                text += "<b>Info: </b>" + "<code>" + str(item['description']) + "</code>" + '\n'
                text += "-" * 10 + "\n"
            await message.answer("Основные варианты:\n" + text, parse_mode='html')
    except Exception as e:
        logging.warning(e)
        logging(e)


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
