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

    @staticmethod
    def read_all_queries(table_name: str) -> str:
        """
        Reads all queries of a given table
        :param table_name: preferred table name
        :return: list of all the queries on the table
        """

        return f"""
            SELECT *
            FROM {table_name};
            """

    @staticmethod
    def read_user_data_fields(table_name: str, columns: str) -> str:
        """
        Reads a specific column of a given table
        :param table_name: preferred table name
        :param columns: required column(s)
        :return: list of a selected column
        """

        return f"""
            SELECT {columns}
            FROM {table_name};
            """

    @staticmethod
    def read_user_specific_field(table_name: str, filter_expression: str, column: str) -> str:
        """
        Reads a specific value from a column of a given table using filter expressions
        :param table_name: preferred table name
        :param filter_expression: expression to filter out a specific value
        :param column: required column
        :return: tuple of a selected data
        """

        return f"""
            SELECT {column}
            FROM {table_name}
            WHERE {filter_expression};
            """

    @staticmethod
    def create_row_query(table_name: str, data_list: list) -> str:
        """
        Enter a row of data to a specified table
        :param table_name: preferred table name
        :param data_list: list of values to be entered as a row
        :return: None
        """

        values_string = ", ".join(map(str, data_list))

        return f"""
            INSERT INTO {table_name}
            VALUES ({values_string});
            """

    @staticmethod
    def update_rows_query(table_name: str, column_value_pair: str, filter_expression: str) -> str:
        """
        Update a row of a specified table
        :param table_name: preferred table name
        :param column_value_pair: column and the value required to be updated
        :param filter_expression: filter expression to isolate a specific value
        :return: None
        """

        return f"""
            UPDATE {table_name}
            SET {column_value_pair}
            WHERE {filter_expression};
            """

    @staticmethod
    def delete_rows(table_name: str, filter_expression: str) -> str:
        """
        Delete a specified row from a specified table
        :param table_name: preferred table name
        :param filter_expression: filter expression to isolate a specific row
        :return: None
        """

        return f"""
            DELETE FROM {table_name}
            WHERE {filter_expression};
            """

    @staticmethod
    def read_using_inner_join(table_columns: str, join_table_1: str, join_table_2: str,
                              common_column: str, table_filter_expression: str) -> str:
        """
        Select a unique value from a given pair of tables using
        inner join to match 2 common columns and by filtering out unnecessary data
        :param table_columns: column from which the data is to be retrieved
        :param join_table_1: preferred table 1 name
        :param join_table_2: preferred table 2 name
        :param common_column: column common to both table 1 and table 2
        :param table_filter_expression: filter expression to isolate a specific data
        :return: tuple of a selected data
        """

        return f"""
            SELECT {table_columns}
            FROM {join_table_1} INNER JOIN {join_table_2} 
            ON {join_table_1}.{common_column} = {join_table_2}.{common_column}
            WHERE {table_filter_expression};
            """
