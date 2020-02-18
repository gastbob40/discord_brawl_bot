import discord
import yaml

from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def get_reasons_list(client: discord.Client, message: discord.Message):
    if not PermissionsManager.has_perm(message.author, 'manage_reason'):
        await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Vous n'avez pas les permissions pour cette commande."
            )
        )
        return

    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    content = f"{message.author.mention} voici la liste des **raisons** des sanctions :\n"

    for i in range(len(reasons)):
        content += f"\n**Raison {i+1} :** {reasons[i]}"

    await message.channel.send(
        embed=EmbedsManager.complete_embed(content)
    )