from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session


async def list_customcommands(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.administrator:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    custom_commands: List[CustomCommand] = session.query(CustomCommand).all()

    content = "Voici les commandes personnalisées :"

    for custom_command in custom_commands:
        content += f'\n - `{custom_command.command}`'

    await message.channel.send(content)
