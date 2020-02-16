from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session


async def remove_customcommands(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.administrator:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    if len(args) != 1:
        await message.channel.send(f":x: Erreur dans la commande.")
        return

    command_name = args[0]
    custom_commands: List[CustomCommand] = session.query(CustomCommand).filter_by(command=command_name).all()

    if len(custom_commands) != 1:
        await message.channel.send(f":x: Erreur. Je ne trouve pas cette commande.")
        return

    session.delete(custom_commands[0])
    session.commit()

    await message.channel.send(f"Je viens de supprimer la commande **{command_name}**.")
