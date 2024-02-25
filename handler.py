from abc import ABCMeta, abstractmethod, ABC
from python_datalogger import DataLogger

from dataserver import DataServer
from security import SecurityHandler


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

    def __init__(self, name: str = "TestUser", password: str = "password", row: str = None, column: str = None):
        self.__logger = DataLogger(name="BookingHandler", propagate=True, level="DEBUG")

        if BookingHandler.__instance is not None:
            raise Exception("Cannot be instantiated more than once")
        else:
            self.__name = name
            self.__password_hash = SecurityHandler(password=password).get_hashed_password()
            self.__row = row
            self.__column = column
            BookingHandler.__instance = self

    @staticmethod
    def print_data(**kwargs):
        print(BookingHandler.__instance.__name)

    def book_seat(self):
        if self.__row is not None and self.__column is not None:
            pass

    def change_booking(self):
        if self.__row is not None and self.__column is not None:
            pass

    def delete_booking(self):
        if self.__row is not None and self.__column is not None:
            pass

    @staticmethod
    def test_shit():
        DataServer()
