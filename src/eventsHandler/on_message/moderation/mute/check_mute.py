from datetime import datetime
from typing import List

import discord

from src.models.models import Mute, session


async def check_mute(client: discord.Client, message: discord.Message):
    mutes: List[Mute] = session.query(Mute).filter_by(is_active=True).all()

    now = datetime.now()

    for mute in mutes:
        try:
            if mute.end_time < now:
                # Remove mute
                target: discord.Member = message.guild.get_member(mute.target_id)
                for channel in message.guild.channels:
                    if not target.permissions_in(channel).send_messages:
                        await channel.set_permissions(target,
                                                      overwrite=None)
                session.commit()
        except:
            session.commit()
