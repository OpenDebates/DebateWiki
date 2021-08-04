__version__ = "0.1.0-alpha.0"

# Config Loader
import sys

import toml
from loguru import logger

from DebateWiki.exceptions import ArgumentNotFoundError

try:
    config = toml.load("config.toml")
except FileNotFoundError:
    logger.error("A config.toml file is required.")
    sys.exit()
except ArgumentNotFoundError:
    logger.error("--config argument is required.")
    sys.exit()
