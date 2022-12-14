import os.path

from typing import List, Optional


API_ID: int = insert_your_own_api_id_here
API_HASH: str = "insert_your_own_api_hash_here"
TOKEN: str = "insert_your_bot_token_here"

log_chat: int = insert_log_chat_id_here
sudoers: List[int] = [1757169682, 859229457]
super_sudoers: List[int] = [1757169682, 859229457]

prefix: List[str] = ["/", "!", ".", "$", "-"]

disabled_plugins: List[str] = []

WORKERS = 24

DATABASE_PATH = os.path.join("eduu", "database", "eduu.db")

TENOR_API_KEY: Optional[str] = "X9HD35B7ZGP6"

sudoers.extend(super_sudoers)

# notes

# 1. api_id & api_hash get from my.telegram.org
# 2. token fill with your bot_token get from @BotFather
# 3. log_chat fill with the chat id of a group that you should create for the bot logger
# 4. [optional] var disabled_plugins let you to disable an plugin to be loaded. Example:
# You don't want the youtube plugin to be loaded, then fill disabled_plugins var with youtube (or any name of the plugins file)