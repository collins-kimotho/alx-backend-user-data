#!/usr/bin/env python3

"""
Module that defines a RedactingFormatter for logging, which obfuscates
sensitive fields in log messages.
"""

import re
import logging
from typing import List

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
