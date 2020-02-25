from typing import List
import discord
import yaml
from src.models.models import CustomCommand, session
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def permissions(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not message.author.guild_permissions.administrator:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Vous n'avez pas les permissions pour cette commande."
            )
        )

    # Help message
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed(
                "Rappel de la commande : \n"
                f"`{config['prefix']}perm list`\n"
                f"`{config['prefix']}perm list <perm_name>`\n"
                f"`{config['prefix']}perm add <perm_name> <@role>`\n"
                f"`{config['prefix']}perm remove <perm_name> <@role>`\n"
            )
        )

    if not args:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: | Erreur dans la commande."
            )
        )

    command = args.pop(0)

    if command not in ['list', 'add', 'remove']:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: | Erreur dans la commande."
            )
        )

    with open('src/_data/permissions.yml', 'r') as file:
        perms = yaml.safe_load(file)

    if command == 'list':
        # Case if we don't specify a perm name
        if not args:
            content = 'Voici les différentes permissions que je peux mettre : \n\n'
            for perm_name in perms.keys():
                content += f' - {perm_name}\n'

            return await message.channel.send(
                embed=EmbedsManager.complete_embed(content)
            )

        else:
            # Case if we specify a perm name
            if not args[0] in perms.keys():
                return await message.channel.send(
                    embed=EmbedsManager.error_embed(
                        f":x: | Hum, je ne trouve pas la permission `{args[0]}`."
                    )
                )

            content = f'Voici les roles ayant la permission `{args[0]}`\n\n'
            for role_id in perms[args[0]]:
                role: discord.Role = message.guild.get_role(role_id)
                content += f' - {role.name} ({role.id}) \n'

            return await message.channel.send(
                embed=EmbedsManager.complete_embed(content)
            )

    elif command == 'add':
        if len(args) < 2 or len(message.role_mentions) != 1:
            return await message.channel.send(
                embed=EmbedsManager.error_embed(
                    f":x: | Erreur dans la commande."
                )
            )

        perm_name = args[0]
        role = message.role_mentions[0]

        if role.id in perms[perm_name]:
            return await message.channel.send(
                embed=EmbedsManager.error_embed(
                    f":x: | Hum, le role `{role.name}` a déjà la permission `{perm_name}`."
                )
            )

        perms[perm_name].append(role.id)
        with open('src/_data/permissions.yml', 'w', encoding='utf8') as outfile:
            yaml.dump(perms, outfile, default_flow_style=False, allow_unicode=True)

        return await message.channel.send(
            embed=EmbedsManager.complete_embed(
                f"Le role `{role.name}` a maintenant la permission `{perm_name}`."
            )
        )

    elif command == 'remove':
        if len(args) < 2 or len(message.role_mentions) != 1:
            return await message.channel.send(
                embed=EmbedsManager.error_embed(
                    f":x: | Erreur dans la commande."
                )
            )

        perm_name = args[0]
        role = message.role_mentions[0]

        if role.id not in perms[perm_name]:
            return await message.channel.send(
                embed=EmbedsManager.error_embed(
                    f":x: | Hum, le role `{role.name}` n'a pas la permission `{perm_name}`."
                )
            )

        perms[perm_name].remove(role.id)
        with open('src/_data/permissions.yml', 'w', encoding='utf8') as outfile:
            yaml.dump(perms, outfile, default_flow_style=False, allow_unicode=True)

        return await message.channel.send(
            embed=EmbedsManager.complete_embed(
                f"Le role `{role.name}` n'a maintenant plus la permission `{perm_name}`."
            )
        )