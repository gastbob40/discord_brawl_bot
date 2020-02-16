from typing import List
import discord
from src.models.models import Ban, session


async def revoke_ban(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.ban_members:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    if len(args) != 1:
        await message.channel.send(f":x: Erreur dans la commande, merci de spécifier l'index du ban.")
        return

    if not args[0].startswith("b"):
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    index = int(args[0][1:])
    current_ban: Ban = session.query(Ban).filter_by(id=index).first()

    if current_ban is None:
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    if not current_ban.is_active:
        await message.channel.send(f":x: Erreur, ce bannissement est déjà révoqué.")
        return

    current_ban.is_active = False
    session.commit()

    await message.channel.send(f"🔨 Le bannissement **{args[0]}** a été révoqué.")