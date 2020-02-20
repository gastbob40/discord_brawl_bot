from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session
from src.utils.embeds_manager import EmbedsManager


async def list_customcommands(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Help message
    if args and args[0] == '-h':
        return await message.channel.send(
                embed=EmbedsManager.information_embed(
                    "Rappel de la commande : \n"
                    f"`{config['prefix']}list_command`"
                )
            )

    custom_commands: List[CustomCommand] = session.query(CustomCommand).all()

    content = "Voici les commandes personnalisées :"

    for custom_command in custom_commands:
        content += f'\n - `{custom_command.command}`'

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            content
        )
    )
