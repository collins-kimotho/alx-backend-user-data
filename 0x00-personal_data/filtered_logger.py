#!/usr/bin/env python3

"""
Module that defines a logger with a RedactingFormatter to obfuscate sensitive
information in log messages.
"""
import os
import re
import logging
from typing import List

# Defining the fields in user_data.csv that are considered sensitive
PII_FIELDS = ("name", "email", "ssn", "password", "phone")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    """
    pattern = f"({'|'.join(fields)})=[^;{separator}]*"
    return re.sub(
        pattern,
        lambda match: match.group().split('=')[0] + f"={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for obfuscating sensitive information. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with specified fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating sensitive fields.
        """
        # Use filter_datum to obfuscate specified fields in the log message
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for user data.
    """
    # Create a logger named "user_data" with INFO level
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Prevent logs from propagating to other loggers

    # Create a StreamHandler with a RedactingFormatter
    # set up to redact PII_FIELDS
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the MySQLdatabase using credentials from environment variables.
    Returns a MySQLConnection object.
    """
    # Fetching environment variables for database credentials
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connecting to the database
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
