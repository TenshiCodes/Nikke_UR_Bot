from config import BotSettings
from .base import Database, RowResult
import discord
import mysql.connector as mysql
from typing import List

__all__ = [
    "notificationsFuncs"
]

TABLE_NAME = f"`{BotSettings.notifs}`"
columns = ["boss_name","channelID","userID","idx"]

class notificationsFuncs:
    def __init__(self, database: Database):
        self._db = database
        
    async def create_table(self) -> None:
        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (`boss_name` VARCHAR(45) NOT NULL,`userID` VARCHAR(45) NOT NULL,`channelID` VARCHAR(45) NOT NULL, idx BIGINT AUTO_INCREMENT PRIMARY KEY);", commit=True)
        await self._db.commit()
        
    async def store(self, boss_name:str, user:discord.Member,  channelID:discord.TextChannel) -> None:
        await self._db.execute(f"INSERT INTO {TABLE_NAME} (`boss_name`, `userID`, `channelID`) VALUES (%s, %s, %s)", (boss_name, user, channelID), commit=True)
        await self._db.commit()
        
    async def search(self, user: discord.Member) -> List[RowResult]:
        rows = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE `userID` = %s", (user.id,), fetch="all")
        await self._db.commit()
        return rows
    
    async def clear(self, n1:str, n2:str) -> None:
        await self._db.execute(f"DELETE FROM {TABLE_NAME} WHERE `userID` = %s AND `boss_name` = %s AND `idx` > 0 LIMIT 1", (n1,n2,), commit=True)
        await self._db.commit()
        
    async def bossclear(self,n1:str) -> None:
        await self._db.execute(f"DELETE FROM {TABLE_NAME} WHERE `boss_name` = %s AND `idx` > 0",(n1,), commit=True)
        await self._db.commit()
        
    async def get_user(self,n1:str) -> List[RowResult]:
        rows = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE `boss_name` = %s AND `idx` > 0",(n1,), fetch="all")
        await self._db.commit()
        return rows






