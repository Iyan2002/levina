import os.path

from typing import List, Optional


API_ID: int = 123456
API_HASH: str = "1a2b3c4d5e6f7g8h9i10j"
TOKEN: str = "12345:abcdefghijklmn"

log_chat: int = 12345
sudoers: List[int] = [12345, 12345]
super_sudoers: List[int] = [12345, 12345]

prefix: List[str] = ["/", "!", ".", "$", "-"]

disabled_plugins: List[str] = []

WORKERS = 24

DATABASE_PATH = os.path.join("eduu", "database", "eduu.db")

TENOR_API_KEY: Optional[str] = "X9HD35B7ZGP6"

sudoers.extend(super_sudoers)
