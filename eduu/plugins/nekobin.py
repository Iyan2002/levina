import os
import re
import aiofiles

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message

from ..config import prefix
from ..utils import commands
from ..utils.localization import use_chat_lang


aiohttpsession = ClientSession()

async def post(url: str, *args, **kwargs):
    async with aiohttpsession.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data

BASE = "https://batbin.me/"

async def paste(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return BASE + resp["message"]


@Client.on_message(filters.command("paste", prefix))
@use_chat_lang(context="pastes")
async def nekobin(c: Client, m: Message, strings):
    if not m.reply_to_message:
        return await m.reply_text(strings("reply_to_document_or_text"))

    r = m.reply_to_message

    if not r.text and not r.document:
        return await m.reply_text(
            strings("supported_text_document")
        )

    msg = await m.reply_text(strings("paste_upload_process"))

    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await msg.edit_text(strings("paste_file_limit"))
        if not pattern.search(r.document.mime_type):
            return await msg.edit_text(strings("paste_text_only"))

        doc = await m.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    url = await paste(content)
    try:
        if m.from_user.is_bot:
            await m.reply_photo(
                photo=url,
                quote=False,
            )
        else:
            await m.reply_photo(
                photo=url,
                quote=False,
                caption=f"🔗 {url}",
            )
        await msg.delete()
    except Exception:
        await msg.edit_text(f"🔗 {url}")


commands.add_command("paste", "tools", "nekobin_description", context_location="pastes")