from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.errors import UsernameNotOccupied

from ...config import prefix, sudoers
from ...utils import commands, get_target_user
from ...utils.consts import admin_status
from ...utils.decorators import require_admin
from ...utils.localization import use_chat_lang


@Client.on_message(filters.command("del", prefix))
@use_chat_lang()
@require_admin(permissions=["can_delete_messages"])
async def FuncDelMessage(c: Client, m: Message, strings):
    if not m.reply_to_message:
        return await m.reply_text(strings("rep_messageto_delete"))
    await m.reply_to_message.delete()
    await m.delete()


@Client.on_message(filters.command("wipe", prefix))
@use_chat_lang()
@require_admin(permissions=["can_restrict_members"])
async def FuncDelGhost(c: Client, m: Message, strings):
    chat_id = m.chat.id
    users_delete = []
    users_banned = 0
    msg = await m.reply_text(strings("clean_ghost_process"))

    async for i in c.get_chat_members(chat_id):
        if i.user.is_deleted:
            users_delete.append(i.user.id)
    if len(users_delete) > 0:
        for deleted_user in users_delete:
            try:
                await m.chat.ban_member(deleted_user)
            except Exception:
                pass
            users_banned += 1
        await msg.edit_text(strings("banned_ghost_acc").format(total=users_banned))
    else:
        await msg.edit_text(strings("no_ghost_exist"))



commands.add_command("del", "admin")
commands.add_command("wipe", "admin")
