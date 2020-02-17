import discord
import yaml


class PermissionsManager:
    @staticmethod
    def has_perm(member: discord.Member, perm_name: str) -> bool:
        with open('src/_data/permissions.yml', 'r') as file:
            permissions = yaml.safe_load(file)

        if perm_name not in permissions:
            raise Exception(f'{perm_name} not found in configuration file')

        for role in member.roles:
            if role.id in permissions[perm_name]:
                return True

        return False
