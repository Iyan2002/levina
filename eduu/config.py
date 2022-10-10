import os.path

from typing import List, Optional


API_ID: int = 3487995
API_HASH: str = "7b9f1868c1e90b7408d48445f1e89603"
TOKEN: str = "5200427414:AAHT02y59QBp0X2qUcEGDcU0f4JK_iQoqzA"

log_chat: int = -1001306851903
sudoers: List[int] = [1757169682, 859229457]
super_sudoers: List[int] = [1757169682, 859229457]

prefix: List[str] = ["/", "!", ".", "$", "-"]

disabled_plugins: List[str] = []

WORKERS = 24

DATABASE_PATH = os.path.join("eduu", "database", "eduu.db")

TENOR_API_KEY: Optional[str] = "X9HD35B7ZGP6"

sudoers.extend(super_sudoers)