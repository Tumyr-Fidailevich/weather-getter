from requests.exceptions import *


class UserInputException(Exception):
    def __init__(self):
        super().__init__("User input exception occurred")


if __name__ == "__main__":
    pass
