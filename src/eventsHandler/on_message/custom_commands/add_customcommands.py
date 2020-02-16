from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session


async def add_customcommands(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.administrator:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    # Check parameters
    # ?add_command name content
    if len(args) < 2:
        await message.channel.send(f":x: Erreur dans la commande.")
        return

    command_name = args[0]
    command_content = ' '.join(args[1:])

    await message.channel.send(f"{message.author.mention} vient de créer une nouvelle commande :\n"
                               f"**Nom :** {command_name}\n"
                               f"**Contenue :** {command_content}.")

    custom_command = CustomCommand(command_name, command_content)
    session.add(custom_command)
    session.commit()
