from config import BotSettings
from .base import Database, RowResult
import mysql.connector as mysql

__all__ = [
    "google_sheetFuncs"
]

TABLE_NAME = f"`{BotSettings.gs}`"
columns = ["current","timestamp"]

class google_sheetFuncs:
    def __init__(self, database: Database):
        self._db = database
    
    async def current(self) -> None:
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"DELETE FROM {TABLE_NAME} WHERE `current` = 'n'")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET current='y' WHERE url = (SELECT url FROM (SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT 1) AS subquery)")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET current='n' WHERE url IN (SELECT url FROM (SELECT url FROM {TABLE_NAME} WHERE timestamp != (SELECT MAX(timestamp) FROM {TABLE_NAME})) AS subquery)")
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
        return await self._db.execute(f"SELECT url FROM {TABLE_NAME} WHERE timestamp = (SELECT MAX(timestamp) FROM {TABLE_NAME}) LIMIT 1",fetch="one")
   
    async def upload(self, url:str) -> None:
        data = await self._db.execute(f"SELECT * FROM {TABLE_NAME} WHERE url = %s", (url,), fetch="one")
        await self._db.execute(f"DELETE FROM {TABLE_NAME} WHERE (`url` = %s)", (url,))
        await self._db.execute(f"INSERT INTO {TABLE_NAME}(url) VALUES(%s)", (url,))
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET current='y' WHERE url = (SELECT url FROM (SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT 1) AS subquery)")
        await self._db.execute(f"UPDATE {TABLE_NAME} SET current='n' WHERE url IN (SELECT url FROM (SELECT url FROM {TABLE_NAME} WHERE timestamp != (SELECT MAX(timestamp) FROM {TABLE_NAME})) AS subquery)")
        await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
        await self._db.commit()
        if data is None:
            await self._db.execute(f"INSERT INTO {TABLE_NAME}(url) VALUES(%s)", (url,))
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET current='y' WHERE url = (SELECT url FROM (SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT 1) AS subquery)")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET current='n' WHERE url IN (SELECT url FROM (SELECT url FROM {TABLE_NAME} WHERE timestamp != (SELECT MAX(timestamp) FROM {TABLE_NAME})) AS subquery)")
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()
        
    async def use(self) -> RowResult:
        data = await self._db.execute(f"SELECT url FROM {TABLE_NAME} WHERE timestamp = (SELECT MAX(timestamp) FROM {TABLE_NAME}) LIMIT 1",fetch="one")
        if data is None:
            await self._db.execute(f"UPDATE {TABLE_NAME} SET current='y' WHERE url = (SELECT url FROM (SELECT * FROM {TABLE_NAME} ORDER BY timestamp DESC LIMIT 1) AS subquery)")
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 0")
            await self._db.execute(f"UPDATE {TABLE_NAME} SET current='n' WHERE url IN (SELECT url FROM (SELECT url FROM {TABLE_NAME} WHERE timestamp != (SELECT MAX(timestamp) FROM {TABLE_NAME})) AS subquery)")
            await self._db.execute(f"SET SQL_SAFE_UPDATES = 1")
            await self._db.commit()
        return await self._db.execute(f"SELECT url FROM {TABLE_NAME} WHERE timestamp = (SELECT MAX(timestamp) FROM {TABLE_NAME}) LIMIT 1",fetch="one")
    
    async def view(self) -> None:
        return await self._db.execute(f"SELECT * FROM {TABLE_NAME}", fetch="all")
    
    async def create_table(self) -> None:
        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}(url VARCHAR(100) PRIMARY KEY)", commit=True)
        try:
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `current` CHAR(1) DEFAULT 'n' ")
            await self._db.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()")
            await self._db.commit()
        except mysql.errors.ProgrammingError:
            pass
        
   