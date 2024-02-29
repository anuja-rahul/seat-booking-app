import uuid
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
            self.__uid = uuid.uuid4()
            self.__name = name
            self.__security = SecurityHandler(password=password)
            self.__password_hash = self.__security.get_hashed_password()
            self.__row = row
            self.__column = column
            self.__database = DataServer()
            BookingHandler.__instance = self

    @staticmethod
    def print_data(**kwargs):
        print(BookingHandler.__instance.__name)

    def __check_existing_user(self):
        sample_data = self.__database.execute(func=DataServer.read_user_specific_field(
            table_name='user_data',
            column='name',
            filter_expression=f"name='{self.__name}'"
        ),
            output=True
        )
        if len(sample_data) == 0:
            return False
        else:
            return True

    @DataLogger.logger
    def __check_credentials(self):
        if self.__check_existing_user():
            user_id = self.__database.execute(func=DataServer.read_user_specific_field(
                table_name='user_data',
                column='uid',
                filter_expression=f"name='{self.__name}'"
            ),
                output=True
            )

            user_id = user_id[0][0]

            user_creds = self.__database.execute(func=DataServer.read_user_specific_field(
                table_name='user_credentials',
                column='hash',
                filter_expression=f"uid='{user_id}'"
            ),
                output=True
            )

            creds_hash = user_creds[0][0]
            return self.__security.check_password_hashes(password_hash=creds_hash)

    def __validate_data(self):
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        columns = [num for num in range(1, 11)]

        if self.__row.upper() in rows and int(self.__column) in columns:
            return True
        else:
            return False

    def add_user(self):
        if not self.__check_existing_user():
            user_data_entry = [f"'{self.__uid}'", f"'{self.__name}'"]
            self.__database.execute(func=DataServer.create_row_query(
                table_name='user_data',
                data_list=user_data_entry
            ))

            user_creds_entry = [f"'{self.__uid}'", f"'{self.__password_hash}'"]
            self.__database.execute(func=DataServer.create_row_query(
                table_name='user_credentials',
                data_list=user_creds_entry
            ))
        else:
            raise Exception("\nUser already exists !\n")

    @DataLogger.logger
    def book_seat(self, row: str = None, column: str = None):
        if self.__check_existing_user() and self.__check_credentials():
            if row is not None and column is not None:
                self.__row = row
                self.__column = column

                if self.__validate_data():
                    user_booking_entry = [f"'{self.__uid}'", f"'{self.__row}'", f"'{self.__column}'"]
                    self.__database.execute(func=DataServer.create_row_query(
                        table_name='user_bookings',
                        data_list=user_booking_entry
                    ))
        else:
            raise Exception(f"\nUser credentials doesn't match !\n")

    def change_booking(self):
        if self.__check_existing_user() and self.__check_credentials():
            if self.__row is not None and self.__column is not None:
                if self.__validate_data():
                    pass
        else:
            raise Exception(f"\nUser credentials doesn't match !\n")

    def delete_booking(self):
        if self.__check_existing_user() and self.__check_credentials():
            if self.__row is not None and self.__column is not None:
                if self.__validate_data():
                    pass
        else:
            raise Exception(f"\nUser credentials doesn't match !\n")

    @staticmethod
    def test_shit():
        DataServer()
