from pyrogram import Client
from pyrogram.types import Message

from eduu.database.chats import add_chat, chat_exists


@Client.on_message(group=-1)
async def check_chat(c: Client, m: Message):
    chat_id = m.chat.id
    chat_type = m.chat.type
    chatexists = await chat_exists(chat_id, chat_type)

    if not chatexists(chat_id, chat_type):
        await add_chat(chat_id, chat_type)
