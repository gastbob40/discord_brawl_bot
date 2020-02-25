from typing import List
import discord
import yaml

from src.models.models import Ban, session, Warn
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def revoke_warn(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not PermissionsManager.has_perm(message.author, 'warn'):
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
                f"`{config['prefix']}rwarn <warn_id>`"
            )
        )

    # Check inputs
    if len(args) != 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande, merci de spécifier l'index de l'avertissement."
            )
        )

    if not args[0].startswith("w"):
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur, index invalide."
            )
        )

    # Process code
    index = int(args[0][1:])
    current_warn: Warn = session.query(Warn).filter_by(id=index).first()

    if current_warn is None:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur, index invalide."
            )
        )

    if not current_warn.is_active:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Erreur, cet avertissement est déjà révoqué."
            )
        )

    current_warn.is_active = False
    session.commit()

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"🔨 L'avertissement **{args[0]}** a été révoqué."
        )
    )
