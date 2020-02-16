import asyncio
from typing import List
import discord
import yaml


async def remove_reason(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    if len(args) != 1:
        await message.channel.send(f":x: Merci de mettre le numéro de la raison à retirer.")
        return

    index = int(args[0]) - 1

    if index >= len(reasons):
        await message.channel.send(f":x: Merci de mettre un index valide.")
        return

    current_message: discord.Message = await message.channel.send \
        (f"{message.author.mention} La raison **{reasons[index]}** va être retiré de la liste.\n"
         f"Confirmer vous ce choix ?")

    await current_message.add_reaction('✅')
    await current_message.add_reaction('❌')

    def check(reaction, user):
        return user == message.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await message.channel.send(f"Vous avez __refusé__ la suppresion de la raison **{reasons[index]}** de la liste")
    else:
        if str(reaction.emoji) == '❌':
            await message.channel.send(
                f"Vous avez __refusé__ la suppresion de la raison **{reasons[index]}** de la liste")
            return

        await message.channel.send(f"La raison **{reasons[index]}** a été __définitivement__ retiré de la liste.")
        reasons.pop(index)
        with open('run/config/reasons.yml', 'w', encoding='utf8') as outfile:
            yaml.dump(reasons, outfile, default_flow_style=False, allow_unicode=True)

