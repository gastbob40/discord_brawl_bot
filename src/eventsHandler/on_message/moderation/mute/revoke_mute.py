from typing import List
import discord
import yaml

from src.models.models import Mute, session
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def revoke_mute(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

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
                "Rappel de la commande : \n"
                f"`{config['prefix']}rmute <mute_id>`"
            )
        )

    if len(args) != 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande, merci de spécifier l'index du mute."
            )
        )

    if not args[0].startswith("m"):
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Erreur, index invalide."
            )
        )

    index = int(args[0][1:])
    current_mute: Mute = session.query(Mute).filter_by(id=index).first()

    if current_mute is None:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Erreur, index invalide."
            )
        )

    if not current_mute.is_active:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Erreur, ce mute est déjà révoqué."
            )
        )

    current_mute.is_active = False
    session.commit()

    target: discord.Member = message.guild.get_member(current_mute.target_id)
    for channel in message.guild.channels:
        if not target.permissions_in(channel).send_messages:
            await channel.set_permissions(target,
                                          overwrite=None)

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"⚠ Le mute **{args[0]}** a été révoqué."
        )
    )
