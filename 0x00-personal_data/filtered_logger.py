#!/usr/bin/env python3
"""Filtered Logger."""

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
