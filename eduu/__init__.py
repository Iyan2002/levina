"""GuardBot core package"""

from telegraph import Telegraph

__version__ = "1.0.2"

telegraph = Telegraph()
telegraph.create_account(short_name="GroupsGuardRobot")