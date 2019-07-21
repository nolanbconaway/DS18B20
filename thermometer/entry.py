"""Snapshot the temperature and write it to the database.

This is a command line tool, so run it like `python3 -m thermometer.entry`.
"""

import datetime
import os

import dotenv
import sqlalchemy

from .reader import get_temperature_strict


def main():
    """Entry main function."""
    dotenv.load_dotenv()

    # get temp
    degrees_fahrenheit = get_temperature_strict()

    # write to db
    conn = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI")).connect()
    conn.execute(
        "INSERT INTO snapshots (dttm_utc, fahrenheit) VALUES (%s, %s)",
        (datetime.datetime.utcnow(), degrees_fahrenheit),
    )
    conn.close()


if __name__ == "__main__":
    main()
