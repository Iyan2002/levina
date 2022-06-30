import telegraph.Telegraph

from pyrogram.types import Message
from pyrogram import Client, filters

from eduu.config import prefix
from eduu.utils import commands, http
from eduu.utils.localization import use_chat_lang


telegraph = Telegraph()
telegraph.create_account(short_name="GroupsGuardRobot")


@Client.on_message(filters.command(["telegraph", "tgm"], prefix))
@use_chat_lang()
async def telegraph(c: Client, m: Message, strings):
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
        if m.reply_to_message.text:
            if len(m.command) < 2:
                return await m.reply_text(strings("telegraph_text_example"))
            msg = await c.send_message(
                m.chat.id, strings("telegraph_upload_load")
            )
            name = m.text.split(None, 1)[1]
            page = telegraph.create_page(
                name, html_content=m.reply_to_message.text.html.replace("\n", "<br>")
            )
            return await msg.edit_text(
                strings("telegraph_upload_done").format(url={page['url']})
            )
    else:
        await m.reply_text(strings("telegraph_err_no_reply"))


commands.add_command("telegraph", "tools")