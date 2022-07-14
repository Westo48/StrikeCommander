import utils.coc_utils as coc_utils
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from data.StrikeCommander_Client_Data import StrikeCommander_Data
from database.StrikeModel import (
    StrikeModel,
    select_strike_model_active,
    select_strike_model_all)
from responders.RazBotDB_Responder import (
    read_user)
from database.RemovalReasonModel import (
    RemovalReasonModel,
    select_removal_reason_model_active,
    select_removal_reason_model_all)
from errors.errors_db import (
    NotFoundError)


async def autocomp_unit(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    unit_list = []
    unit_list.extend(coc_utils.get_home_troop_order())
    unit_list.extend(coc_utils.get_spell_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


async def autocomp_supertroop(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    unit_list = []
    unit_list.extend(coc_utils.get_super_troop_order())

    autocomp_list = []
    for unit in unit_list:
        if user_input.lower() in unit.lower():
            autocomp_list.append(unit)

    del autocomp_list[25:]
    return [unit for unit in autocomp_list]


async def autocomp_emoji_name(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    emoji_name_list = []
    emoji_list = StrikeCommander_Data().emojis
    for emoji in emoji_list:
        emoji_name_list.append(emoji.coc_name)

    autocomp_list = []
    for emoji_name in emoji_name_list:
        if user_input.lower() in emoji_name.lower():
            autocomp_list.append(emoji_name)

    del autocomp_list[25:]
    return [emoji_name for emoji_name in autocomp_list]


async def autocomp_strike_model_name_all(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    db_user = read_user(inter.author.id)

    if db_user is None:
        return []

    if not db_user.super_user:
        return []

    try:
        strike_models: list[StrikeModel] = select_strike_model_all()

    except NotFoundError as arg:
        print(arg)
        return []

    strike_model_name_list = []

    for strike_model in strike_models:
        strike_model_name_list.append(strike_model.name)

    autocomp_list = []
    for strike_model_name in strike_model_name_list:
        if user_input.lower() in strike_model_name.lower():
            autocomp_list.append(strike_model_name)

    del autocomp_list[25:]
    return [strike_model_name for strike_model_name in autocomp_list]


async def autocomp_strike_model_name_active(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    try:
        strike_models: list[StrikeModel] = select_strike_model_active()

    except NotFoundError as arg:
        print(arg)
        return []

    strike_model_name_list = []

    for strike_model in strike_models:
        strike_model_name_list.append(strike_model.name)

    autocomp_list = []
    for strike_model_name in strike_model_name_list:
        if user_input.lower() in strike_model_name.lower():
            autocomp_list.append(strike_model_name)

    del autocomp_list[25:]
    return [strike_model_name for strike_model_name in autocomp_list]


async def autocomp_removal_reason_model_name_all(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    db_user = read_user(inter.author.id)

    if db_user is None:
        return []

    if not db_user.super_user:
        return []

    try:
        removal_reason_models: list[RemovalReasonModel] = select_removal_reason_model_all(
        )

    except NotFoundError as arg:
        print(arg)
        return []

    removal_reason_model_name_list = []

    for removal_reason_model in removal_reason_models:
        removal_reason_model_name_list.append(removal_reason_model.name)

    autocomp_list = []
    for removal_reason_model_name in removal_reason_model_name_list:
        if user_input.lower() in removal_reason_model_name.lower():
            autocomp_list.append(removal_reason_model_name)

    del autocomp_list[25:]
    return [removal_reason_model_name for removal_reason_model_name in autocomp_list]


async def autocomp_removal_reason_model_name_active(
    inter: ApplicationCommandInteraction,
    user_input: str
):
    try:
        removal_reason_models: list[RemovalReasonModel] = select_removal_reason_model_active(
        )

    except NotFoundError as arg:
        print(arg)
        return []

    removal_reason_model_name_list = []

    for removal_reason_model in removal_reason_models:
        removal_reason_model_name_list.append(removal_reason_model.name)

    autocomp_list = []
    for removal_reason_model_name in removal_reason_model_name_list:
        if user_input.lower() in removal_reason_model_name.lower():
            autocomp_list.append(removal_reason_model_name)

    del autocomp_list[25:]
    return [removal_reason_model_name for removal_reason_model_name in autocomp_list]


command_param_dict = {
    'superuser_strike_model': commands.Param(
        name="option",
        description="*optional* options for superuser strike model returns",
        default="show active",
        choices=[
            "show active", "show all", "edit", "rename",
            "toggle active", "add", "delete"
        ]
    ),
    'strike_model_name': commands.Param(
        name="strike_model_name",
        description="name of Strike Model to search for",
        default=None
    ),
    'required_strike_model_name': commands.Param(
        name="strike_model_name",
        description="name of Strike Model to search for"
    ),
    'strike_model_description': commands.Param(
        name="description",
        description="*optional* description of strike model",
        default=None
    ),
    'strike_weight': commands.Param(
        name="strike_weight",
        description="*optional* weight of strike",
        default=None,
        choices=[
            1, 2, 3, 4, 5
        ]
    ),
    'strike_model_persistent': commands.Param(
        name="persistent",
        description="*optional* default value for strike persistent",
        default=None
    ),
    'strike_model_rollover_days': commands.Param(
        name="rollover_days",
        description="*optional* default value for strike rollover days",
        default=None
    ),
    'strike_model_new_strike_name': commands.Param(
        name="new_strike_name",
        description="*optional* new name for a strike model",
        default=None
    ),
    'superuser_removal_reason_model': commands.Param(
        name="option",
        description="*optional* options for superuser removal reason model returns",
        default="show active",
        choices=[
            "show active", "show all", "edit", "rename",
            "toggle active", "add", "delete"
        ]
    ),
    'removal_reason_model_name': commands.Param(
        name="removal_reason_model_name",
        description="name of Removal Reason Model to search for",
        default=None
    ),
    'required_removal_reason_model_name': commands.Param(
        name="removal_reason_model_name",
        description="name of Removal Reason Model to search for"
    ),
    'removal_reason_model_description': commands.Param(
        name="description",
        description="*optional* description of removal reason model",
        default=None
    ),
    'removal_reason_model_new_removal_reason_name': commands.Param(
        name="new_removal_reason_name",
        description="*optional* new name for a removal reason model",
        default=None
    ),
    'superuser_strike': commands.Param(
        name="option",
        description="*optional* options for superuser Strike returns",
        default="delete",
        choices=[
            "delete"
        ]
    ),
    'playerstrike_show': commands.Param(
        name="option",
        description="*optional* options for Player Strike show returns",
        default="overview",
        choices=[
            "overview", "active", "all"
        ]
    ),
    'playerstrike_war': commands.Param(
        name="option",
        description="*optional* options for Player Strike war returns",
        default="each",
        choices=[
            "each", "any"
        ]
    ),
    'playerstrike_add': commands.Param(
        name="option",
        description="*optional* options for Player Strike add returns",
        default="player tag",
        choices=[
            "player tag"
        ]
    ),
    'playerstrike_edit': commands.Param(
        name="option",
        description="*optional* options for Player Strike edit returns",
        choices=[
            "toggle persistent", "rollover days"
        ]
    ),
    'userstrike_show': commands.Param(
        name="option",
        description="*optional* options for User Strike show returns",
        default="overview",
        choices=[
            "overview", "active", "all"
        ]
    ),
    'userstrike_edit': commands.Param(
        name="option",
        description="*optional* options for User Strike edit returns",
        choices=[
            "toggle persistent", "rollover days"
        ]
    ),
    'rollover_days': commands.Param(
        name="rollover_days",
        description="*optional* strike rollover days",
        default=None
    ),
    'required_rollover_days': commands.Param(
        name="rollover_days",
        description="strike rollover days"
    ),
    'persistent': commands.Param(
        name="persistent",
        description="*optional* strike persistent value",
        default=None
    ),
    'player_strike_id': commands.Param(
        name="player_strike_id",
        description="ID of the Player Strike"
    ),
    'user_strike_id': commands.Param(
        name="user_strike_id",
        description="ID of the User Strike"
    ),
    'user': commands.Param(
        name="user",
        description="*optional* user to specify for command",
        default=None
    ),
    'required_user': commands.Param(
        name="user",
        description="user to specify for command"
    ),
    'clan_role': commands.Param(
        name="clan_role",
        description="*optional* clan role to use linked clan",
        default=None
    ),
    'tag': commands.Param(
        name="tag",
        description="*optional* tag to search",
        default=None
    ),
    'unit_name': commands.Param(
        name="unit_name",
        description="clash of clans unit name to search for"
    ),
    'super_troop': commands.Param(
        name="super_troop",
        description="*optional* super troop name to search clan donations",
        default=None
    ),
    'unit_type': commands.Param(
        name="unit_type",
        description="*optional* type of unit to return information for",
        default="all",
        choices=[
            "all", "hero", "pet", "troop", "spell", "siege"
        ]
    ),
    'war_selection': commands.Param(
        name="cwl_war_selection",
        description="*optional* cwl war selection",
        default=None,
        choices=[
            "previous", "current", "upcoming"
        ]
    ),
    'missed_attacks': commands.Param(
        name="missed_attacks",
        description="*optional* specified missed attack count",
        default=None,
        choices=[1, 2]
    ),
    'channel': commands.Param(
        name="channel",
        description="*optional* channel to announce the message",
        default=None
    ),
    'message': commands.Param(
        name="message",
        description="message to send the specified channel"
    ),
    'required_tag': commands.Param(
        name="tag",
        description="tag to search"
    ),
    'api_key': commands.Param(
        name="api_key",
        description="api key provided from in game",
        default=None
    ),
    'role': commands.Param(
        name="role",
        description="mentioned discord role"
    ),
    'rank_name': commands.Param(
        name="rank_name",
        description="*optional* requested rank to link to role",
        default=None,
        choices=[
            "leader", "co-leader", "elder", "member", "uninitiated"
        ]
    ),
    'coc_name': commands.Param(
        name="coc_name",
        description="name of emoji to search for"
    ),
    'player_info': commands.Param(
        name="option",
        description="*optional* options for player info returns",
        default="overview",
        choices=[
            "overview", "recruit"
        ]
    ),
    'player_unit': commands.Param(
        name="option",
        description="*optional* options for player unit returns",
        default="all",
        choices=[
            "all", "find"
        ]
    ),
    'clan_lineup': commands.Param(
        name="option",
        description="*optional* options for clan lineup returns",
        default="overview",
        choices=[
            "overview", "member", "count"
        ]
    ),
    'clan_warpreference': commands.Param(
        name="option",
        description="*optional* options for clan warpreference returns",
        default="overview",
        choices=[
            "overview", "count"
        ]
    ),
    'clan_supertroop': commands.Param(
        name="option",
        description="*optional* options for clan supertroop returns",
        default="active",
        choices=[
            "active", "donate"
        ]
    ),
    'star_count': commands.Param(
        name="star_count",
        description="*optional* star count selection for open bases",
        default=2,
        choices=[
            0, 1, 2
        ]
    ),
    'war_stars': commands.Param(
        name="option",
        description="*optional* options for war star returns",
        default="stars",
        choices=[
            "stars", "attacks"
        ]
    ),
    'war_lineup': commands.Param(
        name="option",
        description="*optional* options for war lineup returns",
        default="clan",
        choices=[
            "overview", "clan", "member"
        ]
    ),
    'cwl_scoreboard': commands.Param(
        name="option",
        description="*optional* options for cwl scoreboard returns",
        default="group",
        choices=[
            "group", "rounds", "clan"
        ]
    ),
    'coc_name': commands.Param(
        name="emoji_name",
        description="options for emoji name"
    ),
    'discord_role': commands.Param(
        name="option",
        description="*optional* options for discord role returns",
        default="me",
        choices=[
            "me", "member", "all"
        ]
    ),
    'discord_nickname': commands.Param(
        name="option",
        description="*optional* options for discord nickname returns",
        default="me",
        choices=[
            "me", "member", "all"
        ]
    ),
    'discord_user': commands.Param(
        name="option",
        description="*optional* options for discord user returns",
        default="clan",
        choices=[
            "player", "clan"
        ]
    ),
    'discord_user_tag': commands.Param(
        name="player_tag",
        description="*optional* player tag to search linked user",
        default=None
    ),
    'client_user': commands.Param(
        name="option",
        description="*optional* options for client user returns",
        default="claim",
        choices=[
            "claim", "remove"
        ]
    ),
    'client_player': commands.Param(
        name="option",
        description="*optional* options for client player returns",
        default="show",
        choices=[
            "show", "sync", "update", "claim", "remove"
        ]
    ),
    'client_player_tag': commands.Param(
        name="player_tag",
        description="*optional* player tag",
        default=None
    ),
    'required_player_tag': commands.Param(
        name="player_tag",
        description="*required* player tag",
    ),
    'admin_guild': commands.Param(
        name="option",
        description="*optional* options for client guild returns",
        default="claim",
        choices=[
            "claim"
        ]
    ),
    'client_clan': commands.Param(
        name="option",
        description="*optional* options for client clan returns",
        default="show",
        choices=[
            "show"
        ]
    ),
    'admin_clan': commands.Param(
        name="option",
        description="*optional* options for admin clan returns",
        default="show",
        choices=[
            "show", "claim", "remove"
        ]
    ),
    'admin_role': commands.Param(
        name="option",
        description="*optional* options for client role returns",
        default="show",
        choices=[
            "show", "remove"
        ]
    ),
    'role_mention': commands.Param(
        name="role",
        description="*optional* mentioned discord role",
        default=None
    ),
    'admin_clan_rank_role': commands.Param(
        name="option",
        description="*optional* options for admin clan and rank role returns",
        default="claim",
        choices=[
            "claim"
        ]
    ),
    'admin_user': commands.Param(
        name="option",
        description="*optional* options for admin user returns",
        default="player",
        choices=[
            "player", "sync", "update"
        ]
    ),
    'admin_player': commands.Param(
        name="option",
        description="*optional* options for admin player returns",
        choices=[
            "claim", "remove"
        ]
    ),
    'superuser_user': commands.Param(
        name="option",
        description="*optional* options for superuser user returns",
        default="players",
        choices=[
            "players", "sync", "claim", "remove"
        ]
    ),
    'superuser_guild': commands.Param(
        name="option",
        description="*optional* options for superuser guild returns",
        default="show",
        choices=[
            "show", "remove", "leave"
        ]
    ),
    'guild_id': commands.Param(
        name="guild_id",
        description="*optional* id for guild",
        default=None
    ),
    'superuser_admin': commands.Param(
        name="option",
        description="*optional* options for superuser admin returns",
        default="show",
        choices=[
            "show", "toggle", "remove"
        ]
    ),
    'superuser_player': commands.Param(
        name="option",
        description="*optional* options for superuser player returns",
        default="user",
        choices=[
            "user", "claim", "remove"
        ]
    ),
    'superuser_count': commands.Param(
        name="option",
        description="*optional* options for superuser count returns",
        default="user",
        choices=[
            "user", "player", "guild", "clan"
        ]
    ),
}
