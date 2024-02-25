import sqlite3
from python_datalogger import DataLogger


class DataServer:

    local_db = {
        "database": "bookings.db"
    }

    def __init__(self, **kwargs):
        self.__logger = DataLogger(name="DataServer", propagate=False)
        self.__connect = sqlite3.connect(DataServer.local_db["database"])
        self.__cursor = self.__connect.cursor()
        self.__init_tables()
        super().__init__(**kwargs)

    def execute(self, func: any = None, output: bool = False) -> list:
        """
        Executes a SQL query based on user preference
        :param func: Specific SQL query
        :param output: boolean value of output choice (True or False)
        :return: if output is True, returns fetched results
        """

        if func is not None:
            self.__cursor.execute(func)
            self.__connect.commit()
            if output:
                return self.__cursor.fetchall()
        else:
            self.__logger.log_critical(f"param: func is not specified -> {func}")
            raise Exception(f"param: func is not specified -> {func}")

    def __init_tables(self) -> None:
        """
        Initiates all the necessary data tables
        :return: None
        """
        self.execute(self.default_user_setup())
        self.execute(self.default_user_booking_setup())
        self.execute(self.default_user_security_setup())

    @staticmethod
    def default_user_setup() -> str:
        """
        Query to initiate the  user_data table
        :return: user_data table SQL query
        """

        return """

            CREATE TABLE IF NOT EXISTS `user_data` ( 
            `uid` VARCHAR(200) NOT NULL , 
            `name` TEXT(200) NOT NULL);
            """

    @staticmethod
    def default_user_booking_setup() -> str:
        """
        Query to initiate the  user_bookings table
        :return: user_bookings table SQL query
        """

        return """

                CREATE TABLE IF NOT EXISTS `user_bookings` ( 
                `uid` VARCHAR(200) NOT NULL , 
                `row` TEXT(100) NOT NULL , 
                `column` TEXT(100) NOT NULL);
                """

    @staticmethod
    def default_user_security_setup() -> str:
        """
        Query to initiate the  user_credentials table
        :return: user_credentials table SQL query
        """

        return """

                CREATE TABLE IF NOT EXISTS `user_credentials` ( 
                `uid` VARCHAR(200) NOT NULL , 
                `hash` TEXT(200) NOT NULL);
                """