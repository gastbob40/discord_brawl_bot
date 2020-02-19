from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def add_customcommands(client: discord.Client, message: discord.Message, args: List[str]):
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
                f"`{config['prefix']}add_command <name> <content>`"
            )
        )

    # Process code
    if len(args) < 2:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande."
            )
        )

    command_name = args[0]
    command_content = ' '.join(args[1:])

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"{message.author.mention} vient de créer une nouvelle commande :\n"
            f"**Nom :** {command_name}\n"
            f"**Contenue :** {command_content}."
        )
    )

    custom_command = CustomCommand(command_name, command_content)
    session.add(custom_command)
    session.commit()
