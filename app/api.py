from geocoder import ip, osm
from requests import Response, get
from config import *


def get_response(city_name: str) -> Response:
    """@:param city_name - correct city name or an empty string"""
    coordinates = dict()
    if city_name:
        response = osm(city_name).latlng()
    else:
        response = ip("me").latlng()
    coordinates["lat"], coordinates["lon"] = response.latlng
    request = API_CALL.format(lat=coordinates["lat"], lon=coordinates["lon"])
    return get(request)
