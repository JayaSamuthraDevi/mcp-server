import logging
from pythonjsonlogger import jsonlogger
import sys

def setup_json_logging():
    log_handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = [log_handler]

    # Prevent duplicate logs
    root_logger.propagate = False

    return root_logger
