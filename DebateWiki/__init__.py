__version__ = "0.1.0-alpha.0"

# Constants
import logging
import sys

LOG_FORMAT = "%(asctime)s %(name)-18s %(levelname)-8s %(message)s"
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S %z]"

# Log Handlers
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
root_logger = logging.getLogger(__name__)
root_logger.addHandler(stream_handler)
