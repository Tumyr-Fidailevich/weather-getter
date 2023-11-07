def exception_handler(*exceptions):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                print(e)
                wrapper(*args, **kwargs)
        return wrapper
    return decorator


class UserInputException(Exception):
    """
    Basic user input exception.
    """

    def __init__(self, message):
        """
        :param message: Message sent to the user.
        """
        super().__init__(message)


class UnknownCityNameError(UserInputException):
    """
    Exception that occurs when the city name is entered incorrectly.
    """

    def __init__(self):
        super().__init__("Cannot find this city, try another")


class UnknownCommandError(UserInputException):
    """
    Exception that occurs when an invalid command is entered.
    """

    def __init__(self):
        super().__init__("Unsupported command. Type -h for help")


class InvalidBodyRequestError(UserInputException):
    """
    Exception that occurs when an invalid request body is entered.
    """

    def __init__(self):
        super().__init__("Invalid request body")
