import sqlite3
from contextlib import contextmanager
from .weather_data_type import Weather


@contextmanager
def sqlite_connection(data_base_name: str):
    connection = sqlite3.connect(data_base_name)
    yield connection
    connection.commit()
    connection.close()


def insert_response(connection: sqlite3.Connection, response: Weather) -> None:
    """
    Inserts a preprocessed response into the database.
    :param connection: connection with database.
    :param response: Preprocessed response for the database.
    :return: None.

    :exception: No except.
    """
    cursor = connection.cursor()

    cursor.execute(
        f'INSERT INTO Weather ({response.get_fields()}) VALUES ({Weather.get_sqlite_type(response.get_fields())})',
        dict(response))


def get_latest_responses(connection: sqlite3.Connection, num_of_responses: int) -> list[Weather]:
    """
    Returns the latest responses in a prepared form.
    :param connection: connection with database.
    :param num_of_responses: Number of last requests.
    :param list_all: A key that allows you to display all responses at once.
    :return: Preprocessed response.
    :exception: No except.
    """
    cursor = connection.cursor()

    cursor.execute(
        "SELECT " + "".join(f"{field.name}, " for field in
                            Weather.get_fields()) + f"FROM Weather ORDER BY id DESC LIMIT {num_of_responses}")
    last_responses = cursor.fetchall()
    response_list = list()

    for response in last_responses:
        response_list.append(Weather(*response))

    return response_list


def get_all_responses(connection: sqlite3.Connection) -> list[Weather]:
    """
    Returns all responses Weather dataclasses.
    :param connection: connection with database.
    :return: list of Weather.
    :exception: No except.
    """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT " + "".join(f"{field.name}, " for field in
                            Weather.get_fields()) + f"FROM Weather ORDER BY id DESC")
    last_responses = cursor.fetchall()
    response_list = list()

    for response in last_responses:
        response_list.append(Weather(*response))

    return response_list


def create_database(connection: sqlite3.Connection) -> None:
    """
    Creates a database if it has not already been created.
    :param connection: connection with database.
    :return: None.
    :exception: No except.
    """
    cursor = connection.cursor()
    fields = "id INTEGER PRIMARY KEY AUTOINCREMENT, " + ", ".join(
        f"{field.name} {Weather.get_sqlite_type(field.type)}" for field in Weather.get_fields())
    cursor.execute(f"CREATE TABLE IF NOT EXISTS Weather ({fields})")


def drop_database(connection) -> None:
    """
    Drops the database if it exists.
    :param connection: connection with database.
    :return: None.
    :exception: No except.
    """
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Weather IF EXISTS')
