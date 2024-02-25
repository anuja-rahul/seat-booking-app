from abc import ABCMeta, abstractmethod, ABC
from python_datalogger import DataLogger


class IBookingHandler(metaclass=ABCMeta):
    @abstractmethod
    def print_data(self):
        """Implemented in child class"""


class BookingHandler(IBookingHandler, ABC):
    __instance = None

    @staticmethod
    def get_instance():
        if BookingHandler.__instance is None:
            BookingHandler()
        return BookingHandler.__instance

    def __init__(self, name: str = "TestUser"):
        self.__logger = DataLogger(name="BookingHandler", propagate=True, level="DEBUG")

        if BookingHandler.__instance is not None:
            raise Exception("Cannot be instantiated more than once")
        else:
            self.__name = name
            BookingHandler.__instance = self

    @staticmethod
    def print_data(**kwargs):
        print(BookingHandler.__instance.__name)
