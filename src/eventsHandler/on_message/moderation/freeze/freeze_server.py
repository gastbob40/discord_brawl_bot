import asyncio
from typing import List

import discord


async def freeze_server(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.administrator:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    current_message: discord.Message = await message.channel.send \
        (f"{message.author.mention} Vous avez décidé de geler le serveur.\n" +
         f"Confirmer vous ce choix ?")

    await current_message.add_reaction('✅')
    await current_message.add_reaction('❌')

    def check(reaction, user):
        return user == message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await message.channel.send(f"Vous avez __refusé__ le gel du serveur.")
    else:
        if str(reaction.emoji) == '❌':
            await message.channel.send(
                f"Vous avez __refusé__ le gel du serveur.")
            return

        await message.channel.send(f"Le serveur a été gelé")

        members: List[discord.Member] = message.guild.members

        for member in members:
            if not member.guild_permissions.manage_messages:
                for channel in message.guild.channels:
                    if member.permissions_in(channel).read_messages:
                        await channel.set_permissions(member,
                                                      send_messages=False)
