from typing import List

import discord
import yaml

from src.models.models import session, Kick


async def kick_member(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.kick_members:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    # Check parameters
    # ?kick @pseudo raison
    # ?kick @pseudo -r raison
    if len(message.mentions) != 1:
        await message.channel.send(f":x: Erreur dans la commande. Merci de mentionner un utilisateur.")
        return

    args = args[1:]

    if len(args) < 2:
        await message.channel.send(f":x: Erreur dans la commande. Merci de mettre une raison.")
        return

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

    new_kick = Kick(message.mentions[0].id, message.author.id, current_reason)
    session.add(new_kick)
    session.commit()

    await message.channel.send(
        f"👢 Le membre **{message.mentions[0]}** a été kické (id `k{new_kick.id}`):\n{current_reason}")

    await message.mentions[0].kick()
