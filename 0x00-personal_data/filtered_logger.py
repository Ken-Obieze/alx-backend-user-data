#!/usr/bin/env python3
"""Filter logger Module."""
import logging
import re
import csv
import os
import mysql.connector
import datetime
from typing import List
from filtered_logger import RedactingFormatter, filter_datum

PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def get_logger() -> logging.Logger:
    """Get logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger

def read_user_data(filename: str) -> List[dict]:
    """Read user data."""
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        user_data = list(reader)

    return user_data

def get_db():
    """Database connection."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    db_connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return db_connection

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialise class."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format for log."""
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, log_message, self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Create filter."""
    for field in fields:
        replace = "{}={}{}".format(field, redaction, separator)
        message = re.sub("{}=.*?{}".format(field, separator), replace, message)
    return message

def main():
    """Configure logger."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s')
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    db = get_db()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    logger.info("Filtered fields:\n\nname\nemail\nphone\nssn\npassword\n")

    for row in rows:
        filtered_row = "; ".join(f"{field}={filter_datum(['name', 'email', 'phone', 'ssn', 'password'], '***', str(value), ';')}" for field, value in zip(cursor.column_names, row))
        logger.info(filtered_row)

    cursor.close()
    db.close()

if __name__ == '__main__':
    main()
