from typing import List

import discord
import yaml

from src.models.models import Mute, session


async def mute_member(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    # Check parameters
    # ?mute @pseudo raison
    # ?mute @pseudo -r raison
    if len(message.mentions) != 1:
        await message.channel.send(f":x: Erreur dans la commande. Merci de mentionner un utilisateur.")
        return

    if len(args) < 3:
        await message.channel.send(f":x: Erreur dans la commande. Merci de mettre une raison.")
        return

    args = args[1:]

    if not args[0].isdigit():
        await message.channel.send(f":x: Erreur dans la commande. Merci de mettre une durée valide.")
        return

    duration: int = int(args[0])

    args = args[1:]

    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    current_reason = ""

    if args[0] == '-r':
        # Saved reason
        try:
            for reason_index in args[1:]:
                current_reason += f"- {reasons[int(reason_index)]}\n"
        except:
            await message.channel.send(f":x: Erreur dans la commande. Merci de mettre un index d'erreur valide.")
            return

    else:
        # Custom reason
        current_reason = " ".join(args)

    new_mute = Mute(message.mentions[0].id, message.author.id, current_reason, duration)
    session.add(new_mute)
    session.commit()

    # Remove permission
    target: discord.Member = message.mentions[0]
    for channel in message.guild.channels:
        if target.permissions_in(channel).read_messages:
            await channel.set_permissions(target,
                                          send_messages=False)

    await message.channel.send(
        f"⚠ Le membre **{message.mentions[0]}** a été mute (id `m{new_mute.id}`):\n{current_reason}")
