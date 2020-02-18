import asyncio
from typing import List
import discord
import yaml

from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def remove_reason(client: discord.Client, message: discord.Message, args: List[str]):
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
                f"`{config['prefix']}reason_remove <number>`"
            )
        )

    # Check inputs
    if len(args) != 1:
        return message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Merci de mettre le numéro de la raison à retirer."
            )
        )

    # Process code
    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    index = int(args[0]) - 1

    if index >= len(reasons):
        return message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Merci de mettre un index valide."
            )
        )

    current_message: discord.Message = await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"{message.author.mention} La raison **{reasons[index]}** va être retiré de la liste.\n"
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
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f"Vous avez __refusé__ la suppresion de la raison `{reasons[index]}` de la liste."
            )
        )
    else:
        if str(reaction.emoji) == '❌':
            return await message.channel.send(
                embed=EmbedsManager.error_embed(
                    f"Vous avez __refusé__ la suppresion de la raison `{reasons[index]}` de la liste."
                )
            )

        await message.channel.send(
            embed=EmbedsManager.complete_embed(
                f"La raison **{reasons[index]}** a été __définitivement__ retiré de la liste."
            )
        )

        reasons.pop(index)
        with open('run/config/reasons.yml', 'w', encoding='utf8') as outfile:
            yaml.dump(reasons, outfile, default_flow_style=False, allow_unicode=True)
