from pyrogram import Client, filters
from pyrogram.types import Message

from eduu.config import prefix, sudoers
from eduu.utils import commands
from eduu.utils.decorators import require_admin
from eduu.utils.localization import use_chat_lang


async def extract_userid(message, text: str):
    """
    NOT TO BE USED OUTSIDE THIS FILE
    """

    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        # if reply to a message and no reason is given
        if not reply.from_user:
            if (
                    reply.sender_chat
                    and reply.sender_chat != message.chat.id
                    and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    # if not reply to a message and no reason is given
    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    # if reason is given
    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


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
async def FuncPromoteMember(c: Client, message: Message, strings):
    user_id = await extract_user(message)
    user_tg = (await c.get_users(user_id)).mention
    if not user_id:
        return await message.reply_text(strings("user_is_null"))
    bot = await c.get_chat_member(message.chat.id, "5200427414")
    if user_id == "5200427414":
        return await message.reply_text(strings("cant_promote_self"))
    if not bot.can_promote_members:
        return await message.reply_text(strings("cant_promote_mems"))
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        )
        return await message.reply_text(strings("full_promote_done").format(user=user_tg))

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=bot.can_restrict_members,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_video_chats=False,
    )
    await message.reply_text(strings("regular_promote_done").format(user=user_tg))


@Client.on_message(filters.command("demote", prefix))
@use_chat_lang()
@require_admin(permissions=["can_promote_members"])
async def FuncDemoteMember(c: Client, message: Message, strings):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(strings("user_is_null"))
    if user_id == "5200427414":
        return await message.reply_text(strings("cant_demote_self"))
    if user_id in sudoers:
        return await message.reply_text(strings("sudo_is_special"))

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_video_chats=False,
    )
    person = (await c.get_users(user_id)).mention
    await message.reply_text(strings("demote_done").format(user=person))


commands.add_command("del", "admin")
commands.add_command("wipe", "admin")
commands.add_command("promote", "admin")
commands.add_command("fullpromote", "admin")
commands.add_command("demote", "admin")