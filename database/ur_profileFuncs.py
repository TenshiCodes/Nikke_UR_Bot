from config import BotSettings
from .base import RowResult, Database
import mysql.connector as mysql
import discord
from mysql.connector import errors
from typing import Any, List

__all__ = [
    "ur_profileFuncs"
]

TABLE_NAME = f"`{BotSettings.ur_profiles}`"
columns = ["team1", "team2", "team3", "st1","st2","st3"]

class ur_profileFuncs:
    def __init__(self, database: Database):
        self._db = database

    async def create_table(self) -> None:
        """
        Create a new table in the database if it does not exist.

        Returns
        -------
        None
        """
        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}(userID VARCHAR(60) PRIMARY KEY)", commit=True)
        try:
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `team1` VARCHAR(100)")
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `team2` VARCHAR(100)")
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `team3` VARCHAR(100)")
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `st1` CHAR(1) DEFAULT 'n'")
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `st2` CHAR(1) DEFAULT 'n'")
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `st3` CHAR(1) DEFAULT 'n'")
        except errors.ProgrammingError:
            pass
        await self._db.commit()
        
    async def teamcheck1(self,) -> RowResult:
        data = await self._db.execute(f"SELECT userID FROM {TABLE_NAME} WHERE team1 IS NOT NULL AND st1 = 'n'", fetch="all")
        await self._db.commit()
        return data
    
    async def teamcheck2(self,) -> RowResult:
        data = await self._db.execute(f"SELECT userID FROM {TABLE_NAME} WHERE team2 IS NOT NULL AND st2 = 'n'", fetch="all")
        await self._db.commit()
        return data
    
    async def teamcheck3(self,) -> RowResult:
        data = await self._db.execute(f"SELECT userID FROM {TABLE_NAME} WHERE team3 IS NOT NULL AND st3 = 'n'", fetch="all")
        await self._db.commit()
        return data
    
    async def ur_open(self, user: discord.Member) -> None:
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user.id,), fetch="one")
        if data is None:
            await self._db.execute(f"INSERT INTO {TABLE_NAME}(userID) VALUES(%s)", (user.id,))
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team1 = %s,team2 = %s,team3 = %s WHERE (userID = %s)", ("","","", user.id) )            
            await self._db.commit()
            
    async def team_data(self, user: discord.Member) -> RowResult:
        """
        Retrieve the team data for the given user from the database and display it.

        Parameters
        ----------
        user : discord.Member
            The user whose team data should be retrieved.

        Returns
        -------
        None
        """
        return await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
    
    async def checks1(self, user:discord.Member) -> RowResult:
        data = await self._db.execute(f"SELECT `st1` FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
        await self._db.commit()
        return data
    
    async def checks2(self, user:discord.Member) -> RowResult:
        data = await self._db.execute(f"SELECT `st2` FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
        await self._db.commit()
        return data
    
    async def checks3(self, user:discord.Member) -> RowResult:
        data = await self._db.execute(f"SELECT `st3` FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
        await self._db.commit()
        return data
    
    async def team_store(self, user: discord.Member, team: List[str]) -> None:
        """
        Store the given list of teams for the given user in the database.

        Parameters
        ----------
        user : discord.Member
            The user whose teams should be stored.
        teams : List[str]
            The list of teams to store.

        Returns
        -------
        RowResult
            The result of the database query.
        """    
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
        if data is not None:
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team1 = %s, st1 = 'n' WHERE (userID = %s)", (team, user), commit=True)
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()
        else:
            await self._db.execute(f"INSERT INTO {TABLE_NAME} (team1, userID) VALUES (%s, %s)",(team,user), commit=True)
            await self._db.commit() 
               
    async def team_store2(self, user: discord.Member, team: List[str]) -> None:
        """
        Store the given list of teams for the given user in the database.

        Parameters
        ----------
        user : discord.Member
            The user whose teams should be stored.
        teams : List[str]
            The list of teams to store.

        Returns
        -------
        RowResult
            The result of the database query.
        """
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
        if data is not None:
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team2 = %s, st2 = 'n' WHERE (userID = %s)", (team, user), commit=True)
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()
        else:
            await self._db.execute(f"INSERT INTO {TABLE_NAME} (team2, userID) VALUES (%s, %s)",(team,user), commit=True)
            await self._db.commit()
            
    async def team_store3(self, user: discord.Member, team: List[str]) -> None:
        """
        Store the given list of teams for the given user in the database.

        Parameters
        ----------
        user : discord.Member
            The user whose teams should be stored.
        teams : List[str]
            The list of teams to store.

        Returns
        -------
        RowResult
            The result of the database query.
        """
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="one")
        if data is not None:
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team3 = %s, st3 = 'n' WHERE (userID = %s)", (team, user), commit=True)
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()
        else:
            await self._db.execute(f"INSERT INTO {TABLE_NAME} (team3, userID) VALUES (%s, %s)",(team,user), commit=True)
            await self._db.commit()
            
    async def change(self, user:discord.Member) -> None:
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET st1 = 'y' WHERE userID = %s", (user,), commit=True)
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
        
    async def change2(self, user:discord.Member) -> None:
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET st2 = 'y' WHERE userID = %s", (user,), commit=True)
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
        
    async def change3(self, user:discord.Member) -> None:
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET st3 = 'y' WHERE userID = %s", (user,), commit=True)
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
        
    async def team_default(self) -> None:
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET st1 = 'n', st2 = 'n', st3 = 'n'", commit=True)
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()
    async def team_clear(self, user: discord.Member) -> None:
        """
        Clear the team data for the given user from the database.

        Parameters
        ----------
        user : discord.Member
            The user whose team data should be cleared.

        Returns
        -------
        None
        """
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET `team1` = NULL, `team2` = NULL, `team3` = NULL WHERE (`userID` = %s)", (user,), commit=True)
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
