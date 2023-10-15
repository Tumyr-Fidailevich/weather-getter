from typing import List, Dict, Any
import sqlite3
from .config import *
from os import path


def insert_response(response: Dict[str, Any]) -> None:
    """
    Inserts a preprocessed response into the database.
    :param response: Preprocessed response for the database.
    :return: None.
    :exception: No except.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    fields = ", ".join(COLUMN_NAMES)
    values = ', '.join([':' + name for name in COLUMN_NAMES])

    cursor.execute(f'INSERT INTO Weather ({fields}) VALUES ({values})', response)

    connection.commit()
    connection.close()


def get_latest_responses(num_of_responses: int, list_all: bool = False) -> List[Dict[str, Any]]:
    """
    Returns the latest responses in a prepared form.
    :param num_of_responses: Number of last requests.
    :param list_all: A key that allows you to display all responses at once.
    :return: Preprocessed response.
    :exception: No except.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    if list_all:
        cursor.execute(
            "SELECT time, city_name, weather_conditions, "
            "current_temp, feels_like_temp, wind_speed FROM Weather ORDER BY id DESC")
    else:
        cursor.execute(
            f"SELECT time, city_name, weather_conditions, current_temp, "
            f"feels_like_temp, wind_speed FROM Weather ORDER BY id DESC LIMIT {num_of_responses}")

    last_responses = cursor.fetchall()
    connection.close()
    response_list = list()

    for response in last_responses:
        response_list.append(dict(zip(COLUMN_NAMES, response)))

    return response_list


def create_database() -> None:
    """
    Creates a database if it has not already been created.
    :return: None.
    :exception: No except.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    if not path.exists(DB_NAME):
        fields = "id INTEGER PRIMARY KEY AUTOINCREMENT, " + ", ".join(
            f"{column_name} {column_type}" for column_name, column_type in zip(COLUMN_NAMES, COLUMN_TYPES))
        cursor.execute(f"CREATE TABLE Weather ({fields})")
        connection.commit()
    connection.close()


def drop_database() -> None:
    """
    Drops the database if it exists.
    :return: None.
    :exception: No except.
    """
    if path.exists(DB_NAME):
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Weather')
        connection.commit()
        connection.close()
