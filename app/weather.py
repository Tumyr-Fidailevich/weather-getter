from dataclasses import dataclass, asdict, fields
from datetime import datetime
from requests import Response


# TODO добавить описание класса
@dataclass
class Weather:
    time: datetime
    city_name: str
    weather_conditions: str
    current_temp: float
    feels_like_temp: float
    wind_speed: float

    def __iter__(self):
        return iter(asdict(self))

    def __getitem__(self, item):
        return getattr(self, item)

    # TODO добавить метод для отрисовки класса print(Weather)
    def __str__(self):
        pass

    @staticmethod
    def get_fields():
        return iter(fields(Weather))

    @staticmethod
    def get_sqlite_type(python_type):
        if python_type is int:
            return "INTEGER"
        elif python_type is float:
            return "REAL"
        elif python_type is str:
            return "TEXT"
        elif python_type is datetime:
            return "TIME"

    # TODO определить этот метод
    @classmethod
    def get_weather_by_api_response(cls, api_response: Response):
        response_dict = dict()
        response_dict.time = 10
        response_dict.city_name = "123"
        response_dict.weather_conditions = "123"
        response_dict.current_temp = 1
        response_dict.feels_like_temp = 2
        response_dict.wind_speed = 3

        return cls(*response_dict)
