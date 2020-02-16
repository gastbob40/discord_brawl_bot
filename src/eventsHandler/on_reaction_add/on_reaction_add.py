import discord

from .check_reaction_role import check_reaction_role


class OnReactionAdd:
    @staticmethod
    async def check_reaction(client: discord.client, reaction: discord.Reaction, user: discord.User):
        check_reaction_role(client, reaction, user)
