import discord
from readymade import *
from base import Bot
from discord import ui
import gspread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

class MyMenu(ui.View):
    def __init__(self, client: Bot, account: str, damage: int, sheetName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sheetName = sheetName
        self.client = client
        self.account = account
        self.damage = damage
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/PATH/TO/YOUR/.JSON/FOR GOOGLE API/..', scopes)
        self.gc = gspread.authorize(credentials)
        guath = GoogleAuth
        drive = GoogleDrive(guath)
        
    async def process_button_choice(self, button: discord.ui.Button, interaction: discord.Interaction):
        button_choice = str(button.label)
        if button_choice == "Day 2":
            day = "Hits D2"
            sheet = self.gc.open(self.sheetName[0]).worksheet(day)
            account_column = sheet.col_values(1)  # Assuming account column is the first column (column index 1)
            damage_column = sheet.col_values(2)  # Assuming damage column is the second column (column index 2)
            blankci1 = account_column.index("") + 1  # Find the index of the first blank cell (+1 to convert to row number
            blankci2 = next((i+1 for i, value in enumerate(damage_column) if value.strip() == ""), None)
            if blankci2 is None:
                # Update the account and damage values in row 2
                sheet.update_cell(2, 1, self.account)  # Update account value in column 1 (A) of row 2
                sheet.update_cell(2, 2, self.damage)  # Update damage value in column 2 (B) of row 2
            else:
                # Update the first empty cell of the account column
                sheet.update_cell(blankci1, 1, self.account)
                
                # Update the first empty cell of the damage column
                sheet.update_cell(blankci2, 2, self.damage)   
        elif button_choice == "Day 1":
            day = "Hits D1" 
            sheet = self.gc.open(self.sheetName[0]).worksheet(day)
            account_column = sheet.col_values(1)  # Assuming account column is the first column (column index 1)
            damage_column = sheet.col_values(2)  # Assuming damage column is the second column (column index 2)
            blankci1 = account_column.index("") + 1  # Find the index of the first blank cell (+1 to convert to row number)
            # blankci2 = damage_column.index("") + 1  # Find the index of the first blank cell (+1 to convert to row number)
            blankci2 = next((i+1 for i, value in enumerate(damage_column) if value.strip() == ""), None)
            if blankci2 is None:
                # Update the account and damage values in row 2
                sheet.update_cell(2, 1, self.account)  # Update account value in column 1 (A) of row 2
                sheet.update_cell(2, 2, self.damage)  # Update damage value in column 2 (B) of row 2
            else:
                # Update the first empty cell of the account column
                sheet.update_cell(blankci1, 1, self.account)
                
                # Update the first empty cell of the damage column
                sheet.update_cell(blankci2, 2, self.damage)
        #example of adding another button choice.
        # elif button_choice == "Day 3":
        #     day = "Hits D3" 
        #     sheet = self.gc.open(self.sheetName[0]).worksheet(day)
        #     account_column = sheet.col_values(1)  # Assuming account column is the first column (column index 1)
        #     damage_column = sheet.col_values(2)  # Assuming damage column is the second column (column index 2)
        #     blankci1 = account_column.index("") + 1  # Find the index of the first blank cell (+1 to convert to row number)
        #     # blankci2 = damage_column.index("") + 1  # Find the index of the first blank cell (+1 to convert to row number)
        #     blankci2 = next((i+1 for i, value in enumerate(damage_column) if value.strip() == ""), None)
        #     if blankci2 is None:
        #         # Update the account and damage values in row 2
        #         sheet.update_cell(2, 1, self.account)  # Update account value in column 1 (A) of row 2
        #         sheet.update_cell(2, 2, self.damage)  # Update damage value in column 2 (B) of row 2
        #     else:
        #         # Update the first empty cell of the account column
        #         sheet.update_cell(blankci1, 1, self.account)
                
        #         # Update the first empty cell of the damage column
        #         sheet.update_cell(blankci2, 2, self.damage)
 
    @ui.button(label='Day 1', style=discord.ButtonStyle.secondary, custom_id='1')
    async def dayone(self, button: discord.ui.Button, interaction: discord.Interaction):
        button_choice = 'Day 1'
        await interaction.response.edit_message(embed=discord.Embed(title="", description=f"Attempting to append Union {button_choice}..."))
        await self.process_button_choice(button, interaction)
        await self.message.delete()
        followup_content = "`Data Appended`"
        await interaction.followup.send(content=followup_content, ephemeral=True)
        
    @ui.button(label="Day 2", style=discord.ButtonStyle.secondary, custom_id='2')
    async def daytwo(self, button: discord.ui.Button, interaction: discord.Interaction):
        button_choice = 'Day 2'
        await interaction.response.edit_message(embed=discord.Embed(title="", description=f"Attempting to append Union {button_choice}..."))
        await self.process_button_choice(button, interaction)
        await self.message.delete()
        followup_content = "`Data Appended`"
        await interaction.followup.send(content=followup_content, ephemeral=True)
    #example of adding another button to the view. make sure to change the async def function name and everything associated with it 
    # @ui.button(label="Day 3", style=discord.ButtonStyle.secondary, custom_id='3')
    # async def daythree(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     button_choice = 'Day 3'
    #     await interaction.response.edit_message(embed=discord.Embed(title="", description=f"Attempting to append Union {button_choice}..."))
    #     await self.process_button_choice(button, interaction)
    #     await self.message.delete()
    #     followup_content = "`Data Appended`"
    #     await interaction.followup.send(content=followup_content, ephemeral=True)
