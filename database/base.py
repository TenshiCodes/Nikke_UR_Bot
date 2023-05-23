from config import Auth
import mysql.connector as mysql
from mysql.connector import MySQLConnection, errors
from typing import Tuple, Any, Optional, Union, List

__all__ = [
    "Database",
    "Result",
    "RowResult"
]

Result = Optional[Union[Tuple[Any, ...], List[Any]]]
RowResult = Optional[Tuple[Any, ...]]

class Database:
    __conn: Optional[MySQLConnection] = None

    async def connect(self):
        try:
            self.__conn = mysql.connect(
                host=Auth.DB_HOST, port=Auth.DB_PORT,
                database=Auth.DB_NAME, user=Auth.DB_USER, passwd=Auth.DB_PASSWD,
            )
        except errors.Error:
            self.__conn = None
        return self

    @property
    def is_connected(self) -> bool:
        """
        checks whether the bot is connected to database or not

        :return: True or False
        """
        return self.__conn is not None

    @staticmethod
    async def _fetch(cursor, mode) -> Result:
        if mode == "one":
            return cursor.fetchone()
        if mode == "many":
            return cursor.fetchmany()
        if mode == "all":
            return cursor.fetchall()
        return None

    async def execute(self, query: str, values: Tuple[Any, ...] = (), *,
                      fetch: str = None, commit: bool = False) -> Result:
        """
        Executes the sql query

        :param query: sql query
        :param values: values to be added to the query
        :param fetch: fetches one, many or all if passed
        :param commit: commits it to database
        :return: Result
        """
        cursor = self.__conn.cursor()
        cursor.execute(query, values)
        data = await self._fetch(cursor, fetch)
        if commit:
            self.__conn.commit()
        cursor.close()
        return data

    async def commit(self) -> None:
        """
        Commits the database
        """
        self.__conn.commit()
