import asyncio
import logging
import sys

import toml

import DebateWiki
from DebateWiki.exceptions import ArgumentNotFoundError
from DebateWiki.schemas import config_schema

logger = logging.getLogger(__name__)
root_logger = logger.parent


def start(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """
    if kwargs["log_level"]:
        # Set logger level
        level = logging.getLevelName(kwargs["log_level"].upper())
        root_logger.setLevel(level)
    else:
        root_logger.setLevel("INFO")
    # Config Loader
    try:
        if kwargs['config_file']:
            config = toml.load(kwargs["config_file"])
        else:
            raise ArgumentNotFoundError(message="--config argument not passed.")
    except FileNotFoundError:
        logger.error(
            "A config.toml file is required."
        )
        sys.exit()
    except ArgumentNotFoundError:
        logger.error(
            "--config argument is required."
        )
        sys.exit()

    # Override configs from config file with ones from cli
    if kwargs["log_level"]:
        config["api"]["log_level"] = kwargs["log_level"].upper()

    # Validate Config
    config_schema.validate(config)

    logger.info(f"Starting Debate Wiki: {DebateWiki.__version__}")

    # Faster Event Loop
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass


if __name__ == "__main__":
    start()
