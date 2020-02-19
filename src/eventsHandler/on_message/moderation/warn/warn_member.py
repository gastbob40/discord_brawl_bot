from typing import List
import discord
import yaml
from src.models.models import Ban, session, Warn
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager


async def warn_member(client: discord.Client, message: discord.Message, args: List[str]):
    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # Check permissions
    if not PermissionsManager.has_perm(message.author, 'warn'):
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
                f"`{config['prefix']}warn <@pseudo> <reason>`\n"
                f"`{config['prefix']}warn <@pseudo> -r <reason_id>`"
            )
        )

    # Check inputs
    if len(message.mentions) != 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                ":x: Erreur dans la commande. Merci de mentionner un utilisateur."
            )
        )

    args = args[1:]

    if len(args) < 2:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande. Merci de mettre une raison."
            )
        )

    # Process code
    with open('run/config/reasons.yml', 'r', encoding='utf8') as file:
        reasons = yaml.safe_load(file)

    current_reason = ""

    if args[0] == '-r':
        # Saved reason
        try:
            for reason_index in args[1:]:
                current_reason += f"- {reasons[int(reason_index)]}\n"
        except:
            return await message.channel.send(
                embed=EmbedsManager.error_embed(
                f":x: Erreur dans la commande. Merci de mettre un index d'erreur valide."
                )
            )
    else:
        # Custom reason
        current_reason = " ".join(args)

    new_warn = Warn(message.mentions[0].id, message.author.id, current_reason)
    session.add(new_warn)
    session.commit()

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            f"⚠ Le membre **{message.mentions[0]}** a été avertit (id `w{new_warn.id}`):\n{current_reason}"
        )
    )
