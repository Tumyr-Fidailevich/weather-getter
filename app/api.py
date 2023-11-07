from http import HTTPStatus
from typing import Any

from geocoder import ip
from requests import get

from .config import API_CALL, API_KEY
from .exceptions import UnknownCityNameError


def get_city_name_by_current_position() -> str:
    """
    Get city name by current position.
    :return: city name.
    """
    location = ip("me")
    if not location:
        raise UnknownCityNameError
    return location.city


def get_response(city_name: str | None) -> dict[str: Any]:
    """
    Takes as input the name of the city or an empty string.
    If the string is empty, the city will be obtained based on the user's current location.
    :param city_name: name of the requested city.
    :return: json representation of the raw requested data.
    :exception: exceptions from requests.exceptions or UnknownCityNameError.
    """
    if not city_name:
        city_name = get_city_name_by_current_position()
    request = get(API_CALL.format(f"q={city_name}", API_KEY), timeout=5)
    request_data = request.json()
    if request.status_code == HTTPStatus.NOT_FOUND:
        raise UnknownCityNameError
    return request_data
