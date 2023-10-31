from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any
from .config import SECONDS_IN_HOUR


@dataclass
class Weather:
    """
    Dataclass for weather
    """
    time: datetime
    city_name: str
    weather_conditions: str
    current_temp: int
    feels_like_temp: int
    wind_speed: int

    def __iter__(self):
        return iter(asdict(self))

    def __getitem__(self, item):
        return getattr(self, item)

    def __str__(self):
        return f"Current time: {self.time}\n" \
               f"City name: {self.city_name}\n" \
               f"Weather conditions: {self.weather_conditions}\n" \
               f"Current temperature: {self.current_temp} degrees Celsius\n" \
               f"Feels like: {self.feels_like_temp} degrees Celsius\n" \
               f"Wind speed: {self.wind_speed} m/s"

    @classmethod
    def get_fields(cls) -> dict[str: Any]:
        return cls.__annotations__

    @staticmethod
    def get_sqlite_type(python_type: int | str | datetime) -> str:
        """
        Converts python data type to sql type.
        :param python_type: python type.
        :return: sql data type.
        """
        if python_type is int:
            return "INTEGER"
        elif python_type is str:
            return "TEXT"
        elif python_type is datetime:
            return "TIME"

    @classmethod
    def get_weather_by_api_response(cls, api_response: dict[str: Any]):
        """

        :param api_response: api response from get_response function.
        :return: Instance of the Weather class.
        """
        response_list = list()
        current_timezone = timezone(
            timedelta(hours=api_response["timezone"] / SECONDS_IN_HOUR,
                      minutes=api_response["timezone"] % SECONDS_IN_HOUR))
        response_list.append(datetime.fromtimestamp(api_response["dt"], tz=current_timezone))
        response_list.append(api_response["name"])
        response_list.append(api_response["weather"][0]["description"])
        response_list.append(round(api_response["main"]["temp"]))
        response_list.append(round(api_response["main"]["feels_like"]))
        response_list.append(round(api_response["wind"]["speed"]))

        return cls(*response_list)
