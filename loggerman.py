# Erick Gilmore 2025
# logerman its the man that manages the logging for this project

import structlog
import sys
import logging

from structlog.dev import ConsoleRenderer
from structlog.stdlib import ProcessorFormatter

# Configuration for logging

# TODO: change log levels based on environment (dev/prod)

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.INFO
LOG_FILE = "KTAU.log"


# Here we define a Logger class that sets up structured logging using structlog
# Its like the office for the loggerman, where he sets up everything and its manual of how write logs
class Logger:
    # initialize the logger with a name
    def __init__(self):
        self._setup_logger()

    # Function to setup the logger
    def _setup_logger(self):
        # Processors shared by all handlers
        shared_processors = [
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.format_exc_info,
            structlog.processors.StackInfoRenderer(),
        ]

        # Formatter for console output
        console_formatter = ProcessorFormatter(
            processor=ConsoleRenderer(),
            foreign_pre_chain=shared_processors,
        )

        # Handler for console output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(CONSOLE_LOG_LEVEL)

        # Standar Python logging configuration
        stdlib_logger = logging.getLogger()
        # Keep the root logger level to DEBUG, so all messages are processed
        stdlib_logger.setLevel(logging.DEBUG)
        # Add here the habdlers you need
        stdlib_logger.addHandler(console_handler)  # Console handler

        # TODO: Add Handler for file output

        structlog.configure(
            wrapper_class=structlog.stdlib.BoundLogger,
            processors=[
                structlog.stdlib.filter_by_level,
                *shared_processors,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )


# This is loggerman, he is the one who provides the logger instance
def loggerman(logger_name: str = __name__):
    return structlog.get_logger(logger_name)


# This is the loggerman office, here we create the singleton instance
_ = Logger()
