#!/usr/bin/env python3
"""
Filtered Logger
"""

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
        separator: String representing the character separating the fields
                   in the log line.

    Returns:
        The log message with obfuscated fields.
    """
    for key in fields:
        pattern = r'({0}=)[^{1}]*({1})'.format(key, separator)
        message = re.sub(pattern, r'\1{}\2'.format(redaction), message)
    return message
