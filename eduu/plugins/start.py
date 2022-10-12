from typing import Union

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from .. import __version__, __version_code__
from ..config import prefix
from ..utils import commands
from ..utils.localization import use_chat_lang


@Client.on_message(filters.command("start", prefix), group=2)
@Client.on_callback_query(filters.regex("^start_back$"))
@use_chat_lang()
async def start(c: Client, m: Union[Message, CallbackQuery], strings):
    if isinstance(m, CallbackQuery):
        await m.answer(strings("start_back_panel"))
        msg = m.message
        method = msg.edit_text
    else:
        msg = m
        method = msg.reply_text

    if msg.chat.type == ChatType.PRIVATE:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        strings("add_chat_btn"),
                        url=f"https://t.me/{c.me.username}?startgroup=new",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        strings("language_btn"), callback_data="chlang"
                    ),
                    InlineKeyboardButton(
                        strings("infos_btn"), callback_data="infos"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        strings("commands_btn"), callback_data="commands"
                    )
                ],
            ]
        )
        await method(strings("private"), reply_markup=keyboard, disable_web_page_preview=True)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        strings("start_chat"),
                        url=f"https://t.me/{c.me.username}?start=start",
                    )
                ]
            ]
        )
        await method(strings("group"), reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex("^support_info$"))
@use_chat_lang()
async def support_info(c: Client, m: CallbackQuery, strings):
    await m.answer(strings("support_panel"))
    res = strings("support_info_text")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    strings("back_info_btn", context="general"), callback_data="infos"
                )
            ]
        ]
    )
    await m.message.edit_text(res, reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex("^infos$"))
@use_chat_lang()
async def infos(c: Client, m: CallbackQuery, strings):
    await m.answer(strings("info_panel"))
    res = strings("info_page").format(
        version=__version__,
        version_code=__version_code__,
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    strings("back_btn", context="general"), callback_data="start_back"
                ),
                InlineKeyboardButton(
                    strings("support_info_btn", context="general"), callback_data="support_info"
                )
            ]
        ]
    )
    await m.message.edit_text(res, reply_markup=keyboard, disable_web_page_preview=True)


commands.add_command("start", "general")
