"""GuardBot core package"""

from subprocess import run
from telegraph import Telegraph

__version__ = "1.0.2"
__version_code__ = (
    run(["git", "rev-list", "--count", "HEAD"],
    capture_output=True).stdout.decode().strip() or "0"
)

telegraph = Telegraph()
telegraph.create_account(short_name="GroupsGuardRobot")