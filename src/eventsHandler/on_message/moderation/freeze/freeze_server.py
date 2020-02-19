import asyncio
from typing import List

import discord
import yaml

from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def freeze_server(client: discord.Client, message: discord.Message, args: List[str]):
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
                "Rappel de la commande : \n"
                f"`{config['prefix']}freeze`"
            )
        )

    current_message: discord.Message = await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"{message.author.mention} Vous avez décidé de geler le serveur.\n" +
            f"Confirmer vous ce choix ?"
        )
    )

    await current_message.add_reaction('✅')
    await current_message.add_reaction('❌')

    def check(reaction: discord.Reaction, user: discord.User):
        return user == message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await  message.channel.send(
            embed=EmbedsManager.error_embed(
                f"Vous avez __refusé__ le gel du serveur."
            )
        )
    else:
        if str(reaction.emoji) == '❌':
            return await  message.channel.send(
                embed=EmbedsManager.error_embed(
                    f"Vous avez __refusé__ le gel du serveur."
                )
            )

        await message.channel.send(
            embed=EmbedsManager.complete_embed(
                "Le serveur a été gelé"
            )
        )

        members: List[discord.Member] = message.guild.members

        for member in members:
            if not member.guild_permissions.manage_messages:
                for channel in message.guild.channels:
                    if member.permissions_in(channel).read_messages:
                        await channel.set_permissions(member,
                                                      send_messages=False)
