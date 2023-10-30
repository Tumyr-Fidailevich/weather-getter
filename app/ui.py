from types import MappingProxyType
from .api import *
from .data_base import *
from exceptions import *
from enum import StrEnum
from datetime import datetime


class Command(StrEnum):
    """
    Enum class for user input.
    """
    REQUEST = "-r"
    LIST = "-l"
    ALL = "-a"
    CLEAR = "-c"
    QUIT = "-q"
    HELP = "-h"


def execute_app() -> None:
    """
    Starts the main application loop. The function handles exceptions.
    Also, when the application starts, a responses database is created.
    :return: None.
    :exception: No except.
    """
    with sqlite_connection() as connection:

        create_database(connection)
        while True:
            try:
                message_type, body = get_input("Type your command-> ")
                COMMAND_DISPATCH_DICT[Command(message_type)](body)
            except UnknownCommandError as e:
                print(e)
            except InvalidBodyRequestError as e:
                print(e)
            except UnknownCityNameError as e:
                print(e)
            except (ConnectTimeout, ReadTimeout) as e:
                print("You have problems with your Internet connection")
                print(e)
            except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
                print("Server problems")
                print(e)
            except KeyboardInterrupt:
                exit()


def get_input(message_for_user: str) -> (str, str):
    """
    Receives user input and preprocesses it.
    @:param message_for_user: Message for the user.
    :return: Returns a tuple of strings, in which 1 string is the request type, the second is the request body.
    :exception: UnknownCommand.
    """
    user_input = input(message_for_user).split(maxsplit=1)
    message_type = user_input[0] if user_input else ""
    body = user_input[1] if len(user_input) > 1 else ""

    if message_type not in Command:
        raise UnknownCommandError
    return message_type, body


def request_response(body: str) -> None:
    """
    Sends a request to the api, receives a response from it.
    If no errors occur, displays the response to the user and inserts it into the database.
    :param body:
    :return: None.
    :exception: UnknownCityName, requests.exceptions.
    """
    response = prepare_raw_response(get_response(body))
    print_response(response)
    insert_response(response)


def prepare_raw_response(response: dict[str: Any]) -> dict[str: Any]:
    """
    Prepares data for insertion into the database.
    :param: response: Raw response.
    :return: Prepared data.
    :exception: No except.
    """
    prepared_response = dict()
    prepared_response["time"] = datetime.fromtimestamp(response["dt"])
    prepared_response["city_name"] = response["name"]
    prepared_response["weather_conditions"] = response["weather"][0]["description"]
    prepared_response["current_temp"] = round(response["main"]["temp"] - TO_CELSIUS)
    prepared_response["feels_like_temp"] = round(response["main"]["feels_like"] - TO_CELSIUS)
    prepared_response["wind_speed"] = response["wind"]["speed"]
    return prepared_response


def list_last_responses(body: str) -> None:
    """
    Prints the last n responses from the database if body can be converted to int.
    :param body: Body of the request received from the user.
    :return: None.
    :exception: InvalidBodyRequest.
    """
    if body.isdigit() and int(body) >= 0:
        responses = get_latest_responses(int(body))
    elif not body:
        responses = get_latest_responses(0, list_all=True)
    else:
        raise InvalidBodyRequestError

    if len(responses) == 0:
        print("Data base is empty")
        return

    for i in range(len(responses) - 1):
        print_response(responses[i])
        input("Press Enter for next -> ")
    print_response(responses[len(responses) - 1])


def list_all_responses(body: str) -> None:
    """
    Prints the last responses from the database.
    :param body: Body of the request received from the user.
    :return: None.
    :exception: InvalidBodyRequest.
    """

    responses = get_latest_responses(0, list_all=True)
    if len(responses) == 0:
        print("Data base is empty")
        return

    for i in range(len(responses)):
        print_response(responses[i])
        print("----------------------")


def print_response(response: dict[str: Any]) -> None:
    """
    Displays the processed response.
    :param response: Processed request.
    :return: None.
    :exception: No except.
    """
    for key, value in response.items():
        print(ID_TO_NAMES[key].format(value))


def clear_responses(body: str) -> None:
    """
    Calls a function that clears the database.
    :param body: Body of the request received from the user.
    :return: None.
    :exception: No except.
    """
    drop_database()


def show_help(body: str) -> None:
    """
    Displays help on working with the application.
    :param body: Body of the request received from the user.
    :return: None.
    :exception: No except.
    """
    print("-r {city_name}: Get position by city name. To find out the local weather, leave the request body empty\n"
          "-l {last_requests}: Display the latest requests\n"
          "-a : Display all recent requests\n"
          "-с: Clears requests\n"
          "-q: Exits the program")


def quit_app(exit_status_code: str) -> None:
    """
    Exits the application.
    :param exit_status_code: A useless parameter for now.
    :return: None.
    :exception: No except.
    """
    raise SystemExit()


COMMAND_DISPATCH_DICT = MappingProxyType({
    Command.REQUEST: request_response,
    Command.LIST: list_last_responses,
    Command.ALL: list_all_responses,
    Command.CLEAR: clear_responses,
    Command.QUIT: quit_app,
    Command.HELP: show_help
})
