from config import BotSettings
from .base import Database, RowResult
import discord
import mysql.connector as mysql
from typing import Union, Optional
from mysql.connector import errors
from typing import Any, List

__all__ = [
    "union_raidFuncs"
]

TABLE_NAME = f"`{BotSettings.union_raid}`"
columns = ["boss_name","day","userID"]

class unionraidFuncs:
    def __init__(self, database: Database):
        self._db = database
        
    async def hitters(self, user:discord.Member, boss_name:str, day:str) -> None:
        hitters = await self._db.execute(f"SELECT userID FROM {TABLE_NAME} WHERE boss_name = %s AND day = %s",(boss_name,day), fetch="all")
        return hitters
    
    async def ur_open(self, user: discord.Member) -> None:
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user.id,), fetch="all")
        if data is None:
            await self._db.execute(f"INSERT INTO {TABLE_NAME}(userID) VALUES(%s)", (user.id,))
            await self._db.execute(f"UPDATE {TABLE_NAME} SET `boss_name` = %s WHERE userID = %s", ("", user.id))
            await self._db.commit()
            
    async def get_ur(self, user: discord.Member) -> RowResult:
        return await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user.id,), fetch="all")
            
    async def create_table(self) -> None:
        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}(idx BIGINT AUTO_INCREMENT PRIMARY KEY)", commit=True)
        for col in columns:
            try:
                await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `{col}` VARCHAR(60) DEFAULT '' ")
            except mysql.errors.ProgrammingError:
                pass
        await self._db.commit()
   
    async def add_boss(self, boss_name: str, day: str, user: discord.Member, mode: str = "boss_name", mode2:str = "day") -> RowResult:
        """Add a boss_name into the columns"""
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="all")
        if data is None:
            print("data is none")
        if data is not None:
            await self._db.execute(f"INSERT INTO {TABLE_NAME} (`{mode}`, `{mode2}`, `userID`) VALUES (%s, %s, %s)", (boss_name, day, user), commit=True)
            await self._db.commit()
        user = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE boss_name = %s", (boss_name,), fetch="all")
        return user
    
    async def get_hit(self, boss_name:str, day:str) -> List[Any]:
        return await self._db.execute(f"SELECT userID FROM {TABLE_NAME} Where boss_name = %s AND day = %s",(boss_name,day), fetch="all")
        
    async def add_hitter(self, user: discord.Member) -> None:
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user.id,), fetch="all")
        if data is None:
            await self._db.execute(f"INSERT INTO {TABLE_NAME}(userID) VALUES(%s)", (user.id,), commit=True)
            
    async def delete_hitter(self, user: discord.Member, boss_name: str, day: int) -> None:        
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE userID = %s", (user,), fetch="all")        
        if data is not None:
            await self._db.execute(f"DELETE FROM {TABLE_NAME} WHERE `boss_name` = %s AND `userID` = %s AND `day` = %s AND `idx` > 0", (boss_name, user, day,), commit=True)
        else:
            pass #print("")
        
    async def deleteall(self) -> None:
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"DELETE FROM {TABLE_NAME}")
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
