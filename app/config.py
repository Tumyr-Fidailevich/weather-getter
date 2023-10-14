from os import getcwd, path
API_KEY = "123"
API_CALL = f"https://api.openweathermap.org/data/2.5/weather?lat={'lat'}&lon={'lon'}&appid={API_KEY}&lang=ru"
BASE_DIR = path.basename(getcwd())

if __name__ == "__main__":
    print(API_CALL.format())
