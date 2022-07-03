from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.errors import UsernameNotOccupied

from eduu.config import prefix, sudoers
from eduu.utils import commands, get_target_user
from eduu.utils.consts import admin_status
from eduu.utils.decorators import require_admin
from eduu.utils.localization import use_chat_lang


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


@Client.on_message(filters.command(["promote", "fullpromote"], prefix))
@use_chat_lang()
@require_admin(permissions=["can_promote_members"])
async def FuncPromoteMember(c: Client, m: Message, strings):
    target_user = await get_target_user(c, m)
    check_admin = await m.chat.get_member(target_user.id)

    if target_user.id == "5200427414":
        return await m.reply_text(strings("cant_promote_self"))
    if not c.can_promote_members:
        return await m.reply_text(strings("cant_promote_mems"))

    if check_admin.status not in admin_status:
        try:
            if m.command[0][0] == "f":
                await c.promote_chat_member(
                    m.chat.id,
                    user_id=target_user.id,
                    privileges=ChatPrivileges(
                        can_change_info=True,
                        can_invite_users=True,
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_pin_messages=True,
                        can_promote_members=True,
                        can_manage_chat=True,
                        can_manage_video_chats=True,
                    ),
                )
                return await m.reply_text(strings("full_promote_done").format(user=user_tg))
            else:
                await c.promote_chat_member(
                    m.chat.id,
                    user_id=target_user.id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=True,
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_pin_messages=False,
                        can_promote_members=False,
                        can_manage_chat=True,
                        can_manage_video_chats=False,
                    ),
                )
                return await m.reply_text(strings("regular_promote_done").format(user=user_tg))
        except UsernameNotOccupied:
            return await m.reply_text(strings("user_is_null"))
    else:
        return await m.reply_text(strings("user_is_author"))


@Client.on_message(filters.command("demote", prefix))
@use_chat_lang()
@require_admin(permissions=["can_promote_members"])
async def FuncDemoteMember(c: Client, m: Message, strings):
    target_user = await get_target_user(c, m)
    check_admin = await m.chat.get_member(target_user.id)

    if target_user.id == "5200427414":
        return await m.reply_text(strings("cant_demote_self"))
    if target_user.id in sudoers:
        return await m.reply_text(strings("sudo_is_special"))
    if not c.can_promote_members:
        return await m.reply_text(strings("cant_promote_mems"))
    
    if check_admin.status in admin_status:
        try:
            await c.promote_chat_member(
                m.chat.id,
                user_id=target_user.id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                ),
            )
            person = (await c.get_users(user_id)).mention
            return await m.reply_text(strings("demote_done").format(user=person))
        except UsernameNotOccupied:
            return await m.reply_text(strings("user_is_null"))
    else:
        return await m.reply_text(strings("user_isnot_author"))


commands.add_command("del", "admin")
commands.add_command("wipe", "admin")
commands.add_command("promote", "admin")
commands.add_command("fullpromote", "admin")
commands.add_command("demote", "admin")