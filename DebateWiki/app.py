import asyncio
import logging
import os
import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

import DebateWiki
from DebateWiki import config
from DebateWiki.schemas import config_schema
from DebateWiki.versions import v1

UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "propagate": False},
    },
}


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# Intercept everything at the root logger
logging.root.handlers = [InterceptHandler()]

# Remove every other logger's handlers
# and propagate to root logger
for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True

# Create App Instance
app = FastAPI(title="Debate Wiki", version=DebateWiki.__version__)

# Include Version Routers
app.include_router(v1.users.router)

# Mount Files
static_folder = "Frontend/dist/"
app.mount("/static", StaticFiles(directory=f"{static_folder}"), name="static")


@app.get("/", response_class=FileResponse)
def read_index(request: Request):
    index = f"{static_folder}/index.html"
    return FileResponse(index)


@app.get("/{catchall:path}", response_class=FileResponse)
def read_index(request: Request):
    path = request.path_params["catchall"]
    file = static_folder + path

    if os.path.exists(file):
        return FileResponse(file)

    index = f"{static_folder}/index.html"
    return FileResponse(index)


def start(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """

    # Override configs from config file with ones from cli
    if kwargs["log_level"]:
        config["api"]["log_level"] = kwargs["log_level"].upper()

    # Validate Config
    config_schema.validate(config)

    logger.configure(
        handlers=[{"sink": sys.stdout, "level": config["api"]["log_level"].upper()}]
    )

    logger.info(f"Starting Debate Wiki: {DebateWiki.__version__}")

    # Faster Event Loop
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

    register_tortoise(
        app,
        db_url=config["api"]["database_url"],
        modules={"models": ["DebateWiki.models", "aerich.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=5000,
        debug=config["api"]["debug"],
        log_config=UVICORN_LOGGING_CONFIG,
        log_level=config["api"]["log_level"].lower(),
    )


if __name__ == "__main__":
    start()
