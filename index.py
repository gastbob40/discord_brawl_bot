import discord
import yaml
from discord.utils import get

from src.eventsHandler.eventsHandler import EventsHandler

# Get configuration
with open('run/config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

client = discord.Client()


@client.event
async def on_ready():
    await EventsHandler.on_ready(client)

    # #ith open('run/data/reactions.yml', 'r') as file:
    #   reactions = yaml.safe_load(file)

    # for reaction in reactions:
    #    message = await client. \
    #        get_channel(reaction['channel_id']). \
    #        fetch_message(reaction['message_id'])
    #    for r in reaction['reactions']:
    #        emoji = [
    #            x for x in client.emojis
    #            if str(x) == r['emoji_id']
    #        ]
    #        if emoji:
    #            await message.add_reaction(emoji[0])


@client.event
async def on_message(message: discord.Message):
    await EventsHandler.on_message(client, message)


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    with open('run/data/reactions.yml', 'r') as file:
        reactions = yaml.safe_load(file)

    reaction = [x for x in reactions
                if x['channel_id'] == payload.channel_id
                and x['message_id'] == payload.message_id]

    if not reaction:
        return

    emoji_role = [x for x in reaction[0]['reactions']
                  if x['emoji_id'] == str(payload.emoji)]

    if not emoji_role:
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)

    role: discord.Role = guild.get_role(emoji_role[0]['role_id'])
    await guild.get_member(payload.user_id).add_roles(role)
    print(role.name)


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    with open('run/data/reactions.yml', 'r') as file:
        reactions = yaml.safe_load(file)

    reaction = [x for x in reactions
                if x['channel_id'] == payload.channel_id
                and x['message_id'] == payload.message_id]

    if not reaction:
        return

    emoji_role = [x for x in reaction[0]['reactions']
                  if x['emoji_id'] == str(payload.emoji)]

    if not emoji_role:
        return

    guild: discord.Guild = client.get_guild(payload.guild_id)

    role: discord.Role = guild.get_role(emoji_role[0]['role_id'])
    await guild.get_member(payload.user_id).remove_roles(role)
    print(role.name)


client.run(config['token'])
