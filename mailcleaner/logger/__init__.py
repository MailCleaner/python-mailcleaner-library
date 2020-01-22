import sys
import os
import logging
from logging import DEBUG, INFO, ERROR
from mailcleaner.config import MailCleanerConfig
import enum


class MCLogLevel(enum.Enum):
    """
    MailCleaner Enum for the level
    """
    critical = "50"
    error = "40"
    warning = "30"
    info = "20"
    debug = "10"


class McLogger(object):
    _mc_config = MailCleanerConfig.get_instance()
    loggers = set()

    def __init__(self,
                 name: str,
                 project: str = "",
                 filename: str = "",
                 path: str = "",
                 level=INFO):
        # Initial construct.
        self.format = "%(asctime)s | {} | %(levelname)s | %(message)s".format(
            name)

        if "LOG_LEVEL" in os.environ:
            self.level = int(os.environ["LOG_LEVEL"])
        else:
            self.level = level
        self.name = name
        if filename == "":
            filename = name
        if project != "":
            project = project + "/"

        #Testing path
        full_path = "{}/log/{}".format(
            self._mc_config.get_value("VARDIR"), project)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)

        # Logger configuration.
        self.console_formatter = logging.Formatter(self.format,
                                                   "%Y-%m-%d %H:%M:%S")
        self.console_logger = logging.FileHandler(
            "{}{}.log".format(full_path, filename))
        self.console_logger.setFormatter(self.console_formatter)

        self.logger = logging.getLogger(name)
        if name not in self.loggers:
            self.loggers.add(name)
            self.logger.setLevel(self.level)
            self.logger.addHandler(self.console_logger)

    def critical(self, msg, extra=None):
        self.logger.critical(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warning(msg, extra=extra)

    def warning(self, msg, extra=None):
        self.logger.warning(msg, extra=extra)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)
