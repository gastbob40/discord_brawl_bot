from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def remove_customcommands(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not PermissionsManager.has_perm(message.author, 'custom_commands'):
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Vous n'avez pas les permissions pour cette commande."
            )
        )

    # Help message
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed(
                "Rappel de la commande : \n"
                f"`{config['prefix']}remove_command <command_id>`"
            )
        )

    # Check inputs
    if len(args) != 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande."
            )
        )

    command_name = args[0]
    custom_commands: List[CustomCommand] = session.query(CustomCommand).filter_by(command=command_name).all()

    if len(custom_commands) != 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur. Je ne trouve pas cette commande."
            )
        )

    session.delete(custom_commands[0])
    session.commit()

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"Je viens de supprimer la commande **{command_name}**."
        )
    )
