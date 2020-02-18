from typing import List
import discord
import yaml
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def change_prefix(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not PermissionsManager.has_perm(message.author, 'prefix'):
        await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Vous n'avez pas les permissions pour cette commande."
            )
        )
        return

    # Help message
    if args and args[0] == '-h':
        await message.channel.send(
            embed=EmbedsManager.information_embed(
                "Rappel de la commande de changement de préfix : \n"
                f"`{config['prefix']}prefix <nouveau prefix>`"
            )
        )
        return

    # Check input
    if len(args) != 1:
        await message.channel.send(
            embed=EmbedsManager.error_embed(
                f"Erreur dans la commande.\nRappel : `{config['prefix']}prefix <nouveau prefix>`"
            )
        )
        return

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"⚙ Le préfix `{config['prefix']}` a été changé par `{args[0]}`."
        )
    )

    with open('run/config/config.yml', 'w', encoding='utf8') as outfile:
        yaml.dump(config, outfile, default_flow_style=False, allow_unicode=True)
