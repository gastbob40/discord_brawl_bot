import discord
import yaml
from typing import List

# Import from databse
from src.models.models import session, CustomCommand

# Prefix manipulation
from src.eventsHandler.on_message.miscs.change_prefix import change_prefix

# Ban manipulation
from src.eventsHandler.on_message.moderation.ban.ban_member import ban_member
from src.eventsHandler.on_message.moderation.ban.revoke_ban import revoke_ban
# Kick manipulation
from src.eventsHandler.on_message.moderation.kick.kick_member import kick_member
from src.eventsHandler.on_message.moderation.kick.revoke_kick import revoke_kick
from src.eventsHandler.on_message.moderation.reasons.add_reason import add_reason
# Reason manipuation
from src.eventsHandler.on_message.moderation.reasons.get_reasons_list import get_reasons_list
from src.eventsHandler.on_message.moderation.reasons.remove_reason import remove_reason
# Warn manipulation
from src.eventsHandler.on_message.moderation.warn.revoke_warn import revoke_warn
from src.eventsHandler.on_message.moderation.warn.warn_member import warn_member
# Mute manipulation
from src.eventsHandler.on_message.moderation.mute.mute_member import mute_member
from src.eventsHandler.on_message.moderation.mute.revoke_mute import revoke_mute
from src.eventsHandler.on_message.moderation.mute.check_mute import check_mute
# Mod manipulation
from src.eventsHandler.on_message.moderation.mod.get_mod import get_mod
# Freeze manipulation
from src.eventsHandler.on_message.moderation.freeze.freeze_server import freeze_server
from src.eventsHandler.on_message.moderation.freeze.unfreeze_server import unfreeze_server

# Announce manipulation
from src.eventsHandler.on_message.miscs.annonce import annonce_msg

# Custom command manipulation
from src.eventsHandler.on_message.custom_commands.add_customcommands import add_customcommands
from src.eventsHandler.on_message.custom_commands.remove_customcommands import remove_customcommands
from src.eventsHandler.on_message.custom_commands.list_customcommands import list_customcommands


class OnMessage:
    @staticmethod
    async def run(client: discord.Client, message: discord.Message):
        with open('run/config/config.yml', 'r') as file:
            config = yaml.safe_load(file)

        if message.author.bot:
            return

        await check_mute(client, message)

        if not message.content.startswith(config['prefix']):
            return

        command = message.content[1:].split(' ')[0]
        args = message.content[1:].split(' ')[1:]

        # Check for custom command
        custom_commands: List[CustomCommand] = session.query(CustomCommand).filter_by(command=command).all()

        if len(custom_commands) == 1:
            await message.channel.send(custom_commands[0].content)

        elif command == 'prefix':
            await change_prefix(client, message, args)

        # Reason management
        elif command == 'reason_list':
            await get_reasons_list(client, message)
        elif command == 'reason_add':
            await add_reason(client, message, args)
        elif command == 'reason_remove':
            await remove_reason(client, message, args)

        # Ban management
        elif command == 'ban':
            await ban_member(client, message, args)
        elif command == 'rban':
            await revoke_ban(client, message, args)

        # Kick management
        elif command == 'kick':
            await kick_member(client, message, args)
        elif command == 'rkick':
            await revoke_kick(client, message, args)

        # Warn management
        elif command == 'warn':
            await warn_member(client, message, args)
        elif command == 'rwarn':
            await revoke_warn(client, message, args)

        # Mute management
        elif command == 'mute':
            await mute_member(client, message, args)
        elif command == 'rmute':
            await revoke_mute(client, message, args)

        # Mod management
        elif command == "mod":
            await get_mod(client, message, args)

        # Annonce management
        elif command == "annonce":
            await annonce_msg(client, message, args)

        # Free management
        elif command == "freeze":
            await freeze_server(client, message, args)
        elif command == "rfreeze":
            await unfreeze_server(client, message, args)

        # Custom command mangement
        elif command == "add_command":
            await add_customcommands(client, message, args)
        elif command == "remove_command":
            await remove_customcommands(client, message, args)
        elif command == "list_command":
            await list_customcommands(client, message, args)
