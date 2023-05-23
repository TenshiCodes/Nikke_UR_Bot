#!/usr/bin/python

from config import Auth
from base import Bot
from readymade import Colors
import sys
import os
import discord
import subprocess

intents = discord.Intents.all()
client = Bot(command_prefix=Auth.COMMAND_PREFIX, intents=intents)

# removes default help command
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"{Auth.COMMAND_PREFIX}help")
    )
    print(Colors.purple("Loading cogs:"))
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                client.load_extension(f"cogs.{file[:-3]}")
                print(Colors.blue(f"\t- {file[:-3]} ✅"))
            except Exception as e:
                if isinstance(e, discord.errors.ExtensionError) or isinstance(
                        e, discord.errors.NoEntryPointError
                ):
                    print(Colors.blue(f"\t- {file[:-3]} ❌"))
    print()
    await client.db.connect()
    if not client.db.is_connected:
        raise RuntimeError("Database access denied")
    else:
        print(Colors.green("Connected to Database!"))
    await client.profile.create_table()
    await client.union_raid.create_table()
    await client.gs.create_table()
    await client.notifs.create_table()
    await client.ur_profiles.create_table()
    print(Colors.green("Created/modified tables successfully"))
    print(Colors.green(f"{client.user.name} is online!"))
    
def restart_bot():
    # Get the command used to start the current Python interpreter
    python_cmd = [sys.executable]

    # Get the arguments used to start the current Python interpreter
    python_cmd.extend(sys.argv)

    # Start a new Python interpreter in a separate process
    subprocess.Popen(python_cmd)
    
@client.command(name='r_bot')
async def restart(ctx):
    data = str(ctx.author.id)
    if data == '163022587063042051' or '619893018115178517':
        await ctx.author.send("Restarting bot...")
    
        # Get the command used to start the current Python interpreter
        python_cmd = [sys.executable]

        # Get the arguments used to start the current Python interpreter
        python_cmd.extend(sys.argv)
        try:
            # Start a new process of the current script
            pid = os.spawnv(os.P_NOWAIT, sys.executable, python_cmd)
            if pid > 0:
                print(".......Bot is Restarting with PID: ", pid)
                # Terminate the current process
                sys.exit(0)
            else:
                print("Failed to spawn the process.")
                
        except OSError as e:
            print("Failed to spawn the process:", str(e))

    else:
        await ctx.author.send("You are not authorized to use this command.")
        
if __name__ == "__main__":
    # Make sure to add required secrets in '.env' file
    client.run(os.getenv('TOKEN'))
