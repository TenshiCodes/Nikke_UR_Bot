from readymade import *
from config import Auth
from base import Bot, Context
from datetime import timedelta
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.errors.CommandNotFound):
            return

        if isinstance(error, commands.errors.MissingPermissions) or isinstance(error, commands.errors.NotOwner):
            return await ctx.reply(embed("You cannot use this command"))

        if isinstance(error, commands.errors.MemberNotFound):
            return await ctx.reply(error_embed("the member you provided is incorrect or not found"))

        if isinstance(error, commands.errors.MissingRequiredArgument):
            cmd_parent = ctx.command.parent
            if cmd_parent is not None:
                cmd_name = f"{cmd_parent} {ctx.command.name}"
            else:
                cmd_name = ctx.command.name 
            desc_usage = ctx.command.description
            cmd_usage = ctx.command.usage
            aliases = ctx.command.aliases
            cmd_params = list(ctx.command.params.values())
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
            if ctx.channel.id != 1052240945032220732:   
                em = embed(f"**Correct usage**\n`{usage}`")
                if desc_usage:
                    em.add_field(name="Description", value=desc_usage, inline=False)
                if len(aliases) >= 1:
                    em.add_field(name="Aliases", value=', '.join(aliases))
                em.set_footer(text="' * ' means that argument is required")
                return await ctx.reply(em)
            if isinstance(error, commands.errors.CommandOnCooldown):
                time_left = timedelta(seconds=error.retry_after)
                return await ctx.reply(
                    error_embed(f"You are on cooldown. Try after `{time_formatter(time_left.total_seconds())}`"))
            raise error

def setup(client):
    client.add_cog(Events(client))
