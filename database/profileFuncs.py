from config import BotSettings
from .base import RowResult, Database
import discord
from mysql.connector import errors
from typing import Any, List

__all__ = [
    "profileFuncs"
]

TABLE_NAME = f"`{BotSettings.profile}`"
columns = ["team1", "team2", "team3"]

class profileFuncs:
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
        except errors.ProgrammingError:
            pass
        await self._db.commit()
    
    async def drop(self,) -> None:
        await self._db.execute(f"DROP TABLE gs", commit=True) #**might need to change these if you renamed your tables to something else.**
        await self._db.execute(f"DROP TABLE notifs", commit=True)      
        await self._db.execute(f"DROP TABLE {TABLE_NAME}", commit=True)      
        await self._db.execute(f"DROP TABLE union_raid", commit=True)
        # await self._db.execute(f"DROP TABLE ur_profiles", commit=True)               
        await self._db.commit()
        
    async def pr_open(self, user: discord.Member) -> None:
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
        return await self._db.execute(
            f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,),
            fetch="one")
        
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
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team1 = %s WHERE (userID = %s)", (team, user), commit=True)
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
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team2 = %s WHERE (userID = %s)", (team, user), commit=True)
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
            await self._db.execute(f"UPDATE {TABLE_NAME} SET team3 = %s WHERE (userID = %s)", (team, user), commit=True)
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()      
        else:
            await self._db.execute(f"INSERT INTO {TABLE_NAME} (team3, userID) VALUES (%s, %s)",(team,user), commit=True)
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
        await self._db.execute(f"UPDATE {TABLE_NAME} SET team1=0, team2=0, team3=0 WHERE userID=%s", user.id)
        await self._db.commit()

