import discord
import yaml
from src.eventsHandler.on_ready.on_ready import OnReady
from src.eventsHandler.on_message.on_message import OnMessage
from src.eventsHandler.on_reaction_add.on_reaction_add import OnReactionAdd


class EventsHandler:
    @staticmethod
    async def on_ready(client: discord.Client):
        OnReady.login_information(client)

    @staticmethod
    async def on_message(client: discord.Client, message: discord.Message):
        await OnMessage.run(client, message)

    @staticmethod
    async def on_reaction_add(client: discord.client, reaction: discord.Reaction, user: discord.User):
        await OnReactionAdd.check_reaction(client, reaction, user)

