import discord
from discord.ext import commands
from discord.ui import View, Button
from readymade import *
from base import Bot
import math
from discord import ui
from numpy import random
from typing import List, Optional, Tuple


class MyMenu(ui.View):
    def __init__(self,client: Bot,
        *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

        self.add_item(Button(label='Red', style=discord.ButtonStyle.secondary, custom_id='red_button'))
        self.add_item(Button(label='Green', style=discord.ButtonStyle.secondary, custom_id='green_button'))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message('This menu is only for the command invoker.', ephemeral=True)
        return False

    @View.button(label='Red', style=discord.ButtonStyle.secondary, custom_id='red_button')
    async def on_red_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button_choice = 'red'
        await interaction.response.edit_message(embed=discord.Embed(title="Button Menu", description=f"You clicked the {button_choice} button."))
        await self.process_button_choice(button_choice)

    @View.button(label='Green', style=discord.ButtonStyle.secondary, custom_id='green_button')
    async def on_green_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        button_choice = 'green'
        await interaction.response.edit_message(embed=discord.Embed(title="Button Menu", description=f"You clicked the {button_choice} button."))
        await self.process_button_choice(button_choice)

    async def process_button_choice(self, button_choice):
        print(f"Button choice: {button_choice}")