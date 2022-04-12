from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from eduu.utils import add_chat, chat_exists
from eduu.utils.localization import use_chat_lang


@Client.on_message(group=-1)
async def check_chat(c: Client, m: Message):
    # task: message.chat.id & message.chat.type
    chat_id = m.chat.id
    chat_type = m.chat.type
    # task: run function to add chat into database
    if not chat_exists(chat_id, chat_type):
        add_chat(chat_id, chat_type)


@Client.on_message(filters.new_chat_members)
@use_chat_lang()
async def new_chat(c: Client, m: Message, strings):
    chat_id = m.chat.id

    for new in m.new_chat_members:
        keyboard_1 = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        strings("channel_button_txt"), url="https://t.me/levinachannel",
                    ),
                    InlineKeyboardButton(
                        strings("support_button_txt"), url="https://t.me/VeezSupportGroup",
                    )
                ],
            ]
        )
        keyboard_2 = InlineKeyboardMarkup(
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        strings("language_button_txt"), callback_data="chlang",
                    ),
                    InlineKeyboardButton(
                        strings("commands_button_txt"), url="https://t.me/GroupsGuardRobot?start=help",
                    )
                ],
            ]
        )
        
        try:
            if new.id == c.id:
                return await m.reply_text(
                    strings("greetings_add_chat"), reply_markup=keyboard_1
                )
            return await m.reply_text(
                strings("introducing_usages"), reply_markup=keyboard_2
            )
        except Exception:
            return
