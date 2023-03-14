"""
Reference: https://docs.python-guide.org/writing/logging/
Structured logging reference: https://github.com/madzak/python-json-logger  
"""
import logging
import os

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def parse(self):
        return self._fmt.split(";")

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["status"] = log_record.get("levelname")
        if not log_record.get("service"):
            log_record["service"] = os.getenv("IMAGENAME", "name-not-found")


def get_logger(name, level=logging.DEBUG):
    """Sets up a json logger.

    Parameters
    ----------
    name : str
        The module name: `logger = logger.get_logger(__name__)`
    level : int, optional
        Set the logging level, by default logging.DEBUG
    version : int, optional
        Python version, by default get_python_version()

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    log_handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        "asctime;levelname;message;filename;lineno", validate=False
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.propagate = True
    return logger
