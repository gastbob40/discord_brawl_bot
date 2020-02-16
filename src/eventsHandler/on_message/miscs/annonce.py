from typing import List
import discord
import yaml


async def annonce_msg(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.administrator:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    if len(message.channel_mentions) != 1:
        await message.channel.send \
            (f":x: Erreur dans la commande. Merci de specifier un channel")
        return

    channel: discord.TextChannel = message.channel_mentions[0]
    content = ' '.join(args[1:])

    try:
        await channel.send(content)
        await message.channel.send(f"Le message a bien été envoyé dans {channel} : \n ```{content}```")
    except:
        await message.channel.send("Je n'ai pas les permissions pour ce salon.")

