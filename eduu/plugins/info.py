import html

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import BadRequest, UserNotParticipant

from ..config import prefix
from ..utils import commands
from ..utils.localization import use_chat_lang


@Client.on_message(filters.command("info", prefix))
@use_chat_lang()
async def user_info(c: Client, m: Message, strings):
    if len(m.command) == 2:
        try:
            user = await c.get_users(
                int(m.command[1]) if m.command[1].isdecimal() else m.command[1]
            )
        except BadRequest:
            return await m.reply_text(
                strings("user_not_found").format(user=m.command[1])
            )
    elif m.reply_to_message:
        user = m.reply_to_message.from_user
    else:
        user = m.from_user

    text = strings("info_header")
    text += strings("info_id").format(id=user.id)
    text += strings("info_first_name").format(first_name=html.escape(user.first_name))

    if user.last_name:
        text += strings("info_last_name").format(last_name=html.escape(user.last_name))

    if user.username:
        text += strings("info_username").format(username=html.escape(user.username))
        
    if user.language_code:
        text += strings("info_user_lang").format(user_lang=html.escape(user.language_code))

    text += strings("info_userlink").format(tap_here=user.mention("tap_here", style="html"))

    try:
        member = await m.chat.get_member(user.id)
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            text += strings("info_chat_admin")
        elif member.status == ChatMemberStatus.OWNER:
            text += strings("info_chat_owner")
        elif member.status == ChatMemberStatus.LEFT:
            text += strings("info_chat_left")
        elif member.status == ChatMemberStatus.BANNED:
            text += strings("info_chat_banned")
        elif member.status == ChatMemberStatus.RESTRICTED:
            text += strings("info_chat_restricted")
    except (UserNotParticipant, ValueError):
        pass

    await m.reply_text(text)


commands.add_command("info", "tools")
