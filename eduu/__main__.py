import sys
import time
import asyncio
import logging
import platform

import pyrogram
from pyrogram import Client, idle
from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest

import eduu
from eduu.utils import del_restarted, get_restarted, shell_exec
from eduu.config import API_HASH, API_ID, TOKEN, disabled_plugins, log_chat


try:
    import uvloop

    uvloop.install()
except ImportError:
    if platform.system() != "Windows":
        logging.warning("uvloop is not installed and therefore will be disabled.")


async def main() -> None:
    client = Client(
        name="bot",
        app_version=f"GuardBot v{eduu.__version__}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TOKEN,
        workers=24,
        parse_mode=ParseMode.HTML,
        plugins=dict(root="eduu.plugins", exclude=disabled_plugins),
    )

    await client.start()

    client.me = await client.get_me()
    client.start_time = time.time()
    if "test" not in sys.argv:
        wr = get_restarted()
        del_restarted()

        start_message = (
            "✅ <b>GuardBot started!</b>\n\n"
            f"🔖 <b>Version:</b> <code>v{eduu.__version__} (753)</code>\n"
            f"🔖 <b>Pyrogram:</b> <code>v{pyrogram.__version__}</code>"
        )

        try:
            await client.send_message(chat_id=log_chat, text=start_message)
            if wr:
                await client.edit_message_text(wr[0], wr[1], "Bot has rebooted!")
        except BadRequest:
            logging.warning("Unable to send message to log_chat.")

        await idle()

    await client.stop()


set_loop = asyncio.get_event_loop_policy()
new_event_loop = set_loop.new_event_loop()
new_event_loop.run_until_complete(main())
