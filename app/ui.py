from enum import EnumMeta, StrEnum
from collections import namedtuple
from requests.exceptions import ConnectionError, Timeout, HTTPError
from .api import get_response
from .data_base import sqlite_connection, insert_response, get_latest_responses, get_all_responses, create_database, \
    drop_database
from .exceptions import InvalidBodyRequestError, UnknownCityNameError, UnknownCommandError, exception_handler
from .weather import Weather
from .config import DB_NAME


UserInput = namedtuple("UserInputRequest", ["command", "body"])


class CustomEnumMeta(EnumMeta):
    """
    Metaclass for overriding the in operator.
    """
    def __contains__(cls, item):
        return any(item == member.value for member in cls)


class Command(StrEnum, metaclass=CustomEnumMeta):
    """
    Enum class for user input.
    """
    REQUEST = "-r"
    LIST = "-l"
    ALL = "-a"
    CLEAR = "-c"
    QUIT = "-q"
    HELP = "-h"


@exception_handler(UnknownCommandError, UnknownCityNameError, InvalidBodyRequestError)
def execute_app() -> None:
    """
    Starts the main application loop. The function handles exceptions.
    Also, when the application starts, a responses database is created.
    :return: None.
    :exception: No except.
    """
    with sqlite_connection(DB_NAME) as connection:
        create_database(connection)

    while True:
        try:
            command, body = get_input("Type your command-> ")
            match command:
                case Command.REQUEST:
                    request_response(body)
                case Command.LIST:
                    list_last_responses(body)
                case Command.ALL:
                    list_all_responses()
                case Command.CLEAR:
                    clear_responses()
                case Command.QUIT:
                    quit_app()
                case Command.HELP:
                    show_help()
        except ConnectionError as e:
            print("You have problems with your Internet connection")
        except (Timeout, HTTPError) as e:
            print("Problems with connection to api")
        except KeyboardInterrupt:
            exit()


def get_input(message_for_user: str) -> UserInput:
    """
    Receives user input and preprocesses it.
    @:param message_for_user: Message for the user.
    :return: Returns a tuple of strings, in which 1 string is the request type, the second is the request body.
    :exception: UnknownCommand.
    """
    user_input = input(message_for_user).split(maxsplit=1)
    command = user_input[0] if user_input else ""
    body = user_input[1] if len(user_input) > 1 else ""
    if command not in Command:
        raise UnknownCommandError
    return UserInput(command, body)


def request_response(city_name: str) -> None:
    """
    Sends a request to the api, receives a response from it.
    If no errors occur, displays the response to the user and inserts it into the database.
    :param city_name: name of city,
    :return: None.
    :exception: UnknownCityNameError, requests.exceptions.
    """
    weather = Weather.get_weather_by_api_response(get_response(city_name))
    print(weather)
    with sqlite_connection(DB_NAME) as connection:
        insert_response(connection, weather)


def list_last_responses(num_of_responses: str) -> None:
    """
    Prints the last n responses from the database if body can be converted to int.
    :param num_of_responses: number of responses user wants to display.
    :return: None.
    :exception: InvalidBodyRequestError.
    """
    with sqlite_connection(DB_NAME) as connection:
        if num_of_responses.isdigit() and not num_of_responses.startswith("0"):
            responses = get_latest_responses(connection, int(num_of_responses))
        else:
            raise InvalidBodyRequestError

    print_responses(responses)


def list_all_responses() -> None:
    """
    Prints the last responses from the database.
    :return: None.
    :exception: No except.
    """
    with sqlite_connection(DB_NAME) as connection:
        responses = get_all_responses(connection)

    print_responses(responses)


def print_responses(responses: list[Weather]) -> None:
    """
    Displays the processed response.
    :param responses: list of Weather dataclasses.
    :return: None.
    :exception: No except.
    """
    if not responses:
        print("Data base is empty")
        return

    for i in range(len(responses) - 1):
        print(responses[i])
        input("Press Enter for next -> ")
    print(responses[len(responses) - 1])


def clear_responses() -> None:
    """
    Calls a function that clears the database.
    :return: None.
    :exception: No except.
    """
    with sqlite_connection(DB_NAME) as connection:
        drop_database(connection)
    print("Responses cleared successfully")


def show_help() -> None:
    """
    Displays help on working with the application.
    :return: None.
    :exception: No except.
    """
    print("-r {city_name}: Get position by city name. To find out the local weather, leave the request body empty\n"
          "-l {last_requests}: Display the latest requests\n"
          "-a : Display all recent requests\n"
          "-с: Clears requests\n"
          "-q: Exits the program")


def quit_app() -> None:
    """
    Exits the application.
    :return: None.
    :exception: No except.
    """
    raise KeyboardInterrupt
