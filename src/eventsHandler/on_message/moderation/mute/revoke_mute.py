from typing import List
import discord
from src.models.models import Mute, session


async def revoke_mute(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    if len(args) != 1:
        await message.channel.send(f":x: Erreur dans la commande, merci de spécifier l'index du mute.")
        return

    if not args[0].startswith("m"):
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    index = int(args[0][1:])
    current_mute: Mute = session.query(Mute).filter_by(id=index).first()

    if current_mute is None:
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    if not current_mute.is_active:
        await message.channel.send(f":x: Erreur, ce mute est déjà révoqué.")
        return

    current_mute.is_active = False
    session.commit()

    target: discord.Member = message.guild.get_member(current_mute.target_id)
    for channel in message.guild.channels:
        if not target.permissions_in(channel).send_messages:
            await channel.set_permissions(target,
                                          overwrite=None)

    await message.channel.send(f"⚠ Le mute **{args[0]}** a été révoqué.")