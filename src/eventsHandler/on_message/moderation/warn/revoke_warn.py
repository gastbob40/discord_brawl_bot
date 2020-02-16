from typing import List
import discord
from src.models.models import Ban, session, Warn


async def revoke_warn(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    if len(args) != 1:
        await message.channel.send(f":x: Erreur dans la commande, merci de spécifier l'index de l'avertissement.")
        return

    if not args[0].startswith("w"):
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    index = int(args[0][1:])
    current_warn: Warn = session.query(Warn).filter_by(id=index).first()

    if current_warn is None:
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    if not current_warn.is_active:
        await message.channel.send(f":x: Erreur, cet avertissement est déjà révoqué.")
        return

    current_warn.is_active = False
    session.commit()

    await message.channel.send(f"🔨 L'avertissement **{args[0]}** a été révoqué.")