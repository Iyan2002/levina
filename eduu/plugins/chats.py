from pyrogram import Client
from pyrogram.types import Message

from eduu.utils import add_chat, chat_exists


@Client.on_message(group=-1)
async def check_chat(c: Client, m: Message):
    # task: message.chat.id & message.chat.type
    chat_id = m.chat.id
    chat_type = m.chat.type
    # task: run function to add chat into database
    if not chat_exists(chat_id, chat_type):
        add_chat(chat_id, chat_type)
