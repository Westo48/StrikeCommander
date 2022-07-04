from database import (
    RazBotDB_user as user,
    RazBotDB_player as player,
    RazBotDB_guild as guild,
    RazBotDB_clan as clan,
    RazBotDB_clan_role as clan_role,
    StrikeModel,
    RemovalReasonModel
)
from errors.errors_db import (
    NotFoundError,
    ConflictError
)

# user


def read_user(discord_user_id):
    """
        finds user in db, if user is not found returns None

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: user object (discord_id, admin, super_user)
    """
    user_data = user.select_user(discord_user_id)
    # if user data is found return user
    if user_data:
        user_discord_id, user_admin, user_super_user = user_data
        return user.User(user_discord_id, bool(
            user_admin), bool(user_super_user))
    else:
        return None


def read_user_from_tag(player_tag):
    """
        finds user with given player tag in db,
        if user is not found returns None

        Args:
            player_tag (str): requested player tag

        Returns:
            obj: user object (discord_id, admin, super_user)
    """
    user_data = user.select_user_from_tag(player_tag)
    # if user data is found return user
    if user_data:
        user_discord_id, user_admin, user_super_user = user_data
        return user.User(user_discord_id, bool(
            user_admin), bool(user_super_user))
    else:
        return None


def read_user_admin_all():
    """
        finds all admin users,
        returns empty list if no users are found

        Returns:
            list: list of user object (discord_id, admin, super_user)
    """
    user_data_list = list(user.select_user_admin_all())
    user_list = []

    for user_data in user_data_list:
        user_discord_id, user_admin, user_super_user = user_data
        user_list.append(user.User(
            user_discord_id, bool(user_admin), bool(user_super_user)
        ))

    return user_list


# player

def claim_player(discord_user_id, player_tag):
    """
        claims player and returns player object instance, 
        if player has been previously claimed return None

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: player object (player_tag, active)
    """

    # check if user has another player
    active_player_data = player.select_player_active(discord_user_id)

    if active_player_data:
        # if a user has a active player
        player_data = player.insert_player_alt(discord_user_id, player_tag)
    else:
        # if a player does not have a active player
        player_data = player.insert_player_active(discord_user_id, player_tag)

    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def read_player_list(discord_user_id):
    """
        returns all players associated with discord id
        and returns empty list if no players are found

        Args:
            discord_user_id (int): discord id for user

        Returns:
            list: list of player object (player_tag, active)
    """
    player_list = list(player.select_player_all(discord_user_id))
    player_obj_list = []
    for item in player_list:
        player_tag, player_active = item
        player_obj_list.append(player.Player(player_tag, bool(player_active)))
    return player_obj_list


def read_player(discord_user_id, player_tag):
    """
        returns player where discord user id and player tag
        and returns None if no player is found

        Args:
            discord_user_id (int): discord id for user
            player_tag (str): user's player tag

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.select_player_from_user_tag(
        discord_user_id, player_tag)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def read_player_from_tag(player_tag):
    """
        returns player where player tag
        and returns None if no player is found

        Args:
            player_tag (str): user's player tag

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.select_player_from_tag(player_tag)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


def read_player_active(discord_user_id):
    """
        returns user's active player
        and returns None if no player is found

        Args:
            discord_user_id (int): discord id for user

        Returns:
            obj: player object (player_tag, active)
    """
    player_data = player.select_player_active(
        discord_user_id)
    if player_data:
        player_tag, active = player_data
        return player.Player(player_tag, bool(active))
    else:
        return None


# guild

def read_guild(discord_guild_id):
    """
        finds guild in db, if guild is not found returns None

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            obj: guild object (guild_id, admin_user_id,
                bot_channel, active, dev)
    """
    guild_data = guild.select_guild(discord_guild_id)

    if guild_data:
        # if guild data is found return guild
        guild_id, admin_user_id, bot_channel, active, dev = guild_data
        guild_obj = guild.Guild(
            guild_id, admin_user_id, bot_channel, bool(active), bool(dev))
        return guild_obj

    else:
        return None


# clan

def read_clan(discord_guild_id, clan_tag):
    """
        finds clan in db, if clan is not found returns None

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            obj: clan object (guild_id, clan_tag)
    """
    clan_data = clan.select_clan(discord_guild_id, clan_tag)

    if clan_data:
        # if clan data is found return clan
        guild_id, clan_tag = clan_data
        clan_obj = clan.Clan(guild_id, clan_tag)
        return clan_obj

    else:
        return None


def read_clan_list_from_guild(discord_guild_id):
    """
        finds clans in db, if clan is not found returns empty list

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            obj list: list of clan object (guild_id, clan_tag)
    """

    clan_data_list = list(clan.select_clan_all_from_guild(discord_guild_id))
    clan_obj_list = []
    for item in clan_data_list:
        guild_id, clan_tag = item
        clan_obj_list.append(clan.Clan(guild_id, clan_tag))
    return clan_obj_list


# clan role

def read_clan_role(discord_role_id):
    """
        finds clan_role in db, if clan_role is not found returns None

        Args:
            discord_role_id (int): discord id for role

        Returns:
            obj: clan role object 
                (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role(discord_role_id)

    if clan_role_data:
        # if clan role data is found return clan
        discord_guild_id, discord_role_id, clan_tag = clan_role_data
        return clan_role.ClanRole(discord_guild_id, discord_role_id, clan_tag)

    else:
        return None


def read_clan_role_list(discord_role_id_list):
    """
        finds clan_role in db, 
        if no clan_role is not found returns empty list

        Args:
            list
                discord_role_id (int): discord id for role

        Returns:
            list
                obj: clan role object 
                    (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role_from_list(discord_role_id_list)

    clan_role_list = []
    for role in clan_role_data:
        # add each role object to clan_role_list
        discord_guild_id, discord_role_id, clan_tag = role
        clan_role_list.append(clan_role.ClanRole(
            discord_guild_id, discord_role_id, clan_tag))

    return clan_role_list


def read_guild_clan_role(discord_guild_id):
    """
        finds clan_role in db from guild id, 
        if no clan_role is not found returns empty list

        Args:
            discord_guild_id (int): discord id for guild

        Returns:
            list
                obj: clan role object
                    (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role_from_guild(discord_guild_id)

    clan_role_list = []
    for role in clan_role_data:
        # add each role object to clan_role_list
        discord_guild_id, discord_role_id, clan_tag = role
        clan_role_list.append(clan_role.ClanRole(
            discord_guild_id, discord_role_id, clan_tag))

    return clan_role_list


def read_clan_role_from_tag(discord_guild_id, clan_tag):
    """
        finds clan_role in db, if clan_role is not found returns None

        Args:
            discord_guild_id (int): discord id for guild
            clan_tag (str): tag for clan

        Returns:
            obj: clan role object 
                (discord_guild_id, discord_role_id, clan_tag)
    """
    clan_role_data = clan_role.select_clan_role_from_tag(
        discord_guild_id, clan_tag)

    if clan_role_data:
        # if clan role data is found return clan
        discord_guild_id, discord_role_id, clan_tag = clan_role_data
        return clan_role.ClanRole(discord_guild_id, discord_role_id, clan_tag)

    else:
        return None


# Strike Model

def create_strike_model(
    name: str,
    description: str,
    strike_weight: int = 1,
    persistent: bool = False,
    rollover_days: int = 30
):
    """
        add Strike Model to DB

        Args:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int, optional): amount the strike is worth
                defaults to 1
            `persistent` (bool, optional): whether or not the strike is persistent by default
                defaults to False
            `rollover_days` (int, optional): amount of rollover days by default
                defaults to 30

        Raises:
            `ConflictError`: Strike Model with specified name already exists
            `NotFoundError`: Strike Model with specified name not found after insert

        Returns:
            obj: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # insert the strike model
    try:
        query_data = StrikeModel.insert_strike_model(
            name=name, description=description,
            strike_weight=strike_weight, persistent=persistent,
            rollover_days=rollover_days
        )

    except ConflictError as arg:
        raise ConflictError(arg)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_model: StrikeModel.StrikeModel = StrikeModel.query_data_to_obj(
        query_data=query_data)

    return strike_model


def read_strike_model_from_name(name: str):
    """
        selects Strike Models from the given name

        Args:
            `name` (str): Strike Model Name

        Raises:
            `NotFoundError`: Strike Model with specified name not found

        Returns:
            obj: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # query strike model
    try:
        query_data = StrikeModel.select_strike_model_from_name(name=name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_model: StrikeModel.StrikeModel = StrikeModel.query_data_to_obj(
        query_data=query_data)

    return strike_model


def read_strike_model_active():
    """
        selects all active Strike Models

        Args:

        Raises:
            `NotFoundError`: no active Strike Models found

        Returns:
            list[obj]: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # query strike model
    try:
        query_data = StrikeModel.select_strike_model_active()

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_models: list[StrikeModel.StrikeModel] = []

    for data in query_data:
        strike_models.append(StrikeModel.query_data_to_obj(data))

    return strike_models


def read_strike_model_all():
    """
        selects all Strike Models

        Args:

        Raises:
            `NotFoundError`: no Strike Models found

        Returns:
            list[obj]: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # query strike model
    try:
        query_data = StrikeModel.select_strike_model_all()

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_models: list[StrikeModel.StrikeModel] = []

    for data in query_data:
        strike_models.append(StrikeModel.query_data_to_obj(data))

    return strike_models


def toggle_strike_model_active(name: str):
    """
        toggles the active value for the specified Strike Model

        Args:
            `name` (str): Strike Model Name

        Raises:
            `NotFoundError`: Strike Model with specified name not found

        Returns:
            obj: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # toggle active value for strike model
    try:
        query_data = StrikeModel.update_strike_model_active_toggle(name=name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_model: StrikeModel.StrikeModel = StrikeModel.query_data_to_obj(
        query_data=query_data
    )

    return strike_model


def edit_strike_model(
    name: str,
    description: str = None,
    strike_weight: int = None,
    persistent: bool = None,
    rollover_days: int = None
):
    """
        edits the given values for the specified Strike Model

        Args:
            `name` (str): Strike name
            `description` (str, optional): Strike description
                defaults to None
            `strike_weight` (int, optional): amount the strike is worth
                defaults to None
            `persistent` (bool, optional): whether or not the strike is persistent by default
                defaults to None
            `rollover_days` (int, optional): amount of rollover days by default
                defaults to None

        Raises:
            `NotFoundError`: Strike Model with specified name not found

        Returns:
            obj: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # edit given values for strike model
    try:
        query_data = StrikeModel.update_strike_model_edit(
            name=name, description=description,
            strike_weight=strike_weight, persistent=persistent,
            rollover_days=rollover_days)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_model: StrikeModel.StrikeModel = StrikeModel.query_data_to_obj(
        query_data=query_data
    )

    return strike_model


def edit_strike_model_name(
    current_name: str, new_name: str
):
    """
        edits the name for a specified Strike Model

        Args:
            `current_name` (str): Strike Model's current name
            `new_name` (str): Strike Model's name to change to

        Raises:
            `NotFoundError`: Strike Model with specified name not found after insert
            `ConflictError`: Strike Model with specified name already exists

        Returns:
            obj: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # edit given values for strike model
    try:
        query_data = StrikeModel.update_strike_model_edit_name(
            current_name=current_name, new_name=new_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    except ConflictError as arg:
        raise ConflictError(arg)

    strike_model: StrikeModel.StrikeModel = StrikeModel.query_data_to_obj(
        query_data=query_data
    )

    return strike_model


def delete_strike_model(name: str):
    """
        toggles the active value for the specified Strike Model

        Args:
            `name` (str): Strike Model Name

        Raises:
            `NotFoundError`: Strike Model not found after deletion

        Returns:
            obj: `Strike Model` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    # query strike model
    try:
        query_data = StrikeModel.delete_strike_model(name=name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    strike_model: StrikeModel.StrikeModel = StrikeModel.query_data_to_obj(
        query_data=query_data)

    return strike_model


# Removal Reason Model

def create_removal_reason_model(
    name: str, description: str
):
    """
        add Removal Reason Model to DB

        Args:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description

        Raises:
            `ConflictError`: Removal Reason Model with specified name 
                already exists
            `NotFoundError`: Removal Reason Model with specified name 
                not found after insert

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # insert the removal reason model
    try:
        query_data = RemovalReasonModel.insert_removal_reason_model(
            name=name, description=description
        )

    except ConflictError as arg:
        raise ConflictError(arg)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_model: RemovalReasonModel.RemovalReasonModel = (
        RemovalReasonModel.query_data_to_obj(query_data=query_data)
    )

    return removal_reason_model


def read_removal_reason_model_from_name(name: str):
    """
        selects Removal Reason Models from the given name

        Args:
            `name` (str): Removal Reason Model Name

        Raises:
            `NotFoundError`: Removal Reason Model with specified name not found

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # query removal reason model
    try:
        query_data = RemovalReasonModel.select_removal_reason_model_from_name(
            name=name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_model: RemovalReasonModel.RemovalReasonModel = RemovalReasonModel.query_data_to_obj(
        query_data=query_data)

    return removal_reason_model


def read_removal_reason_model_active():
    """
        selects all active Removal Reason Models

        Args:

        Raises:
            `NotFoundError`: no active Removal Reason Models found

        Returns:
            list[obj]: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # query removal reason model
    try:
        query_data = RemovalReasonModel.select_removal_reason_model_active()

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_models: list[RemovalReasonModel.RemovalReasonModel] = []

    for data in query_data:
        removal_reason_models.append(
            RemovalReasonModel.query_data_to_obj(data))

    return removal_reason_models


def read_removal_reason_model_all():
    """
        selects all Removal Reason Models

        Args:

        Raises:
            `NotFoundError`: no Removal Reason Models found

        Returns:
            list[obj]: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # query removal reason model
    try:
        query_data = RemovalReasonModel.select_removal_reason_model_all()

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_models: list[RemovalReasonModel.RemovalReasonModel] = []

    for data in query_data:
        removal_reason_models.append(
            RemovalReasonModel.query_data_to_obj(data))

    return removal_reason_models


def toggle_removal_reason_model_active(name: str):
    """
        toggles the active value for the specified Removal Reason Model

        Args:
            `name` (str): Removal Reason Model Name

        Raises:
            `NotFoundError`: Removal Reason Model with
                specified name not found

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # toggle active value for removal reason model
    try:
        query_data = (
            RemovalReasonModel.update_removal_reason_model_active_toggle(
                name=name)
        )

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_model: RemovalReasonModel.RemovalReasonModel = (
        RemovalReasonModel.query_data_to_obj(query_data=query_data)
    )

    return removal_reason_model


def edit_removal_reason_model(
    name: str, description: str
):
    """
        edits the given values for the specified Removal Reason Model

        Args:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description

        Raises:
            `NotFoundError`: Removal Reason Model with
                specified name not found

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # edit given values for removal reason model
    try:
        query_data = RemovalReasonModel.update_removal_reason_model_edit(
            name=name, description=description
        )

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_model: RemovalReasonModel.RemovalReasonModel = (
        RemovalReasonModel.query_data_to_obj(query_data=query_data)
    )

    return removal_reason_model


def edit_removal_reason_model_name(
    current_name: str, new_name: str
):
    """
        edits the name for a specified Removal Reason Model

        Args:
            `current_name` (str): Removal Reason Model's current name
            `new_name` (str): Removal Reason Model's name to change to

        Raises:
            `NotFoundError`: Removal Reason Model with specified name not found after insert
            `ConflictError`: Removal Reason Model with specified name already exists

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # edit given values for removal reason model
    try:
        query_data = RemovalReasonModel.update_removal_reason_model_edit_name(
            current_name=current_name, new_name=new_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    except ConflictError as arg:
        raise ConflictError(arg)

    removal_reason_model: RemovalReasonModel.RemovalReasonModel = (
        RemovalReasonModel.query_data_to_obj(query_data=query_data)
    )

    return removal_reason_model


def delete_removal_reason_model(name: str):
    """
        toggles the active value for the specified Removal Reason Model

        Args:
            `name` (str): Removal Reason Model Name

        Raises:
            `NotFoundError`: Removal Reason Model not found after deletion

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    # query removal reason model
    try:
        query_data = (
            RemovalReasonModel.delete_removal_reason_model(name=name)
        )

    except NotFoundError as arg:
        raise NotFoundError(arg)

    removal_reason_model: RemovalReasonModel.RemovalReasonModel = (
        RemovalReasonModel.query_data_to_obj(query_data=query_data)
    )

    return removal_reason_model
