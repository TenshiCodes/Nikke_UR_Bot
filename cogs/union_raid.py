from readymade import *
from base import Bot
import discord
import asyncio
from datetime import datetime
from discord.ext import commands
import pandas as pd
import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from views.menu import MyMenu
from mysql.connector import IntegrityError

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/PATH/TO/YOUR/.JSON/FOR GOOGLE API/..', scopes)
gc = gspread.authorize(credentials)
guath = GoogleAuth
drive = GoogleDrive(guath)

class union_raid(commands.Cog):
    def __init__(self, client: Bot):
        """
        Initializes clients, empty lists(boss_list,boss_associations,sheetName), and databases --> profile, union_raid, gs, notifs.
        pr = profile, pr3 = union_raid, gs = gsheet, notifs = notifications

        Returns
        -------
        None
        """
        self.client = client
        self.pr = self.client.profile
        # self.pr2 = self.client.ur_profiles
        self.pr3 = self.client.union_raid
        self.gsheet = self.client.gs
        self.notifs = self.client.notifs
        self.boss_list = []
        self.boss_associations = []
        self.sheetName = ["invalid_sheet"]
        
    @commands.command(aliases=["a"], usage=f"<Account*: Member Name> <Damage*: int>", description="Coordinator can send data to the CURRENT GOOGLE SHEET. all you need is the Name and Damage. Example: Tenshi 501928929")
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def add(self, ctx: commands.Context, account: str, damage: int):
        """Checks to make sure its not in a specific channel. This appends data to the Google Sheets using a view. Args need to be provided.
        Args:
            ctx (commands.Context): discord.ext commands for client
            account (str): passing account arg. This should be the name/account that is in Google Sheets
            damage (str): passing damage # arg. This should be the damage# that will be in Google Sheets
        """
        if ctx.channel.id != 1052240945032220732: #we check to make sure its not in the pvp channel so that command doesnt get initiated
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet("Config")#"GOOGLE SHEET NAME" #Config TAB
                if sheet is not None:
                    sheetName = self.sheetName
                    view = MyMenu(self, account, damage, sheetName)
                    em = discord.Embed(title="Adding to the Sheet:",
                                    description=f"Pick the Union Raid Day")  
                    await ctx.reply(content=f"",
                                    embed=em, view=view)
                else:
                    pass
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
    
    @commands.command(aliases=["se","upl","upload"], usage=f"",description="Select a sheet by Name that the bot is in\ntenshibot@impactful-facet-385622.iam.gserviceaccount.com\n")
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def select(self, ctx):
        """Selects the google sheet for Configs. puts the name in self.sheeetName and uploads the name to database.
        Goes through Config worksheet and looks at the bosses. puts them in the boss_list and responds with an embed.
        Args:
            ctx (_type_): Client
        """
        if ctx.channel.id != 1052240945032220732:
            em = embed(f"What is the sheet name?")
            await ctx.reply(em)
            try:
                response = await ctx.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel,
                    timeout=60,
                )
                index = 0
                self.sheetName[index] = response.content
                dsheet = str(self.sheetName[0])
                # print(dsheet)
                try:
                    await self.gsheet.upload(dsheet)
                except IntegrityError as e:
                    # Handle the IntegrityError here
                    # You can choose to log the error, display a message, or perform any necessary actions
                    print("Duplicate entry error:", e)
                
            except asyncio.TimeoutError:
                    em = embed( f"Response timed out, Try again"
                        )
                    await ctx.reply(em)
                    return
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet("Config")#"Copy of Nikke Union raid" #Config
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
            headers = sheet.row_values(1)
            # #print(headers)
            data=sheet.get_all_values()
            data_range = sheet.get("A1:K")
            data = data_range[1:]
            # #print(data)
            dataFrame = pd.DataFrame(data)
            dataFrame.columns = headers
            dataFrame = dataFrame.dropna(how='all')
            dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
            self.boss_list = list(dataFrame['Name'][:5])#makes dataframe into list
            self.boss_list = [x.lower() for x in self.boss_list]
            self.boss_associations = {
                "b1": self.boss_list[0],
                "b2": self.boss_list[1],
                "b3": self.boss_list[2],
                "b4": self.boss_list[3],
                "b5": self.boss_list[4]
            }
            msg = "\n".join(self.boss_list)
            em = discord.Embed(
                title=f"Current Bosses for {self.sheetName[0]}",
                description=f"\n\n{msg}",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
            )
            em.set_footer(text=f"GLOBAL - {ctx.guild.name}")
            await ctx.reply(em)
            em = embed( f"Commands are configured!"
                    )
            await ctx.reply(em)
        
    @commands.command(aliases=["n"], usage=f"<boss_name*: string> <member: @member>",description="Opt in for notifications for a specific boss")
    @commands.guild_only()
    async def notify(self, ctx: commands.Context, boss_name:str.lower, member: discord.Member = None): #sends boss info to table
        """Checks to make sure its not in a specific channel. Firsts checks to see what role the user has because
        if the sheet is not selected then it will ERROR out. To prevent that we check Coordinator role then run 
        &select command. If user doesnt have the role then it will ERROR out that theres no bosses in boss_list
        If everything works, pings user in channel_id by storing it in the database for future reference.
        Args:
            ctx (commands.Context): discord.ext commands for client
            boss_name (str.lower): name of a boss in boss_list
            member (discord.Member, optional): user's ID or discord tag. Defaults to None.
        """
        if ctx.channel.id != 1052240945032220732:
            desired_role_name = "Coordinator"
            desired_role = discord.utils.get(ctx.author.roles, name=desired_role_name)
            if not self.boss_list and desired_role is not None:
                await self.select(ctx)
            else:
                if boss_name in self.boss_list:
                    user = member or ctx.author
                    channel_id = 1108865038799876177 #channel id for boss ping/notifications
                    channel = ctx.guild.get_channel(channel_id)
                    await self.notifs.store(boss_name, user.id, channel_id)
                    await ctx.send(f"{user.mention}, you will be notified in {channel.mention} when {boss_name} is up!")
                else:
                    em = discord.Embed(
                    title=f"",
                    description=f"{boss_name} isnt in the list or the sheet has not been configured.\n **Have a Coordinator use &select**",
                    color=BotSettings.EMBED_COLOR,
                    timestamp=datetime.now()
                    )
                    em.set_footer(text=f"{ctx.guild.name}")
                    await ctx.reply(em)
                
    @commands.command(aliases=["h","hitters","hit"], usage=f"<day*: integer> <member: @member>",description="Checks current hitters on current boss on a specific day") #checks hitters // NEED TO CHANGE THIS FUNCTION TO NOT HAVE BOSS_NAME ->AUTO GET BOSS
    @commands.guild_only() 
    async def hitter(self, ctx: commands.Context, day: int, member: discord.Member = None):
        """Checks to make sure its not in a specific channel. Checks day arg and sorts it to respective worksheet(sheet_name). Looks into database to make sure it
        has the latest sheet(sheetName). Grabs headers from google sheet. Grabs all values. Combines them and puts them in a Pandas DataFrame. Drops all empty values,
        all empty account columns, or duplicated empty columns. Locates last boss(boss_name), then Checks database for Users. Returns those users and put them in 
        a list to display on an embed.
        Args:
            ctx (commands.Context): discord.ext commands for client
            day (int): passing the number arg for respective day in the command
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        """
        if ctx.channel.id != 1052240945032220732:
            user = member or ctx.author
            if day == 1:
                sheet_name = 'Hits D1'
            elif day == 2:
                sheet_name = 'Hits D2'
            # elif day =="3":
            #     sheet_name = 'Hits D3' #this should be the name of the google sheet TAB.
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet(sheet_name)
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
            headers = sheet.row_values(1)
            data=sheet.get_all_values()
            data_range = sheet.get("A1:K")
            data = data_range[1:]
            dataFrame = pd.DataFrame(data)
            dataFrame.columns = headers
            dataFrame = dataFrame.dropna(how='all')
            dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
            dataFrame = dataFrame.dropna(axis=1, how='all')
            dataFrame = dataFrame.dropna(subset=['Account'])
            boss_name = dataFrame.iloc[-2]['Full boss name'] #boss_name
            users = await self.pr3.get_hit(boss_name, day) #all hitters under that specific boss

            data = []
            for i, member in enumerate(users, start=1):
                if i > 10:
                    break
                user_id = int(member[0])
                
                member_name = self.client.get_user(user_id)
                
                #print(member_name)
                if member_name is None:
                    member_name = f"User ID {user_id}"
                data.append(f"**{i}).**  {member_name}")
            
            msg = "\n".join(data)

            em = discord.Embed(
                title=f"Boss: {boss_name}, Day: {day}",
                description=f"\n\n{msg}",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
            )
            em.set_footer(text=f"GLOBAL - {ctx.guild.name}")
            await ctx.reply(em)
            
    @commands.command(aliases=["st"], usage=f"<day*: integer> <member*: @member>", description="Add a hitter to current boss on a specific day, this will auto-add to notifications") #adds hitters // // NEED TO CHANGE THIS FUNCTION TO NOT HAVE BOSS_NAME ->AUTO GET BOSS
    @commands.guild_only()
    async def start(self, ctx: commands.Context, day: str, member: discord.Member):
        """Checks to make sure its not in a specific channel. Sets channel_id for notificaitons. 
        Checks day arg and sorts it to respective worksheet(sheet_name). Looks into database to make sure it
        has the latest sheet(sheetName). Grabs headers from google sheet. Grabs all values. Combines them and puts them in a Pandas DataFrame. Drops all empty values,
        all empty account columns, or duplicated empty columns. Locates last boss(boss_name), Adds user to that boss to be in the embed for Hitters.
        Gets the next boss coming up and adds User to next_boss notification.
        Args:
            ctx (commands.Context): discord.ext commands for client
            day (str): passing the number arg for respective day in the command
            member (discord.Member, optional): user's ID or discord tag. Defaults to None.
        """        
        if ctx.channel.id != 1052240945032220732:
            user = member
            # channel = ctx.channel
            channel_id = 1108865038799876177 #channel for boss pings/notifications
            if day == "1":
                sheet_name = 'Hits D1'
            elif day == "2":
                sheet_name = 'Hits D2'
            # elif day =="3":
            #     sheet_name = 'Hits D3' #this should be the name of the google sheet TAB.
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet(sheet_name)#"Copy of Nikke Union raid" #Config
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
            headers = sheet.row_values(1)
            data=sheet.get_all_values()
            data_range = sheet.get("A1:K")
            data = data_range[1:]
            dataFrame = pd.DataFrame(data)
            dataFrame.columns = headers
            dataFrame = dataFrame.dropna(how='all')
            dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
            dataFrame = dataFrame.dropna(axis=1, how='all')
            dataFrame = dataFrame.dropna(subset=['Account'])
            boss_name = dataFrame.iloc[-2]['Full boss name'] #boss_name
            # users = await self.pr3.get_hit(boss_name, day) #all hitters under that specific boss
            await self.pr3.add_boss(boss_name, day, user.id)
            # hitters = await self.pr3.hitters(user.id,boss_name, day)
            em = embed( f"added {member}: {boss_name} to Day:{day}\n")
            await ctx.reply(em)
            matching_boss = None
            # Iterate over the boss_associations dictionary
            for key, value in self.boss_associations.items():
                if value.lower() in boss_name.lower():
                    matching_boss = {key: value}
                    break
            #print(matching_boss)
            search_value = str(list(matching_boss.values())[0]).strip('[]')
            #print(search_value)
            self.boss_list = [x.lower() for x in self.boss_list]
            #print(self.boss_list)
            if search_value in self.boss_list:
                index = self.boss_list.index(search_value)
                next_value = self.boss_list[index + 1] if index + 1 < len(self.boss_list) else None
                #print("Next value:", next_value)
            else:
                print("Search value not found in the list.")
            #auto add hitters to notifications
            await self.notifs.store(next_value, user.id, channel_id)
                
    @commands.command(aliases=["b","lb","last"], usage=f"<day*: integer>", description="Get last boss info according to the specified day") #get last boss info according to what day
    @commands.guild_only()
    async def boss(self, ctx: commands.Context, day:str):
        """Checks to make sure its not in a specific channel. Checks day arg and sorts it to respective worksheet(sheet_name). Looks into database to make sure it
        has the latest sheet(sheetName). Grabs headers from google sheet. Grabs all values. Combines them and puts them in a Pandas DataFrame. Drops all empty values,
        all empty account columns, or duplicated empty columns. Locates last boss(boss_name) and their HP remaining. Puts info in an embed.
        Args:
            ctx (commands.Context): discord.ext commands for client
            day (str): passing the number arg for respective day in the command
        """
        if ctx.channel.id != 1052240945032220732:
            if day == "1":
                sheet_name = 'Hits D1'
            elif day == "2":
                sheet_name = 'Hits D2'
            # elif day =="3":
            #     sheet_name = 'Hits D3' #this should be the name of the google sheet TAB.
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet(sheet_name)#"Copy of Nikke Union raid" #Config
                rhits=gc.open(self.sheetName[0]).worksheet("Accounts")
                # print(rhits)
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
            headers = sheet.row_values(1)
            data=sheet.get_all_values()
            data_range = sheet.get("A1:K")
            hit_data = rhits.get("M3:N3")
            # print(hit_data[0])
            hit_data = hit_data[0]
            data = data_range[1:]
            dataFrame = pd.DataFrame(data)
            dataFrame.columns = headers
            dataFrame = dataFrame.dropna(how='all')
            dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
            dataFrame = dataFrame.dropna(axis=1, how='all')
            dataFrame = dataFrame.dropna(subset=['Account'])
    
            try:
                df_last = dataFrame.iloc[-2]['Full boss name']   
                df_hp = dataFrame.iloc[-2]['Boss HP remaining']
                msg2 = df_last
                msg = df_hp
            except IndexError:
                em = embed( f"You must enter an Account name in the google sheet first!"
                        )
                await ctx.reply(em)
            
            em = discord.Embed(
                title=f"Last Boss Data For Day {day}",
                description=f"\n\n{msg2}: {msg} hp remaining\n Hits remaining: {hit_data[1]}",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
            )
            await ctx.reply(em)

    @commands.command(aliases=["u","unleash"], usage=f"<day*: integer or string> <all*: all> <member: @member>", description="Clear all hitters and notify those that are opt-in") #function needs to be changed for boss_name // needs to auto_get
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def unleashed(self, ctx: commands.Context, day: str, all: str = None, member: discord.Member = None,):
        """Checks to make sure its not in a specific channel. Checks day arg and sorts it to respective worksheet(sheet_name). Looks into database to make sure it
        has the latest sheet(sheetName). Grabs headers from google sheet. Grabs all values. Combines them and puts them in a 2 Pandas DataFrames. Drops all empty values,
        all empty account columns, or duplicated empty columns. If all arg is present then it will delete all records under hitters in database. Then checks 
        database for notifications if the next boss is up for that specific user.
        Args:
            ctx (commands.Context): discord.ext commands for client
            day (str): passing the number arg for respective day in the command
            all (str, optional): Overwrite arg for the command. Defaults to None.
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        """
        if ctx.channel.id != 1052240945032220732:
            user = member or ctx.author
            if day == "1":
                sheet_name = 'Hits D1'
            elif day == "2":
                sheet_name = 'Hits D2'
            # elif day =="3":
            #     sheet_name = 'Hits D3' #this should be the name of the google sheet TAB.
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet(sheet_name)#"Copy of Nikke Union raid" #Config
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
            headers = sheet.row_values(1)
            data=sheet.get_all_values()
            data_range = sheet.get("A1:K")
            data = data_range[1:]
            dataFrame = pd.DataFrame(data)
            df2 = pd.DataFrame(data)
            df2.columns = headers
            df2 = df2.dropna(how='all')
            df2 = df2.loc[:, ~df2.columns.duplicated()]
            df2['Account'] = df2['Account'].str.strip()
            df2['Account'] = df2['Account'].replace('', np.nan)
            df2 = df2.dropna(subset=['Account'])
            dataFrame.columns = headers
            dataFrame = dataFrame.dropna(how='all')
            dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
            dataFrame = dataFrame.dropna(axis=1, how='all')
            dataFrame = dataFrame.dropna(subset=['Account'])
            boss_name = dataFrame.iloc[-2]['Full boss name'] #boss_name
            # users = await self.pr3.get_hit(boss_name, day) #all hitters under that specific boss
            if all == "all":
                await self.pr3.deleteall()
                em = discord.Embed(
                title=f"",
                description=f"deleted all records",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
                )
                em.set_footer(text=f"{ctx.guild.name}")
                await ctx.reply(em)
            await self.pr3.ur_open(user)
            #when removing a user check if the boss is the same and if it isnt update the event notification
            # users = await self.pr3.get_ur(user)
            await self.pr3.delete_hitter(user.id,boss_name, day)
            if len(df2) >= 2:
                Last = df2.iloc[-2]['Next boss?']
            else:
                print("Have not configured the sheet")
                # Handle the case when there are not enough rows in the DataFrame
                # Print an error message or perform an alternative action
            Last2 = dataFrame.iloc[-2]['Full boss name']
            boss_associations = {
                "b1": self.boss_list[0],
                "b2": self.boss_list[1],
                "b3": self.boss_list[2],
                "b4": self.boss_list[3],
                "b5": self.boss_list[4]
            }
            #boss_associations['b1'] will return 'Vulcan'.
            # boss_associations2 = {
            #     self.boss_list[0]: "b1",
            #     self.boss_list[1]: "b2",
            #     self.boss_list[2]: "b3",
            #     self.boss_list[3]: "b4",
            #     self.boss_list[4]: "b5"
            # }
            # Find the matching boss name for Last2
            matching_boss = None

            # Iterate over the boss_associations dictionary
            for key, value in boss_associations.items():
                if value.lower() in Last2.lower():
                    matching_boss = {key: value}
                    break
            search_value = str(list(matching_boss.values())[0]).strip('[]')
            self.boss_list = [x.lower() for x in self.boss_list]
            if search_value in self.boss_list:
                index = self.boss_list.index(search_value)
                next_value = self.boss_list[index + 1] if index + 1 < len(self.boss_list) else None
            else:
                print("Search value not found in the list.")
            current_boss = Last
            if current_boss == "TRUE":
                await self.event3(ctx, search_value)
            else:
                pass
    
    @commands.command(aliases=["d","del","remove","rmve"], usage=f"<day*: integer or string> <member: @member>", description="Deletes one hitter from the list '&start' then notifies if opt-in") #function needs to be changed for boss_name // needs to auto_get
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def delete(self, ctx: commands.Context,day: str, member: discord.Member = None):
        """Checks to make sure its not in a specific channel. Checks day arg and sorts it to respective worksheet(sheet_name). Looks into database to make sure it
        has the latest sheet(sheetName). Grabs headers from google sheet. Grabs all values. Combines them and puts them in a 2 Pandas DataFrames. Drops all empty values,
        all empty account columns, or duplicated empty columns. If all arg is present then it will delete all records under hitters in database. Then checks 
        database for notifications if the next boss is up for that specific user.
        Args:
            ctx (commands.Context): discord.ext commands for client
            day (str): passing the number arg for respective day in the command
            member (discord.Member, optional): user's ID or discord tag. Defaults to authors ID.
        """
        if ctx.channel.id != 1052240945032220732:
            em = discord.Embed(
                title=f"",
                description=f"deleted {user}'s previous hit!",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
            )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(em)
            user = member or ctx.author
            if day == "1":
                sheet_name = 'Hits D1'
            elif day == "2":
                sheet_name = 'Hits D2' #THIS IS FOR ONLY TWO DAYS OF UNION RAID. FOR MORE DAYS ADD MORE ELIF'S EXAMPLE IS COMMENTED
            # elif day =="3":
            #     sheet_name = 'Hits D3' #this should be the name of the google sheet TAB.
            try:
                dsheet = await self.gsheet.use()
                self.sheetName[0] = dsheet[0]
                sheet=gc.open(self.sheetName[0]).worksheet(sheet_name)#"GOOGLE SHEET NAME" #Config TAB
            except gspread.exceptions.SpreadsheetNotFound:
                em = embed( f"Bot is not in spreadsheet, make sure everything is spelled correctly, this is also case-sensitive!"
                        )
                await ctx.reply(em)
                return
            headers = sheet.row_values(1)
            data=sheet.get_all_values()
            data_range = sheet.get("A1:K")
            data = data_range[1:]
            dataFrame = pd.DataFrame(data)
            df2 = pd.DataFrame(data)
            dataFrame.columns = headers
            dataFrame = dataFrame.dropna(how='all')
            dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
            dataFrame = dataFrame.dropna(axis=1, how='all')
            dataFrame = dataFrame.dropna(subset=['Account'])
            boss_name = dataFrame.iloc[-2]['Full boss name'] #boss_name current
            # users = await self.pr3.get_hit(boss_name, day) #all hitters under that specific boss
            await self.pr3.ur_open(user)
            # users = await self.pr3.get_ur(user)
            await self.pr3.delete_hitter(user.id,boss_name, day)
            dataFrame = dataFrame.dropna(subset=['Account'])
            dataFrame['Account'] = dataFrame['Account'].str.strip()
            dataFrame['Account'] = dataFrame['Account'].replace('', np.nan)
            dataFrame = dataFrame.dropna(subset=['Account'])
            df2.columns = headers
            df2 = df2.dropna(how='all')
            df2 = df2.loc[:, ~df2.columns.duplicated()]
            df2 = df2.dropna(subset=['Account'])
            df2['Account'] = df2['Account'].str.strip()
            df2['Account'] = df2['Account'].replace('', np.nan)
            # boss_data = dataFrame.iloc[-2]['Full boss name']
            bd = dataFrame.iloc[-2]['Next boss?']
            # all = "all"
            matching_boss = None
            # Iterate over the boss_associations dictionary
            for key, value in self.boss_associations.items():
                if value.lower() in boss_name.lower():
                    matching_boss = {key: value}
                    break
            search_value = str(list(matching_boss.values())[0]).strip('[]')
            if bd == "TRUE":
                await self.event3(ctx, search_value)
                await self.pr3.deleteall()
            
            if len(df2) >= 2:
                Last = df2.iloc[-2]['Next boss?']
            else:
                print("Have not configured the sheet")
                # Handle the case when there are not enough rows in the DataFrame
                # Print an error message or perform an alternative action
              
    @commands.command(aliases=["r","res"], usage=f"None", description="WARNING: RESETS EVERYTHING. DO AT YOUR OWN RISK")
    @commands.guild_only()
    @commands.has_role("Coordinator")
    async def reset(self, ctx: commands.Context):
        """Checks to make sure its not in a specific channel. Drops database tables. Clears notifications,boss information, and googlesheet info.
        Recreates the tables that were dropped.
        Args:
            ctx (commands.Context): discord.ext commands for client
        """
        if ctx.channel.id != 1052240945032220732:
            await self.pr.drop()
            await self.pr.create_table()
            # await self.pr2.create_table()
            await self.pr3.create_table()
            await self.notifs.create_table()
            await self.gsheet.create_table()
            
            em = discord.Embed(
                title=f"",
                description=f"Full Reset of Everything",
                color=BotSettings.EMBED_COLOR,
                timestamp=datetime.now()
            )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(em)        
        
    @commands.command(aliases=["e3"], usage=f"<boss_name: string>", description="For debug use only, triggers an event")
    @commands.guild_only()
    @commands.is_owner()
    async def event3(self,ctx: commands.Context, boss:str = None):
        """To trigger an event. to pass the boss name for notifications.
        Args:
            ctx (commands.Context): discord.ext commands for client
            boss (str): passing the boss arg to trigger the event
        """
        n1 = await self.notifs.get_user(boss)
        #grab all userid's then notify all first then clear them after
        for i in range(len(n1)):
            member = ctx.guild.get_member(int(n1[i][1]))
            if member:
                await ctx.send(f"{member.mention}, {n1[i][0]} is up!!!")
            else:
                print("...")
        await self.notifs.bossclear(boss)

    @commands.command(usage=f"", description="This command is to check if settings are configured")
    @commands.guild_only()
    async def check(self, ctx:commands.Context):
        """Checks data for self.boss_list and self.sheetName to see if configs are set.
        Args:
            ctx (commands.Context): discord.ext commands for client
        """
        if ctx.channel.id != 1052240945032220732:
            print("Current Sheet is: ",  self.sheetName)
            print("Current Bosses are: ", self.boss_list)
            em = discord.Embed(
                    title=f"",
                    description=f"If the following are blank then settings arent configure\nPlease run &select if you are a Coordinator/Admin\n **__Current Sheet:__** {self.sheetName}\n **__Current Bosses:__** {self.boss_list}\n",
                    color=BotSettings.EMBED_COLOR,
                    timestamp=datetime.now()
                    )
            em.set_footer(text=f"{ctx.guild.name}")
            await ctx.reply(em)

def setup(client):
    client.add_cog(union_raid(client))
