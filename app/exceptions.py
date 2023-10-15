class UserInputException(Exception):
    """
    Basic user input exception.
    """
    def __init__(self, message):
        """
        :param message: Message sent to the user.
        """
        super().__init__(message)


class UnknownCityName(UserInputException):
    """
    Exception that occurs when the city name is entered incorrectly.
    """
    def __init__(self):
        super().__init__("Cannot find this city, try another")


class UnknownCommand(UserInputException):
    """
    Exception that occurs when an invalid command is entered.
    """
    def __init__(self):
        super().__init__("Unsupported command. Type -h for help")


class InvalidBodyRequest(UserInputException):
    """
    Exception that occurs when an invalid request body is entered.
    """
    def __init__(self):
        super().__init__("Invalid request body")
