import discord
import yaml


async def get_reasons_list(client: discord.Client, message: discord.Message):
    if not message.author.guild_permissions.manage_messages:
        await message.channel.send(f":x: Vous n'avez pas les permissions pour cette commande.")
        return

    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    content = f"{message.author.mention} voici la liste des **raisons** des sanctions :\n"

    for i in range(len(reasons)):
        content += f"\n**Raison {i+1} :** {reasons[i]}"

    await message.channel.send(content)
