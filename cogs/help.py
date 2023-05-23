from readymade import *
from base import Bot, Context
from config import Auth
import discord
from discord.ext import commands
from typing import Dict, List

class Help(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx: Context, command_name: str = None):
        if ctx.channel.id != 1052240945032220732:
            if command_name is not None:
                em = await get_command_usage(self.client, command_name)
                if em is not None:
                    return await ctx.reply(embed=em)
                else:
                    return await ctx.reply(error_embed(f"There's no command named **{command_name}**"))

            bot_commands: Dict[str, List[str]] = {}
            for command in self.client.commands:
                cog = command.cog_name
                if cog not in bot_commands.keys():
                    bot_commands[cog] = []
                if command.parent is not None:
                    cmd_name = f"{command.parent} {command.name}"
                else:
                    cmd_name = command.name
                bot_commands[cog].append(cmd_name)

            em = discord.Embed(title="__Help Menu__", color=BotSettings.EMBED_COLOR)
            em.set_footer(text=f"For more info, use {Auth.COMMAND_PREFIX}help <command_name>")
            categories = {
                "__Members__": {
                    "UR Commands": ["start", "hitter", "boss", "notify"],
                    "Profile Commands": ["profile", "setteam"]
                },
                "__Carnage Coordinators__": {
                    "UR Commands": ["select", "unleashed", "delete", "add", "reset"],
                    "Profile Commands": ["teamcheck", "use", "default", "clear"]
                },
                "__PVP Menu__": {
                    "Profile Commands": ["pvp", "pvpteam"]
                },
            }
            for category, subcategories in categories.items():
                if category in bot_commands:
                    subcommands = bot_commands[category]
                    for subcategory, commands in subcategories.items():
                        if subcategory in subcommands:
                            subcommands[subcategory].extend(commands)
            for category, subcategories in categories.items():
                if any(subcommands for subcommands in subcategories.values()):
                    category_list = []
                    for subcategory, commands in subcategories.items():
                        if commands:
                            command_list = "\n".join([f"- {cmd}" for cmd in commands])
                            category_list.append(f"{subcategory}:\n{command_list}")
                    if category_list:
                        em.add_field(name=category, value="\n\n".join(category_list), inline=False)
            em.description = f"Bot prefix is {Auth.COMMAND_PREFIX}\n**Make sure to share Google Sheet with**\n" \
                            "tenshibot@impactful-facet-385622.iam.gserviceaccount.com\n*__Run command &check to see configs__*\n"
            await ctx.reply(embed=em)

def setup(client):
    client.add_cog(Help(client))
