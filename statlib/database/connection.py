import os
import functools

import pymysql
from pymysql.cursors import Cursor

from dotenv import load_dotenv; load_dotenv()


def _get_database_credentials() -> tuple[str, str, str, str]:
    """
    Load database credentials from environment variables.

    :return: Tuple containing (username, password, database name, endpoint).
    """
    db_username = os.getenv('DBUSER')
    db_password = os.getenv('DBPASS')
    db_name = os.getenv('DBNAME')
    db_endpoint = os.getenv('DBENDPOINT')
    
    return db_username, db_password, db_name, db_endpoint


def db_connect():
    """
    Create a new connection to the database using environment variables.

    :return: A PyMySQL connection object with autocommit enabled.
    """
    db_username, db_password, db_name, db_endpoint = _get_database_credentials()
    conn = pymysql.connect(
        host=db_endpoint,
        port=3306,
        user=db_username,
        password=db_password,
        database=db_name,
        autocommit=True
    )
    return conn


def ensure_cursor(func):
    """
    Decorator that ensures a database cursor is available for the wrapped function.

    If a `cursor` keyword argument is provided, it is reused.
    Otherwise, a new database connection and cursor are created.

    :param func: The function to wrap. Must accept a `cursor` keyword argument.
    :return: Wrapped function with a guaranteed cursor.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cursor: Cursor | None = kwargs.get('cursor')
        if cursor:
            return func(*args, **kwargs)

        with db_connect() as conn:
            conn.autocommit = True
            cursor = conn.cursor()
            kwargs['cursor'] = cursor
            return func(*args, **kwargs)

    return wrapper


def async_ensure_cursor(func):
    """
    Async decorator that ensures a database cursor is available for the coroutine.

    If a `cursor` keyword argument is provided, it is reused.
    Otherwise, a new database connection and cursor are created.

    :param func: The coroutine function to wrap. Must accept a `cursor` keyword argument.
    :return: Wrapped coroutine with a guaranteed cursor.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        cursor: Cursor | None = kwargs.get('cursor')
        if cursor:
            return await func(*args, **kwargs)

        with db_connect() as conn:
            conn.autocommit = True
            cursor = conn.cursor()
            kwargs['cursor'] = cursor
            return await func(*args, **kwargs)

    return wrapper