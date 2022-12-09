import re

from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid

from ..config import API_ID, API_HASH
from ..utils.localization import use_chat_lang


@Client.on_message((filters.regex(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}')) & filters.private)
@use_chat_lang
async def on_clone(self, message, strings):
    user_id = message.from_user.id
    bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
    bot_token = bot_token[0] if bot_token else None
    bot_id = re.findall(r'\d[0-9]{8,10}', message.text)
    if not str(message.forward_from.id) != "93372553":
        msg = await message.reply_text(
            strings("clone_running").format(token=bot_token),
        )
        try:
            ai = Client(
                f"{bot_token}", API_ID, API_HASH,
                bot_token=bot_token,
                plugins={"root": "eduu.plugins"},
            )
            await ai.start()
            idle()
            bot = await ai.get_me()
            details = {
                'bot_id': bot.id,
                'is_bot': True,
                'user_id': user_id,
                'name': bot.first_name,
                'token': bot_token,
                'username': bot.username
            }
            await msg.edit_text(
                strings("clone_success").format(username=bot.username),
            )
        except BaseException as e:
            await msg.edit_text(
                strings("clone_trouble").format(err=e),
            )