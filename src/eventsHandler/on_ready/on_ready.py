import discord
import yaml


class OnReady:
    @staticmethod
    def login_information(client: discord.Client):
        print('We have logged in as {0.user}'.format(client))

