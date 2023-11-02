#!/usr/bin/env python3
"""Filtered Logger."""

import os
import logging
import mysql.connector
import re
from typing import List, Tuple

PII_FIELDS: Tuple[str]= ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = "; "

    def __init__(self, fields: list):
        """Set fields for each instance."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the LogRecord instanceFormats the LogRecord instance."""
        message = super().format(record)
        for field in self.fields:
            message = filter_datum([field], \
                self.REDACTION, message, self.SEPARATOR)
        return message



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



def get_logger():
    """Create and configures a logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """Connect to a mysql database."""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connection


def main():
    """Log database users."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        filtered_data = ""
        for field in PII_FIELDS:
            filtered_data += f"{field}={formatter.REDACTION}; "
        remaining_data = [f"{field}={value}" for field, value in zip(cursor.column_names, row)]
        log_message = f"{filtered_data}{'; '.join(remaining_data)}"
        logger.info(log_message)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
