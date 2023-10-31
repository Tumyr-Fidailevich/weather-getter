from geocoder import ip
from requests import get, exceptions
from typing import Any
from http import HTTPStatus
from .config import API_CALL, API_KEY
from datetime import datetime, timedelta, timezone


# TODO добавить докстринг
def get_city_name_by_current_position() -> str:
    """

    :return:
    """
    location = ip("me")
    return location.city


def get_response(city_name: str | None) -> dict[str: Any]:
    """
    Takes as input the name of the city or an empty string.
    If the string is empty, the city will be obtained based on the user's current location.
    :param city_name: name of the requested city.
    :return: json representation of the raw requested data.
    :exception: exceptions from requests.exceptions or UnknownCityNameError.
    """
    # TODO Пофиксить падение программы при некорректном теле запроса
    if not city_name:
        city_name = get_city_name_by_current_position()
    request = get(API_CALL.format(f"q={city_name}", API_KEY), timeout=5)
    request_data = request.json()
    return request_data

#
# if __name__ == "__main__":
#     print(dir(exceptions))
    # response = get_response("")
    # current_timezone = timezone(timedelta(hours=10800 / 3600, minutes=10800 % 3600))
    # current_time = datetime.fromtimestamp(1698773222, tz=current_timezone)
    # print(response)
    # print(current_time)
    # print(current_timezone)
