API_KEY = "f575323b7ca193b31f091bdf26e24abc"
API_CALL = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&lang=en"
TO_CELSIUS = 273.15

DB_NAME = "weather.db"
COLUMN_NAMES = ("time", "city_name", "weather_conditions", "current_temp", "feels_like_temp", "wind_speed")
COLUMN_TYPES = ("TIME", "TEXT", "TEXT", "REAL", "REAL", "REAL")
ID_TO_NAMES = {"time": "Current time: {}", "city_name": "City name: {}",
               "weather_conditions": "Weather conditions: {}",
               "current_temp": "Current temperature: {} degrees Celsius",
               "feels_like_temp": "Feels like: {} degrees Celsius", "wind_speed": "Wind speed: {} m/s"}
