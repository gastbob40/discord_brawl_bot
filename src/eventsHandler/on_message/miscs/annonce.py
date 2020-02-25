from typing import List
import discord
import yaml

from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def annonce_msg(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not PermissionsManager.has_perm(message.author, 'annonce'):
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
                f"`{config['prefix']}annonce <#channel> <reason>`"
            )
        )

    if len(message.channel_mentions) != 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande. Merci de specifier un channel"
            )
        )

    channel: discord.TextChannel = message.channel_mentions[0]
    content = ' '.join(args[1:])

    try:
        await channel.send(
            embed=EmbedsManager.complete_embed(content)
        )
        await message.channel.send(
            embed=EmbedsManager.complete_embed(
                f"Le message a bien été envoyé dans {channel} : \n {content}"
            )
        )
    except:
        await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Je n'ai pas les permissions pour ce salon."
            )
        )
