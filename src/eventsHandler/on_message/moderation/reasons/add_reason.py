from typing import List
import discord
import yaml

from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def add_reason(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not PermissionsManager.has_perm(message.author, 'manage_reason'):
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Vous n'avez pas les permissions pour cette commande."
            )
        )

    # Help message
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed(
                "Rappel de la commande de changement de préfix : \n"
                f"`{config['prefix']}reason_add <reason>`"
            )
        )

    # Check inputs
    if len(args) < 2:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Merci de mettre une raison d'au moins deux mots."
            )
        )

    # Process code
    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)
    reasons.append((' '.join(args)))

    with open('run/config/reasons.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(reasons, outfile, default_flow_style=False, allow_unicode=True)

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"{message.author.mention} La raison `{reasons[-1]}` a été ajouté à la liste.\n"
            f"Son numéro d'attribution est le {len(reasons)}."
        )
    )
