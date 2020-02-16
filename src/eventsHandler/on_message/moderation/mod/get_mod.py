from datetime import datetime, timedelta
from typing import List

import discord

from src.models.models import session, Kick, Warn, Ban, Mute


async def get_mod(client: discord.Client, message: discord.Message, args: List[str]):
    if not message.author.guild_permissions.kick_members:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    # Check parameters
    # ?mod @pseudo
    if len(message.mentions) != 1:
        await message.channel.send(f":x: Erreur dans la commande. Merci de mentionner un utilisateur.")
        return

    target: discord.Member = message.mentions[0]

    infos = {
        'warns': session.query(Warn).filter_by(target_id=target.id, is_active=True).all(),
        'rwarns': session.query(Warn).filter_by(target_id=target.id, is_active=False).all(),

        'kicks': session.query(Kick).filter_by(target_id=target.id, is_active=True).all(),
        'rkicks': session.query(Kick).filter_by(target_id=target.id, is_active=False).all(),

        'bans': session.query(Ban).filter_by(target_id=target.id, is_active=True).all(),
        'rbans': session.query(Ban).filter_by(target_id=target.id, is_active=False).all(),

        'mutes': session.query(Mute).filter_by(target_id=target.id, is_active=True).all(),
        'rmutes': session.query(Mute).filter_by(target_id=target.id, is_active=False).all()
    }

    embed = discord.Embed()
    embed.set_author(name=f'{target.display_name} (ID: {target.id})', icon_url=target.avatar_url) \
        .add_field(name=f'Voici les informations sur {target.display_name}:',
                   value=f'Sourdine : {len(infos["mutes"]) + len(infos["rmutes"])}'
                         f' (dont {len(infos["rmutes"])} révoqués).\n'
                         f'Avertissements : {len(infos["warns"]) + len(infos["rwarns"])}'
                         f' (dont {len(infos["rwarns"])} révoqués).\n'
                         f'Exclusions : {len(infos["kicks"]) + len(infos["rkicks"])}'
                         f' (dont {len(infos["rkicks"])} révoqués).\n'
                         f'Bannissements : {len(infos["bans"]) + len(infos["rbans"])}'
                         f' (dont {len(infos["rbans"])} révoqués).\n') \
        .set_footer(text=f"{client.user.display_name}", icon_url=client.user.avatar_url)
    embed.timestamp = datetime.now() - timedelta(hours=2)

    await message.channel.send(embed=embed)

    for type in ['warns', 'kicks', 'bans']:
        embed = discord.Embed() \
            .set_author(name=f'{type} de {target.display_name} (ID: {target.id})', icon_url=target.avatar_url)

        if infos[type]:
            for things in infos[type]:
                embed.add_field(name=f"{type} par {message.guild.get_member(things.author_id)}"
                                     f" (ID: {type[0]}{things.id})",
                                value=f"Le {things.date.day}/{things.date.month}/{things.date.year}"
                                      f" à {things.date.hour}:{things.date.minute}"
                                      f" pour : \n {things.reason}")
            await message.channel.send(embed=embed)
