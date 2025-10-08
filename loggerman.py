import structlog
import sys
import logging

from structlog.dev import ConsoleRenderer
from structlog.stdlib import ProcessorFormatter
# logging.basicConfig(
#    format="%(message)s",
#    level=logging.DEBUG,
# )

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.INFO
LOG_FILE = "KTAU.log"

# structlog.configure(
#    processors=[
#        structlog.processors.TimeStamper(fmt="iso"),
#        structlog.processors.add_log_level,
#        structlog.stdlib.add_logger_name,
#        structlog.dev.ConsoleRenderer(),
#    ],
#    logger_factory=structlog.stdlib.LoggerFactory(),
#    cache_logger_on_first_use=True,
# )
# logger = structlog.get_logger(__name__)


class Logger:
    def __init__(self, logger_name: str = __name__):
        self.logger_name = logger_name
        self._logger = self._setup_logger()

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

        stdlib_logger = logging.getLogger(self.logger_name)
        stdlib_logger.setLevel(logging.DEBUG)
        stdlib_logger.addHandler(console_handler)

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

        return structlog.get_logger(self.logger_name)

    def get_logger(self):
        return self._logger


logger = Logger(__name__).get_logger()


def test_logger():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("An exception occurred")
