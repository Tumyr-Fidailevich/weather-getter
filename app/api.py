from geocoder import ip, osm
from requests import get
from typing import Any
from .exceptions import *
from .config import *
from http import HTTPStatus


def get_response(city_name: str) -> dict[str: Any]:
    """
    Takes as input the name of the city or an empty string.
    If the string is empty, the city will be obtained based on the user's current location.
    :param city_name: name of the requested city.
    :return: json representation of the raw requested data.
    :exception: exceptions from requests.exceptions or UnknownCityName.
    """
    if city_name:
        response = osm(city_name)
    else:
        response = ip("me")
        city_name = response.current_result.city
    if response.status_code != HTTPStatus.OK:
        raise UnknownCityName
    latitude, longitude = response.latlng
    request = get(API_CALL.format(latitude, longitude, API_KEY), timeout=5)
    request_data = request.json()
    request_data["name"] = city_name
    return request_data
