import discord
import yaml


def check_reaction_role(client: discord.client, reaction: discord.Reaction, user: discord.User):
    with open('run/data/reactions.yml', 'r') as file:
        reactions = yaml.safe_load(file)

    reactions = [x for x in reactions
                 if x['channel_id'] == reaction.message.channel.id
                 and x['message_id'] == reaction.message.id]


