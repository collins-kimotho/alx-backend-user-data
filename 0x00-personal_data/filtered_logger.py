#!/usr/bin/env python3

"""
Module that defines a function for obfuscating
specified fields in log messages.
"""

import re
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
