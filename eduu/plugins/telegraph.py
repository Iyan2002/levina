from pyrogram.types import Message
from pyrogram import Client, filters

from ..config import prefix
from ..utils import commands, http
from ..utils.localization import use_chat_lang


@Client.on_message(filters.command(["telegraph", "tgm"], prefix))
@use_chat_lang()
async def telegraph(c: Client, m: Message, strings):
    if m.reply_to_message.text:
        await c.send_message(
            m.chat.id, strings("text_not_supported")
            )
        return
    if m.reply_to_message:
        if (
            m.reply_to_message.photo
            or m.reply_to_message.video
            or m.reply_to_message.animation
        ):
            msg = await c.send_message(
                m.chat.id, strings("telegraph_upload_load")
            )
            tg_file = await m.reply_to_message.download()
            response = await http.post(
                "https://telegra.ph/upload", files={"upload-file": open(tg_file, "rb")}
            )
            tele_link = "https://telegra.ph" + response.json()[0]["src"]
            return await msg.edit_text(
                strings("telegraph_upload_done").format(url=tele_link)
            )
    else:
        await m.reply_text(strings("telegraph_err_no_reply"))


commands.add_command("telegraph", "tools")