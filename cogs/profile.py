from readymade import *
from base import Bot
import discord
import asyncio
from datetime import datetime
from discord.ext import commands
import ast

class profile(commands.Cog):
    def __init__(self, client: Bot):
        """
        Initializes client, and databases --> profile & ur_profiles.
        pr = profile, pr2 = ur_profiles

        Returns
        -------
        None
        """
        self.client = client
        self.pr = self.client.profile
        self.pr2 = self.client.ur_profiles

    @commands.command(aliases=["team","set","t","setur"], usage=f"<team*: int>", description="This is to set your own teams. For only of the following: team 1, team 2, and team 3.After you do the command: ex. &t 1 . you will then just need to provide character names.**Doing the same command again WILL OVERWRITE.**")
    @commands.guild_only()
    async def setteam(self, ctx: commands.Context, num: int):
        """Checks to make sure its not in a specific channel, opens and checks .txt files.
        using the num arg, checks for character name filters them and puts them in the team lists.
        After 5 characters are set. the team is stored in database to that specific user.
        Args:
            ctx (commands.Context): discord.ext commands for client
            num (int): passing the number arg for respective team in the command
        Returns:
            _type_: async def function
        """
        if ctx.channel.id != 1052240945032220732: #we check to make sure its not in the pvp channel so that command doesnt get initiated
            user = ctx.author
            team = []
            team2 = []
            team3 = []
            name_mapping = {}
            with open("/PATH TO/cogs/name_mappings.txt", "r") as file:
                for line in file:
                    short_name, full_name = line.strip().split(":")
                    name_mapping[short_name] = full_name

            with open("/PATH TO/cogs/character.txt", "r") as file:
                character = [line.strip() for line in file if line.strip()]

            if num == 1:
                embed = discord.Embed(description="Please enter a character name:")
                message = await ctx.send(embed=embed)
                while len(team) < 5:
                    try:
                        response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                        character_name = response.content.capitalize()

                        if character_name in character:
                            if character_name not in team:
                                team.append(character_name)
                                embed.description += f"\n\nCharacter '{character_name}' added to the team."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                            else:
                                embed.description += "\n\nYou have already selected that character. Please choose a different one."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                        else:
                            matching_names = [full_name for short_name, full_name in name_mapping.items() if character_name.lower() in short_name.lower()]
                            if matching_names:
                                matching_names = [name for name in matching_names if name not in team][:5 - len(team)]  # Limit the number of matching names based on remaining slots
                                for full_name in matching_names:
                                    team.append(full_name)
                                    embed.description += f"\n\nCharacter '{full_name}' added to the team."
                                await message.edit(embed=embed)
                                await response.delete()
                            else:
                                embed.description += "\n\nInvalid character name. Please enter a valid character."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                    except asyncio.TimeoutError:
                        embed.description += "\n\nCharacter selection timed out."
                        await message.edit(embed=embed)
                        break

                embed.description += "\n\nTeam selection complete."
                await message.edit(embed=embed)
            
                team = str(team)
                await self.pr2.team_store(user.id, team)
                await asyncio.sleep(5)
                await message.delete()
            elif num == 2:
                embed = discord.Embed(description="Please enter a character name:")
                message = await ctx.send(embed=embed)
                while len(team2) < 5:
                    try:
                        response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                        character_name = response.content.capitalize()

                        if character_name in character:
                            if character_name not in team2:
                                team2.append(character_name)
                                embed.description += f"\n\nCharacter '{character_name}' added to the team."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                            else:
                                embed.description += "\n\nYou have already selected that character. Please choose a different one."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                        else:
                            matching_names = [full_name for short_name, full_name in name_mapping.items() if character_name.lower() in short_name.lower()]
                            if matching_names:
                                matching_names = [name for name in matching_names if name not in team2][:5 - len(team2)]  # Limit the number of matching names based on remaining slots
                                for full_name in matching_names:
                                    team2.append(full_name)
                                    embed.description += f"\n\nCharacter '{full_name}' added to the team."
                                await message.edit(embed=embed)
                                await response.delete()
                            else:
                                embed.description += "\n\nInvalid character name. Please enter a valid character."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                    except asyncio.TimeoutError:
                        embed.description += "\n\nCharacter selection timed out."
                        await message.edit(embed=embed)
                        break

                embed.description += "\n\nTeam selection complete."
                await message.edit(embed=embed)
                team2 = str(team2)
                await self.pr2.team_store2(user.id, team2)
                await asyncio.sleep(5)
                await message.delete()
                    
            elif num == 3:
                embed = discord.Embed(description="Please enter a character name:")
                message = await ctx.send(embed=embed)
                while len(team3) < 5:
                    try:
                        response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                        character_name = response.content.capitalize()

                        if character_name in character:
                            if character_name not in team3:
                                team3.append(character_name)
                                embed.description += f"\n\nCharacter '{character_name}' added to the team."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                            else:
                                embed.description += "\n\nYou have already selected that character. Please choose a different one."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                        else:
                            matching_names = [full_name for short_name, full_name in name_mapping.items() if character_name.lower() in short_name.lower()]
                            if matching_names:
                                matching_names = [name for name in matching_names if name not in team3][:5 - len(team3)]  # Limit the number of matching names based on remaining slots
                                for full_name in matching_names:
                                    team3.append(full_name)
                                    embed.description += f"\n\nCharacter '{full_name}' added to the team."
                                await message.edit(embed=embed)
                                await response.delete()
                            else:
                                embed.description += "\n\nInvalid character name. Please enter a valid character."
                                await message.edit(embed=embed)
                                await response.delete()  # Delete the user's response
                    except asyncio.TimeoutError:
                        embed.description += "\n\nCharacter selection timed out."
                        await message.edit(embed=embed)
                        break

                embed.description += "\n\nTeam selection complete."
                await message.edit(embed=embed)
                team3 = str(team3)
                await self.pr2.team_store3(user.id, team3)
                await asyncio.sleep(5)
                await message.delete()
            else:
                em = discord.Embed(
                    title=f"",
                    description=f"theres only teams 1-3",
                    color=BotSettings.EMBED_COLOR,
                    timestamp=datetime.now()
                    )
                em.set_footer(text=f"{ctx.guild.name}")
                await ctx.reply(em)
            
    @commands.command(aliases=["strike","so"], usage=f"<team*: int> <member*: @member>", description="Coordinators are able to Specify which team has been used for a member by using @")
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def use(self,ctx: commands.Context, team: int, member:discord.Member = None):
        """Checks to make sure its not in a specific channel. Reads which team # from args and sends to database to change
        that respected column. Deletes the responses at the end.
        Args:
            ctx (commands.Context): discord.ext commands for client
            team (int): passing the number arg for respective team in the command
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        Returns:
            _type_: async def function
        """
        if ctx.channel.id != 1052240945032220732:
            user = member or ctx.author
            if team == 1:
                await self.pr2.change(user.id)    
            if team == 2:
                await self.pr2.change2(user.id)
            if team == 3:
                await self.pr2.change3(user.id)
            else:
                pass
                
            message = await ctx.send(content=f"```ml\nUsed {user}'s Team {team}\n```")
             # Delay for 5 seconds
            await asyncio.sleep(4)

            # Delete the message
            await message.delete()
                           
    @commands.command(aliases=["c"], usage=f"<member*: @member>", description="Coordinators are able to clear ALL users team by using @")
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def clear(self,ctx: commands.Context, member:discord.Member = None):
        """Checks to make sure its not in a specific channel. Clears ALL user's teams by sending their userID to database.
        sends embed when action is completed.
        Args:
            ctx (commands.Context): discord.ext commands for client
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        Returns:
            _type_: async def function
        """
        if ctx.channel.id != 1052240945032220732:
            user = member or ctx.author
            await self.pr2.team_clear(user.id)
            em = discord.Embed(
            title=f"",
            description=f"Cleared all teams for {user}",
            color=BotSettings.EMBED_COLOR,
            timestamp=datetime.now()
            )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(em)      
    
    @commands.command(aliases=["tc","tcheck"], usage=f"", description="Coordinators are able to check which teams have not been used")
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def teamcheck(self, ctx: commands.Context):
        """
        Checks to make sure it's not in a specific channel. Checks from the database which user has not used their respective teams and gets returned.
        Sorts the users into an embed list. The embed has page numbers where the user can react to.
        Args:
            ctx (commands.Context): discord.ext commands for the client
        Returns:
            _type_: async def function
        """
        if ctx.channel.id != 1052240945032220732:
            data = await self.pr2.teamcheck1()
            data2 = await self.pr2.teamcheck2()
            data3 = await self.pr2.teamcheck3()

            # Create a list of pages
            pages = []
            current_page = 0

            em = discord.Embed(title="Team Check", color=BotSettings.EMBED_COLOR, timestamp=datetime.now())
            em.set_footer(text=ctx.guild.name)

            # Team 1
            em.add_field(name="__T1__", value=self.get_member_names(data), inline=False)
            pages.append(em)
            em = discord.Embed(title="Team Check", color=BotSettings.EMBED_COLOR, timestamp=datetime.now())
            em.set_footer(text=ctx.guild.name)

            # Team 2
            em.add_field(name="__T2__", value=self.get_member_names(data2), inline=False)
            pages.append(em)
            em = discord.Embed(title="Team Check", color=BotSettings.EMBED_COLOR, timestamp=datetime.now())
            em.set_footer(text=ctx.guild.name)

            # Team 3
            em.add_field(name="__T3__", value=self.get_member_names(data3), inline=False)
            pages.append(em)

            # Call the embed_pages function to handle pagination
            await self.embed_pages(ctx, pages)

    def get_member_names(self, data):
        member_names = []
        for i, user_id in enumerate(data):
            member = self.client.get_user(int(user_id[0]))
            if member is not None:
                member_names.append(f"**{i+1}.**\t {member.name}")
            else:
                member_names.append(f"**{i+1}.**\t User ID {user_id[0]}")
        return "\n".join(member_names)

    async def embed_pages(self, ctx, pages):
        current_page = 0

        embed = pages[current_page]
        embed.set_footer(text=f"Page {current_page + 1}/{len(pages)}")

        message = await ctx.reply(embed=embed)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "➡️" and current_page < len(pages) - 1:
                    current_page += 1
                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1
                else:
                    continue

                embed = pages[current_page]
                embed.set_footer(text=f"Page {current_page + 1}/{len(pages)}")
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            except TimeoutError:
                await message.clear_reactions()
                break
        
    @commands.command(aliases=["p"], usage=f"<member: @member>", description="View your profile or another members profile by using @")
    @commands.guild_only()
    async def profile(self, ctx: commands.Context, member: discord.Member = None):
        """Checks to make sure its not in a specific channel. Checks database for that specific userID and returns TEAMS to be displayed in an embed.
        Checks to see if the columns st1 st2 and st3 are 'y' and filters them in a formatted list to distinguish if teams are in use. This is for the 
        profile section that union raid uses.
        Args:
            ctx (commands.Context): discord.ext commands for client
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        Returns:
            _type_: async def function
        """
        if ctx.channel.id != 1052240945032220732:        
            user = member or ctx.author
            data = await self.pr2.team_data(user.id)
            if data is None:
                em = discord.Embed(
                    title="",
                    description=f"No Team Data for {user}",
                    color=BotSettings.EMBED_COLOR,
                    timestamp=datetime.now()
                )
                em.set_footer(text=f"{ctx.guild.name}")
                await ctx.reply(embed=em)
                return
            
            tuple_string = data[1]
            tstring2 = data[2]
            tstring3 = data[3]

            tuple_list = []
            tuple_list2 = []
            tuple_list3 = []
            
            # Convert the string into a list
            try:
                if tuple_string:
                    tuple_list = ast.literal_eval(tuple_string)
            except ValueError:
                pass
            
            try:
                if tstring2:
                    tuple_list2 = ast.literal_eval(tstring2)
            except ValueError:
                pass
            
            try:
                if tstring3:
                    tuple_list3 = ast.literal_eval(tstring3)
            except ValueError:
                pass
            
            # Format Team 1
            formatted_list1 = "\n".join([f"{index}. {item}" for index, item in enumerate(tuple_list, start=1)]) if tuple_list else None
            # Format Team 2
            formatted_list2 = "\n".join([f"{index}. {item}" for index, item in enumerate(tuple_list2, start=1)]) if tuple_list2 else None
            # Format Team 3
            formatted_list3 = "\n".join([f"{index}. {item}" for index, item in enumerate(tuple_list3, start=1)]) if tuple_list3 else None
        
            res = await self.pr2.checks1(user.id)
            res2 = await self.pr2.checks2(user.id)
            res3= await self.pr2.checks3(user.id)
            if res[0] == 'y':
                formatted_list1 = f"~~```prolog\n{formatted_list1}\n ```~~"
            if res2[0] == 'y':
                formatted_list2 = f"~~```prolog\n{formatted_list2}\n ```~~"
            if res3[0] == 'y':
                formatted_list3 = f"~~```prolog\n{formatted_list3}\n ```~~"
            # Create the embedded message
            embed = discord.Embed(title="__**Union Raid**__", color=discord.Color.random())
            embed.set_author(name=user.name)

            # Check if the user has an avatar and the icon_url is not empty
            if user.avatar and user.avatar.url:
                embed.set_author(name=user.name, icon_url=user.avatar.url)
            embed.add_field(name="Team 1", value=formatted_list1)
            embed.add_field(name="Team 2", value=formatted_list2)
            embed.add_field(name="Team 3", value=formatted_list3)
            
            # Send the embedded message
            await ctx.send(embed=embed)
        
    @commands.command(aliases=["def"],usage=f"", description="Sets everyones teams to default. non-used.")
    @commands.guild_only()
    @commands.has_role("Coordinator")                              
    async def default(self,ctx: commands.Context):
        """Checks to make sure its not in a specific channel. Checks database to switch st1 st2 st3 column to default which is 'n'.
        this distinguishes which teams are in use and sets them back to not in use.
        Args:
            ctx (commands.Context): discord.ext commands for client
        Returns:
            _type_: async def function
        """
        if ctx.channel.id != 1052240945032220732:
            await self.pr2.team_default()
            em = discord.Embed(
                title=f"",
                description=f"All User teams have been set to default",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
                )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(em)
        
    @commands.command(aliases=["pp"], usage=f"<member: @member>", description="View your pvp profile or another members pvp profile")
    @commands.guild_only()
    async def pvp(self, ctx: commands.Context, member: discord.Member = None):
        """Checks database for that specific userID and returns TEAMS to be displayed in an embed.
        This is for pvp section only.
        Args:
            ctx (commands.Context): discord.ext commands for client
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        Returns:
            _type_: async def function
        """
        user = member or ctx.author
        data = await self.pr.team_data(user.id)
        if data is None:
            em = discord.Embed(
                title="",
                description=f"No Team Data for {user}",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
            )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(embed=em)
            return
        
        tuple_string = data[1]
        tstring2 = data[2]
        tstring3 = data[3]

        tuple_list = []
        tuple_list2 = []
        tuple_list3 = []
        
        # Convert the string into a list
        try:
            if tuple_string:
                tuple_list = ast.literal_eval(tuple_string)
        except ValueError:
            pass
        
        try:
            if tstring2:
                tuple_list2 = ast.literal_eval(tstring2)
        except ValueError:
            pass
        
        try:
            if tstring3:
                tuple_list3 = ast.literal_eval(tstring3)
        except ValueError:
            pass
        
        # Format Team 1
        formatted_list1 = "\n".join([f"{index}. {item}" for index, item in enumerate(tuple_list, start=1)]) if tuple_list else None
        # Format Team 2
        formatted_list2 = "\n".join([f"{index}. {item}" for index, item in enumerate(tuple_list2, start=1)]) if tuple_list2 else None
        # Format Team 3
        formatted_list3 = "\n".join([f"{index}. {item}" for index, item in enumerate(tuple_list3, start=1)]) if tuple_list3 else None

        embed = discord.Embed(title=f"__**PVP Special Arena**__", color=discord.Color.random())
        embed.set_author(name=user.name)

        # Check if the user has an avatar and the icon_url is not empty
        if user.avatar and user.avatar.url:
            embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.add_field(name="Team 1", value=formatted_list1)
        embed.add_field(name="Team 2", value=formatted_list2)
        embed.add_field(name="Team 3", value=formatted_list3)
        
        # Send the embedded message
        await ctx.send(embed=embed)

    @commands.command(aliases=["pteam","pt","setpvp"], usage=f"<team*: int>", description="This is to set your own teams. For only of the following: team 1, team 2, and team 3")
    @commands.guild_only()
    async def pvpteam(self, ctx: commands.Context, num: int):
        """Opens and checks .txt files. Using the num arg, checks for character name filters them and puts them in the team lists.
        After 5 characters are set. the team is stored in database to that specific user.
        Args:
            ctx (commands.Context): discord.ext commands for client
            num (int): passing the number arg for respective team in the command
        Returns:
            _type_: async def function
        """
        user = ctx.author
        team = []
        team2 = []
        team3 = []
        
        name_mapping = {}
        with open("/PATH TO/cogs/name_mappings.txt", "r") as file:
            for line in file:
                short_name, full_name = line.strip().split(":")
                name_mapping[short_name] = full_name

        with open("/PATH TO/cogs/character.txt", "r") as file:
            character = [line.strip() for line in file if line.strip()]          
        
        if num == 1:
            embed = discord.Embed(description="Please enter a character name:")
            message = await ctx.send(embed=embed)
            while len(team) < 5:
                try:
                    response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                    character_name = response.content.capitalize()

                    if character_name in character:
                        if character_name not in team:
                            team.append(character_name)
                            embed.description += f"\n\nCharacter '{character_name}' added to the team."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                        else:
                            embed.description += "\n\nYou have already selected that character. Please choose a different one."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                    else:
                        matching_names = [full_name for short_name, full_name in name_mapping.items() if character_name.lower() in short_name.lower()]
                        if matching_names:
                            matching_names = [name for name in matching_names if name not in team][:5 - len(team)]  # Limit the number of matching names based on remaining slots
                            for full_name in matching_names:
                                team.append(full_name)
                                embed.description += f"\n\nCharacter '{full_name}' added to the team."
                            await message.edit(embed=embed)
                            await response.delete()
                        else:
                            embed.description += "\n\nInvalid character name. Please enter a valid character."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                except asyncio.TimeoutError:
                    embed.description += "\n\nCharacter selection timed out."
                    await message.edit(embed=embed)
                    break

            embed.description += "\n\nTeam selection complete."
            await message.edit(embed=embed)
           
            team = str(team)
            await self.pr.team_store(user.id, team)
            await asyncio.sleep(5)
            await message.delete()
        elif num == 2:
            embed = discord.Embed(description="Please enter a character name:")
            message = await ctx.send(embed=embed)
            while len(team2) < 5:
                try:
                    response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                    character_name = response.content.capitalize()

                    if character_name in character:
                        if character_name not in team2:
                            team2.append(character_name)
                            embed.description += f"\n\nCharacter '{character_name}' added to the team."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                        else:
                            embed.description += "\n\nYou have already selected that character. Please choose a different one."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                    else:
                        matching_names = [full_name for short_name, full_name in name_mapping.items() if character_name.lower() in short_name.lower()]
                        if matching_names:
                            matching_names = [name for name in matching_names if name not in team2][:5 - len(team2)]  # Limit the number of matching names based on remaining slots
                            for full_name in matching_names:
                                team2.append(full_name)
                                embed.description += f"\n\nCharacter '{full_name}' added to the team."
                            await message.edit(embed=embed)
                            await response.delete()
                        else:
                            embed.description += "\n\nInvalid character name. Please enter a valid character."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                except asyncio.TimeoutError:
                    embed.description += "\n\nCharacter selection timed out."
                    await message.edit(embed=embed)
                    break

            embed.description += "\n\nTeam selection complete."
            await message.edit(embed=embed)
            team2 = str(team2)
            await self.pr.team_store2(user.id, team2)
            await asyncio.sleep(5)
            await message.delete()
                
        elif num == 3:
            embed = discord.Embed(description="Please enter a character name:")
            message = await ctx.send(embed=embed)
            while len(team3) < 5:
                try:
                    response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30)
                    character_name = response.content.capitalize()

                    if character_name in character:
                        if character_name not in team3:
                            team3.append(character_name)
                            embed.description += f"\n\nCharacter '{character_name}' added to the team."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                        else:
                            embed.description += "\n\nYou have already selected that character. Please choose a different one."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                    else:
                        matching_names = [full_name for short_name, full_name in name_mapping.items() if character_name.lower() in short_name.lower()]
                        if matching_names:
                            matching_names = [name for name in matching_names if name not in team3][:5 - len(team3)]  # Limit the number of matching names based on remaining slots
                            for full_name in matching_names:
                                team3.append(full_name)
                                embed.description += f"\n\nCharacter '{full_name}' added to the team."
                            await message.edit(embed=embed)
                            await response.delete()
                        else:
                            embed.description += "\n\nInvalid character name. Please enter a valid character."
                            await message.edit(embed=embed)
                            await response.delete()  # Delete the user's response
                except asyncio.TimeoutError:
                    embed.description += "\n\nCharacter selection timed out."
                    await message.edit(embed=embed)
                    break

            embed.description += "\n\nTeam selection complete."
            await message.edit(embed=embed)
            team3 = str(team3)
            await self.pr.team_store3(user.id, team3)
            await asyncio.sleep(5)
            await message.delete()
        else:
            em = discord.Embed(
                title=f"",
                description=f"theres only teams 1-3",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
                )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(em)

def setup(client):
    client.add_cog(profile(client))
    

