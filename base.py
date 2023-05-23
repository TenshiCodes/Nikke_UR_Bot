from database import Database, profileFuncs, unionraidFuncs, ur_profileFuncs, google_sheetFuncs, notificationsFuncs
import discord
from typing import Any
from discord.ext import commands

__all__ = [
    "Context",
    "Bot",
]

class Context(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def reply(self, content: str | discord.Embed = None, **kwargs: Any) -> discord.Message:
        if "mention_author" not in kwargs.keys():
            kwargs.setdefault("mention_author", False)
        if isinstance(content, discord.Embed):
            kwargs.setdefault("embed", content)
            content = None
        return await self.message.reply(content, **kwargs)

class Bot(commands.Bot):
    db = Database()
    union_raid = unionraidFuncs(db)
    profile = profileFuncs(db)
    ur_profiles = ur_profileFuncs(db)
    gs = google_sheetFuncs(db)
    notifs = notificationsFuncs(db)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_context(self, message: discord.Message, *, cls=Context):
        return await super().get_context(message, cls=cls)
