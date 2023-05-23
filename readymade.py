from base import Bot
from config import Auth, BotSettings
import datetime
import discord
from typing import TypeVar, Union, Optional

__all__ = [
    "BotSettings",
    "Colors",
    "embed",
    "error_embed",
    "time_formatter",
    "get_command_usage"
]

class Colors:
    _ColorString = TypeVar("_ColorString", str, str)

    @staticmethod
    def red(content: str) -> _ColorString:
        return "\033[31m" + content + "\033[00m"

    @staticmethod
    def blue(content: str) -> _ColorString:
        return "\033[34m" + content + "\033[00m"

    @staticmethod
    def purple(content: str) -> _ColorString:
        return "\033[35m" + content + "\033[00m"

    @staticmethod
    def green(content: str) -> _ColorString:
        return "\033[92m" + content + "\033[00m"

def embed(context: str, color=BotSettings.EMBED_COLOR, timestamp: bool = BotSettings.EMBED_TIMESTAMP, guild = None) -> discord.Embed:
    if timestamp:
        em = discord.Embed(
            description=context,
            color=discord.Color(color),
            timestamp=datetime.datetime.utcnow()
        )
        return em
    else:
        em = discord.Embed(
            description=context,
            color=discord.Color(color)
        )   
    if guild:
        for field in em.fields:
            field.value = field.value.replace(':','')
            custom_emoji = guild.get_emoji(int(field.value))
            if custom_emoji:
                field.value = str(custom_emoji)
    return em

def error_embed(context: str, timestamp: bool = BotSettings.EMBED_TIMESTAMP):
    return embed(context, BotSettings.EMBED_ERROR_COLOR, timestamp)

def time_formatter(seconds_: Union[int, float], *options):
    time_dict = {"s": 1, "seconds": 1, "m": 60, "minute": 60, "h": 3600,
                 "d": 3600 * 24, "M": 3600 * 24 * 30, "Y": 3600 * 24 * 30 * 12}

    year = seconds_ // (time_dict["Y"])
    secs_ = seconds_ % (time_dict['Y'])
    months = secs_ // (time_dict['M'])
    secs_ %= time_dict['M']
    days = secs_ // (time_dict['d'])
    secs_ %= time_dict['d']
    hrs = secs_ // (time_dict['h'])
    secs_ %= time_dict['h']
    mins = secs_ // (time_dict['m'])
    secs_ %= time_dict['m']
    secs = secs_
    if len(options) != 0:
        cache = []
        for option in options:
            conv_time = {"Y": year, "year": year, "M": months, "month": months, "d": days, "day": days,
                         "h": hrs, "hour": hrs, "m": mins, "minute": mins, "s": secs, "seconds": secs}
            if option in conv_time.keys():
                cur_time = conv_time.get(option)
                cache.append(cur_time)
        return cache
    else:
        if seconds_ >= 2592000:
            if days >= 1:
                return f"{months:.0f} Month(s) and {days:.0f} day(s)"
            else:
                return f"{months:.0f} Month(s)"
        elif seconds_ >= 86400:
            return f"{days:.0f} Day(s), {hrs:.0f} Hour(s) and {mins:.0f} min(s)"
        elif seconds_ >= 3600:
            return f"{hrs:.0f} Hour(s), {mins:.0f} Min(s) and {secs:.0f} sec(s)"
        elif seconds_ >= 60:
            return f"{mins:.0f} Min(s) and {secs:.0f} sec(s)"
        elif seconds_ < 60:
            return f"{secs:.0f} sec(s)"

async def get_command_usage(client: Bot, command_name: str) -> Optional[discord.Embed]:
    for command in client.commands:
        cmd_parent = command.parent
        if cmd_parent is not None:
            cmd_name = f"{cmd_parent} {command.name}"
        else:
            cmd_name = command.name
        if cmd_name == command_name:
            cmd_usage = command.usage
            desc_usage = command.description  # Added line
            aliases = command.aliases
            cmd_params = list(command.params.values())
            usage = f"{Auth.COMMAND_PREFIX}{cmd_name} "
            if cmd_usage is None:
                cmd_params = cmd_params[2:] if cmd_params[0].name == "self" else cmd_params[1:]
                params = []
                for param in cmd_params:
                    if param.empty:
                        log = f"<{param.name}*>"
                    else:
                        log = f"<{param.name}>"
                    params.append(log)
                usage += ' '.join(params)
            else:
                usage += cmd_usage
            em = embed(f"**Correct usage**\n`{usage}`")
            if desc_usage:
                em.add_field(name="Description", value=desc_usage, inline=False)
            if len(aliases) >= 1:
                em.add_field(name="Aliases", value=', '.join(aliases), inline=False)
            em.set_footer(text="' * ' means that argument is required")
            return em
    return None
