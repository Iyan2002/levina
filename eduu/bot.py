import time
import logging

import pyrogram
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import BadRequest
from pyrogram.raw.all import layer

from . import __version__, __version_code__
from .config import API_HASH, API_ID, disabled_plugins, log_chat, TOKEN, WORKERS

logger = logging.getLogger(__name__)


class Eduu(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            name=name,
            app_version=f"GuardBot v{__version__}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
            parse_mode=ParseMode.HTML,
            workers=WORKERS,
            plugins=dict(root="eduu.plugins", exclude=disabled_plugins),
            sleep_threshold=180,
        )

    async def start(self):
        await super().start()

        self.start_time = time.time()

        logger.info(
            "GuardBot running with Pyrogram v%s (Layer %s) started on @%s. Hi!",
            pyrogram.__version__,
            layer,
            self.me.username,
        )

        from .database.restarted import del_restarted, get_restarted

        wr = await get_restarted()
        await del_restarted()

        start_message = (
            "✅ <b>GuardBot started!</b>\n\n"
            f"🔖 <b>Version:</b> <code>v{__version__} ({__version_code__})</code>\n"
            f"🔥 <b>Pyrogram:</b> <code>v{pyrogram.__version__}</code>"
        )

        try:
            await self.send_message(chat_id=log_chat, text=start_message)
            if wr:
                await self.edit_message_text(
                    wr[0], wr[1], text="Bot has rebooted!"
                )
        except BadRequest:
            logger.warning("Unable to send message to log_chat.")

    async def stop(self):
        await super().stop()
        logger.warning("GuardBot stopped, Bye!")
