import sys
import asyncio
import logging
import platform

from pyrogram import idle

from .bot import Eduu
from .utils import http
from .database import database


logging.basicConfig(
    level=logging.INFO,
    format="%(name)s.%(funcName)s | %(levelname)s | %(message)s",
    datefmt="[%X]",
)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

try:
    import uvloop

    uvloop.install()
except ImportError:
    if platform.system() != "Windows":
        logger.warning("uvloop is not installed and therefore will be disabled.")


async def main():
    eduu = Eduu()

    try:
        # start the bot
        await database.connect()
        await eduu.start()

        if "test" not in sys.argv:
            await idle()
    except KeyboardInterrupt:
        # exit gracefully
        logger.warning("Forced stop, Bye!")
    finally:
        # close https connections and the DB if open
        await eduu.stop()
        await http.aclose()
        if database.is_connected:
            await database.close()


if __name__ == "__main__":
    # open new asyncio event loop
    add_event_loop = asyncio.get_event_loop_policy()
    set_event_loop = add_event_loop.new_event_loop()
    asyncio.set_event_loop(set_event_loop)

    # start the bot
    set_event_loop.run_until_complete(main())

    # close asyncio event loop
    set_event_loop.close()
