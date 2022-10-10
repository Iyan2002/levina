"""GuardBot core package"""

from subprocess import run

__version__ = "2.1.0"
__version_code__ = (
    run(["git", "rev-list", "--count", "HEAD"], capture_output=True)
    .stdout.decode()
    .strip()
    or "0"
)