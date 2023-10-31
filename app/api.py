from geocoder import ip
from requests import get
from typing import Any
from http import HTTPStatus
from exceptions import UnknownCityNameError
from config import API_CALL, API_KEY


def get_city_name_by_current_position() -> str:
    location = ip("me")
    return location.city


def get_response(city_name: str) -> dict[str: Any]:
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
    if request.status_code != HTTPStatus.OK:
        raise UnknownCityNameError
    request_data = request.json()
    return request_data
