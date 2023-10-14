from typing import List, Dict, Any
import sqlite3
from config import *

DB_FILE_PATH = BASE_DIR // "weather.db"
ROWS_NAMES = ("id", "time", "city_name", "weather_conditions", "current_temp", "feels_like_temp", "wind_speed")


def insert_response(response: Dict[str, Any]) -> None:
    connection = sqlite3.connect(DB_FILE_PATH)
    cursor = connection.cursor()

    fields = ", ".join(ROWS_NAMES[1:])
    values = ', '.join([':' + name for name in ROWS_NAMES[1:]])

    cursor.execute(f'INSERT INTO Weather ({fields}) VALUES ({values})', response)

    connection.commit()
    connection.close()


def get_latest_responses(num_of_responses: int) -> List[Dict[str, Any]]:
    connection = sqlite3.connect(DB_FILE_PATH)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM Weather ORDER BY id DESC LIMIT {num_of_responses}")

    last_responses = cursor.fetchall()
    connection.close()

    response_list = list()

    for response in last_responses:
        response_list.append(dict(zip(ROWS_NAMES, response)))

    return response_list


def create_database() -> None:
    connection = sqlite3.connect(DB_FILE_PATH)
    cursor = connection.cursor()
    if not path.exists(DB_FILE_PATH):
        cursor.execute("""CREATE TABLE Weather
                 (id INTEGER PRIMARY KEY,
                 time TIME,
                 city_name TEXT,
                 weather_conditions TEXT,
                 current_temp REAL,
                 feels_like_temp REAL,
                 wind_speed REAL)""")
        connection.commit()
    connection.close()


def drop_database() -> None:
    if path.exists(DB_FILE_PATH):
        connection = sqlite3.connect(DB_FILE_PATH)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Weather')
        connection.commit()
        connection.close()
