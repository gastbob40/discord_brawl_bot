from typing import List
import discord
from src.models.models import session, Kick


async def revoke_kick(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.kick_members:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    if len(args) != 1:
        await message.channel.send(f":x: Erreur dans la commande, merci de spécifier l'index de l'expulsion.")
        return

    if not args[0].startswith("k"):
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    index = int(args[0][1:])
    current_kick: Kick = session.query(Kick).filter_by(id=index).first()

    if current_kick is None:
        await message.channel.send(f":x: Erreur, index invalide.")
        return

    if not current_kick.is_active:
        await message.channel.send(f":x: Erreur, cet avertissement est déjà révoqué.")
        return

    current_kick.is_active = False
    session.commit()

    await message.channel.send(f"👢 L'expulsion **{args[0]}** a été révoqué.")