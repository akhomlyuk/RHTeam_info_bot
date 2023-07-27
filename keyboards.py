from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def del_msg_btn():
    del_kb_markup = InlineKeyboardMarkup(row_width=1)
    del_btn = InlineKeyboardButton(text='Удалить', callback_data='delete_message')
    del_kb_markup.add(del_btn)
    return del_kb_markup
