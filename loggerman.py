import structlog
import sys
import logging

from structlog.dev import ConsoleRenderer
from structlog.stdlib import ProcessorFormatter

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.INFO
LOG_FILE = "KTAU.log"


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

        # Standar POython logging configuration
        stdlib_logger = logging.getLogger(self.logger_name)
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

        return structlog.get_logger(self.logger_name)

    def get_logger(self):
        return self._logger
