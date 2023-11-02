#!/usr/bin/env python3
"""Filtered Logger."""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Replace occurrences of certain field values with the redaction string.

    Args:
        fields: List of strings representing fields to obfuscate.
        redaction: String representing the obfuscation value.
        message: String representing the log line.
        separator: String represent character separating fields in log line.

    Returns:
        The log message with obfuscated fields.
    """
    regex = '|'.join(map(re.escape, fields))
    return re.sub(f'({regex})=[^\\{separator}]*', f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        """Instantiation method, sets fields for each instance."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the LogRecord instanceFormats the LogRecord instance."""
        message = super().format(record)
        for field in self.fields:
            message = filter_datum([field], self.REDACTION, message, self.SEPARATOR)
        return message
