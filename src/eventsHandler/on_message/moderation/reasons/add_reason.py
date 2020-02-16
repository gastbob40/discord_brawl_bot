from typing import List
import discord
import yaml


async def add_reason(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    if len(args) < 2:
        await message.channel.send(f":x: Merci de mettre une raison d'au moins deux mots.")
        return

    reasons.append((' '.join(args)))

    with open('run/config/reasons.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(reasons, outfile, default_flow_style=False, allow_unicode=True)

    await message.channel.send(f"{message.author.mention} La raison **{reasons[-1]}** a été ajouté à la liste.\n"
                               f"Son numéro d'attribution est le {len(reasons)}.")
