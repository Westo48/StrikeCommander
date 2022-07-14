from disnake import (
    ApplicationCommandInteraction,
    User)
from responders.ResponderModel import ResponderModel
from database.UserStrike import UserStrike
from database.PlayerStrike import PlayerStrike
from coc.players import Player
import datetime

from responders.DiscordResponder import (
    embed_message,
    get_town_hall_url)
from responders.RazBotDB_Responder import (
    read_player_list)
from responders.ClashResponder import (
    get_player)
from responders.PlayerStrikeResponder import (
    find_player_strike_active,
    find_player_strike_all,
    get_player_strike_overview,
    get_player_strike_active,
    get_player_strike_all)
from errors.errors_db import(
    NotFoundError,
    ConflictError)
from database.UserStrike import (
    select_user_strike,
    select_user_strike_list_active,
    select_user_strike_list_all,
    insert_user_strike,
    update_user_strike_toggle_persistent,
    update_user_strike_rollover_days,
    update_user_strike_add_removal_reason,
    delete_user_strike)


# read

def find_user_strike(user_id: int, strike_id: int):
    """
        returns User Strike
    """

    try:
        user_strike: UserStrike = (
            select_user_strike(
                user_id=user_id, strike_id=strike_id))

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike


def find_user_strike_active(user_id: int):
    """
        returns active User Strike list
    """

    try:
        user_strike_list: list[UserStrike] = (
            select_user_strike_list_active(user_id=user_id))

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike_list


def find_user_strike_all(user_id: int):
    """
        returns User Strike list
    """

    try:
        user_strike_list: list[UserStrike] = (
            select_user_strike_list_all(user_id=user_id))

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike_list


def get_user_summary_active(
        user: User,
        user_strike_list: list[UserStrike],
        player_strike_list: list[PlayerStrike],
        player_count: int):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    responder.title = f"Active Strikes"

    strike_list = []
    strike_list.extend(user_strike_list)
    strike_list.extend(player_strike_list)

    if len(strike_list) == 0:
        strike_weight_sum = 0

    else:
        strike_weight_sum = sum(
            strike.strike_weight for strike in strike_list)

    strike_count = len(strike_list)

    responder.description = (
        f"User: {user.mention}\n"
        f"Player Count: {player_count}\n"
        f"Active Strike Count: **{strike_count}**\n"
        f"Active Strike Weight: **{strike_weight_sum}**")

    if strike_weight_sum >= 5:
        responder.content = (
            f"**"
            f"{user.mention} has accumulated a Strike Weight of "
            f"{strike_weight_sum}, contact leadership to resolve strikes"
            f"**")

    return responder


def get_user_summary_all(
        user: User,
        user_strike_list: list[UserStrike],
        player_strike_list: list[PlayerStrike],
        player_count: int):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    responder.title = f"Strikes"

    strike_list = []
    strike_list.extend(user_strike_list)
    strike_list.extend(player_strike_list)

    if len(strike_list) == 0:
        strike_weight_sum = 0

    else:
        strike_weight_sum = sum(
            strike.strike_weight for strike in strike_list)

    strike_count = len(strike_list)

    active_strike_count = 0
    active_strike_weight = 0
    field_dict_list = []

    for strike in strike_list:

        # user strike ending string
        # user strike active string

        # user strike inactive
        # user strike has been removed
        if strike.removal_reason_name is not None:
            continue

        # user strike active
        # user strike is marked as persistent
        elif strike.persistent:
            active_strike_count = active_strike_count + 1

            active_strike_weight = (
                active_strike_weight + strike.strike_weight)

            continue

        # user strike inactive
        # current date is after user strike end date
        elif datetime.datetime.now() > strike.date_ended:
            continue

        # user strike active
        else:
            active_strike_count = active_strike_count + 1

            active_strike_weight = (
                active_strike_weight + strike.strike_weight)

            continue

    responder.description = (
        f"User: {user.mention}\n"
        f"Player Count: {player_count}\n"
        f"Active Strike Count: **{active_strike_count}**\n"
        f"Active Strike Weight: **{active_strike_weight}**\n"
        f"Strike Count: **{strike_count}**\n"
        f"Strike Weight: **{strike_weight_sum}**")

    if active_strike_weight >= 5:
        responder.content = (
            f"**"
            f"{user.mention} has accumulated a Strike Weight of "
            f"{active_strike_weight}, contact leadership to resolve strikes"
            f"**")

    return responder


async def get_user_strike_message_overview(
        user: User,
        inter: ApplicationCommandInteraction,
        coc_client):
    """
        returns ResponderModel
    """

    embed_list = []
    user_strike_list = []
    total_player_strike_list: list[PlayerStrike] = []

    try:
        user_strike_list = (find_user_strike_active(
            user_id=user.id))

        response = get_user_strike_overview(
            user_string=user.mention,
            user_strike_list=user_strike_list)

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author))

    except NotFoundError as arg:
        response = ResponderModel(
            title=f"Active User Strikes",
            description=(
                f"User: {user.mention}\n"
                f"Active User Strike Count: **0**"))

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author))

    db_player_list = read_player_list(
        discord_user_id=user.id)

    for db_player in db_player_list:
        player: Player = await get_player(
            db_player.player_tag, coc_client)

        if player is None:
            embed_description = (
                f"could not find player with tag "
                f"{db_player.player_tag}")

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author))

            continue

        embed_thumbnail = get_town_hall_url(player)

        try:
            player_strike_list = (find_player_strike_active(
                player_tag=player.tag))

        except NotFoundError as arg:
            response = ResponderModel(
                title=f"{player.name} {player.tag} Active Player Strikes",
                description=(
                    f"Linked User: {user.mention}\n"
                    f"Active Player Strike Count: **0**"))

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=response.title,
                description=response.description,
                bot_user_name=inter.me.display_name,
                thumbnail=embed_thumbnail,
                field_list=response.field_dict_list,
                author=inter.author))

            continue

        response = get_player_strike_overview(
            player=player,
            user_string=user.mention,
            player_strike_list=player_strike_list)

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=response.field_dict_list,
            author=inter.author))

        total_player_strike_list.extend(
            player_strike_list)

    response = get_user_summary_active(
        user=user,
        user_strike_list=user_strike_list,
        player_strike_list=total_player_strike_list,
        player_count=len(db_player_list))

    user_summary_embed = embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=response.title,
        description=response.description,
        bot_user_name=inter.me.display_name,
        field_list=response.field_dict_list,
        author=inter.author)

    return_embed_list = []

    return_embed_list.extend(user_summary_embed)
    return_embed_list.extend(embed_list)

    return_response = ResponderModel(
        content=response.content,
        embed_list=return_embed_list)

    return return_response


async def get_user_strike_message_active(
        user: User,
        inter: ApplicationCommandInteraction,
        coc_client):
    """
        returns ResponderModel
    """

    embed_list = []
    user_strike_list = []
    total_player_strike_list: list[PlayerStrike] = []

    try:
        user_strike_list = (find_user_strike_active(
            user_id=user.id))

        response = get_user_strike_active(
            user_string=user.mention,
            user_strike_list=user_strike_list)

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author))

    except NotFoundError as arg:
        response = ResponderModel(
            title=f"Active User Strikes",
            description=(
                f"User: {user.mention}\n"
                f"Active User Strike Count: **0**"))

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author))

    db_player_list = read_player_list(
        discord_user_id=user.id)

    for db_player in db_player_list:
        player: Player = await get_player(
            db_player.player_tag, coc_client)

        if player is None:
            embed_description = (
                f"could not find player with tag "
                f"{db_player.player_tag}")

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author))

            continue

        embed_thumbnail = get_town_hall_url(player)

        try:
            player_strike_list = (find_player_strike_active(
                player_tag=player.tag))

        except NotFoundError as arg:
            response = ResponderModel(
                title=f"{player.name} {player.tag} Active Player Strikes",
                description=(
                    f"Linked User: {user.mention}\n"
                    f"Active Player Strike Count: **0**"))

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=response.title,
                description=response.description,
                bot_user_name=inter.me.display_name,
                thumbnail=embed_thumbnail,
                field_list=response.field_dict_list,
                author=inter.author))

            continue

        response = get_player_strike_active(
            player=player,
            user_string=user.mention,
            player_strike_list=player_strike_list)

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=response.field_dict_list,
            author=inter.author))

        total_player_strike_list.extend(
            player_strike_list)

    response = get_user_summary_active(
        user=user,
        user_strike_list=user_strike_list,
        player_strike_list=total_player_strike_list,
        player_count=len(db_player_list))

    user_summary_embed = embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=response.title,
        description=response.description,
        bot_user_name=inter.me.display_name,
        field_list=response.field_dict_list,
        author=inter.author)

    return_embed_list = []

    return_embed_list.extend(user_summary_embed)
    return_embed_list.extend(embed_list)

    return_response = ResponderModel(
        content=response.content,
        embed_list=return_embed_list)

    return return_response


async def get_user_strike_message_all(
        user: User,
        inter: ApplicationCommandInteraction,
        coc_client):
    """
        returns ResponderModel
    """

    embed_list = []
    user_strike_list = []
    total_player_strike_list: list[PlayerStrike] = []

    try:
        user_strike_list = (find_user_strike_all(
            user_id=user.id))

        response = get_user_strike_all(
            user_string=user.mention,
            user_strike_list=user_strike_list)

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author))

    except NotFoundError as arg:
        response = ResponderModel(
            title=f"Active User Strikes",
            description=(
                f"User: {user.mention}\n"
                f"Active User Strike Count: **0**"))

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            field_list=response.field_dict_list,
            author=inter.author))

    db_player_list = read_player_list(
        discord_user_id=user.id)

    for db_player in db_player_list:
        player: Player = await get_player(
            db_player.player_tag, coc_client)

        if player is None:
            embed_description = (
                f"could not find player with tag "
                f"{db_player.player_tag}")

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                bot_user_name=inter.me.display_name,
                description=embed_description,
                author=inter.author))

            continue

        embed_thumbnail = get_town_hall_url(player)

        try:
            player_strike_list = (find_player_strike_all(
                player_tag=player.tag))

        except NotFoundError as arg:
            response = ResponderModel(
                title=f"{player.name} {player.tag} Active Player Strikes",
                description=(
                    f"Linked User: {user.mention}\n"
                    f"Active Player Strike Count: **0**"))

            embed_list.extend(embed_message(
                icon_url=inter.bot.user.avatar.url,
                title=response.title,
                description=response.description,
                bot_user_name=inter.me.display_name,
                thumbnail=embed_thumbnail,
                field_list=response.field_dict_list,
                author=inter.author))

            continue

        response = get_player_strike_all(
            player=player,
            user_string=user.mention,
            player_strike_list=player_strike_list)

        embed_list.extend(embed_message(
            icon_url=inter.bot.user.avatar.url,
            title=response.title,
            description=response.description,
            bot_user_name=inter.me.display_name,
            thumbnail=embed_thumbnail,
            field_list=response.field_dict_list,
            author=inter.author))

        total_player_strike_list.extend(
            player_strike_list)

    response = get_user_summary_all(
        user=user,
        user_strike_list=user_strike_list,
        player_strike_list=total_player_strike_list,
        player_count=len(db_player_list))

    user_summary_embed = embed_message(
        icon_url=inter.bot.user.avatar.url,
        title=response.title,
        description=response.description,
        bot_user_name=inter.me.display_name,
        field_list=response.field_dict_list,
        author=inter.author)

    return_embed_list = []

    return_embed_list.extend(user_summary_embed)
    return_embed_list.extend(embed_list)

    return_response = ResponderModel(
        content=response.content,
        embed_list=return_embed_list)

    return return_response


def get_user_strike(
        user_string: str,
        user_strike: UserStrike):
    """
        returns ResponderModel
    """

    # set title
    title = f"User Strike"

    description = f"User: {user_string}"

    field_dict_list = []

    # user strike ending string
    # user strike active string

    # user strike inactive
    # user strike has been removed
    if user_strike.removal_reason_name is not None:
        active_string = f"Inactive\n"
        ending_string = (
            f"Removal Reason: {user_strike.removal_reason_name}\n"
            f"Removal Description: {user_strike.removal_reason_description}")

    # user strike active
    # user strike is marked as persistent
    elif user_strike.persistent:
        active_string = f"Active\n"
        ending_string = f"Persistent: {user_strike.persistent}"

    # user strike inactive
    # current date is after user strike end date
    elif datetime.datetime.now() > user_strike.date_ended:
        active_string = f"Inactive\n"
        ending_string = (
            f"End Date: "
            f"{user_strike.date_ended.strftime('%d %b %Y')}")

    # user strike active
    else:
        time_diff = user_strike.date_ended-datetime.datetime.now()

        active_string = f"Active\n"
        ending_string = (
            f"End Date: "
            f"{user_strike.date_ended.strftime('%d %b %Y')}\n"
            f"Rollover Days: {time_diff.days}")

    field_dict_list.append({
        'name': user_strike.strike_name,
        'value': (
            f"{active_string}"
            f"User Strike ID: {user_strike.id}\n"
            f"Description: {user_strike.strike_description}\n"
            f"Strike Weight: **{user_strike.strike_weight}**\n"
            f"Create Date: "
            f"{user_strike.date_created.strftime('%d %b %Y')}\n"
            f"{ending_string}"),
        'inline': False})

    return ResponderModel(
        title=title, description=description,
        field_dict_list=field_dict_list)


def get_user_strike_overview(
        user_string: str,
        user_strike_list: list[UserStrike]):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"Active User Strikes"

    strike_weight_sum = sum(
        user_strike.strike_weight for user_strike in user_strike_list)

    # set description
    responder.description = (
        f"User: {user_string}\n"
        f"Active User Strike Count: **{len(user_strike_list)}**\n"
        f"Active User Strike Weight: **{strike_weight_sum}**")

    if strike_weight_sum >= 5:
        responder.content = (
            f"**"
            f"{user_string} has accumulated a Strike Weight of "
            f"{strike_weight_sum}, contact leadership to resolve strikes"
            f"**")

    return responder


def get_user_strike_active(
        user_string: str,
        user_strike_list: list[UserStrike]):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"Active User Strikes"

    strike_weight_sum = sum(
        user_strike.strike_weight for user_strike in user_strike_list)

    # set description
    responder.description = (
        f"User: {user_string}\n"
        f"Active User Strike Count: **{len(user_strike_list)}**\n"
        f"Active User Strike Weight: **{strike_weight_sum}**")

    if strike_weight_sum >= 5:
        responder.content = (
            f"**"
            f"{user_string} has accumulated a Strike Weight of "
            f"{strike_weight_sum}, contact leadership to resolve strikes"
            f"**")

    for user_strike in user_strike_list:

        # user strike ending string
        # user strike active string

        # user strike inactive
        # user strike has been removed
        if user_strike.removal_reason_name is not None:
            active_string = f"Inactive\n"
            ending_string = (
                f"Removal Reason: {user_strike.removal_reason_name}\n"
                f"Removal Description: {user_strike.removal_reason_description}")

        # user strike active
        # user strike is marked as persistent
        elif user_strike.persistent:
            active_string = f"Active\n"
            ending_string = f"Persistent: {user_strike.persistent}"

        # user strike inactive
        # current date is after user strike end date
        elif datetime.datetime.now() > user_strike.date_ended:
            active_string = f"Inactive\n"
            ending_string = (
                f"End Date: "
                f"{user_strike.date_ended.strftime('%d %b %Y')}")

        # user strike active
        else:
            time_diff = user_strike.date_ended-datetime.datetime.now()

            active_string = f"Active\n"
            ending_string = (
                f"End Date: "
                f"{user_strike.date_ended.strftime('%d %b %Y')}\n"
                f"Rollover Days: {time_diff.days}")

        responder.field_dict_list.append({
            'name': user_strike.strike_name,
            'value': (
                f"{active_string}"
                f"User Strike ID: {user_strike.id}\n"
                f"Description: {user_strike.strike_description}\n"
                f"Strike Weight: **{user_strike.strike_weight}**\n"
                f"Create Date: "
                f"{user_strike.date_created.strftime('%d %b %Y')}\n"
                f"{ending_string}"),
            'inline': False})

    return responder


def get_user_strike_all(
        user_string: str,
        user_strike_list: list[UserStrike]):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"User Strikes"

    strike_weight_sum = sum(
        user_strike.strike_weight for user_strike in user_strike_list)

    # set description
    responder.description = (
        f"User: {user_string}\n"
        f"User Strike Count: **{len(user_strike_list)}**\n"
        f"User Strike Weight: **{strike_weight_sum}**\n")

    active_strike_count = 0
    active_strike_weight = 0

    for user_strike in user_strike_list:

        # user strike ending string
        # user strike active string

        # user strike inactive
        # user strike has been removed
        if user_strike.removal_reason_name is not None:
            active_string = f"Inactive\n"

            ending_string = (
                f"Removal Reason: {user_strike.removal_reason_name}\n"
                f"Removal Description: {user_strike.removal_reason_description}")

        # user strike active
        # user strike is marked as persistent
        elif user_strike.persistent:
            active_strike_count = active_strike_count + 1
            active_strike_weight = (
                active_strike_weight + user_strike.strike_weight)

            active_string = f"Active\n"

            ending_string = f"Persistent: {user_strike.persistent}"

        # user strike inactive
        # current date is after user strike end date
        elif datetime.datetime.now() > user_strike.date_ended:

            active_string = f"Inactive\n"

            ending_string = (
                f"End Date: "
                f"{user_strike.date_ended.strftime('%d %b %Y')}")

        # user strike active
        else:
            time_diff = user_strike.date_ended-datetime.datetime.now()

            active_strike_count = active_strike_count + 1
            active_strike_weight = (
                active_strike_weight + user_strike.strike_weight)

            active_string = f"Active\n"

            ending_string = (
                f"End Date: "
                f"{user_strike.date_ended.strftime('%d %b %Y')}\n"
                f"Rollover Days: {time_diff.days}")

        responder.field_dict_list.append({
            'name': user_strike.strike_name,
            'value': (
                f"{active_string}"
                f"User Strike ID: {user_strike.id}\n"
                f"Description: {user_strike.strike_description}\n"
                f"Strike Weight: **{user_strike.strike_weight}**\n"
                f"Create Date: "
                f"{user_strike.date_created.strftime('%d %b %Y')}\n"
                f"{ending_string}"),
            'inline': False})

    responder.description += (
        f"Active User Strike Count: **{active_strike_count}**\n"
        f"Active User Strike Weight: **{active_strike_weight}**")

    if active_strike_weight >= 5:
        responder.content = (
            f"**"
            f"{user_string} has accumulated a Strike Weight of "
            f"{active_strike_weight}, contact leadership to resolve strikes"
            f"**")

    return responder


# create

def add_user_strike(
        user: User,
        strike_name: str,
        persistent: bool,
        rollover_days: int,
        striker_user_id: int):
    """
        returns ResponderModel
    """

    try:
        user_strike_list: list[UserStrike] = insert_user_strike(
            user_id=user.id,
            strike_name=strike_name,
            persistent=persistent,
            rollover_days=rollover_days,
            striker_user_id=striker_user_id)

    except ConflictError as arg:
        return ResponderModel(
            title=f"Strike Model not found",
            description=(
                f"Strike Model with name '{strike_name}' not found"))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"Active User Strikes",
            description=(
                f"User: {user.mention}"
                f"Active User Strike Count: **0**"))

    responder = get_user_strike_overview(
        user_string=user.mention,
        user_strike_list=user_strike_list)

    # user ping has not been created
    if responder.content is None:
        responder.content = f"{user.mention}"

    return responder


# edit

def edit_user_strike_toggle_persistent(
        user: User,
        strike_id: int):
    """
        returns ResponderModel
    """

    try:
        user_strike: UserStrike = (
            update_user_strike_toggle_persistent(
                user_id=user.id,
                strike_id=strike_id))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"User Strike",
            description=(
                f"User: {user.mention}"
                f"User Strike with given user and "
                f"User Strike ID not found"))

    responder = get_user_strike(
        user_string=user.mention,
        user_strike=user_strike)

    # user ping has not been created
    if responder.content is None:
        responder.content = f"{user.mention}"

    return responder


def edit_user_strike_rollover_days(
        user: User,
        strike_id: int,
        rollover_days: int):
    """
        returns ResponderModel
    """

    try:
        user_strike: UserStrike = (
            update_user_strike_rollover_days(
                user_id=user.id,
                strike_id=strike_id,
                rollover_days=rollover_days))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"User Strike",
            description=(
                f"User: {user.mention}"
                f"User Strike with given user and "
                f"User Strike ID not found"))

    responder = get_user_strike(
        user_string=user.mention,
        user_strike=user_strike)

    # user ping has not been created
    if responder.content is None:
        responder.content = f"{user.mention}"

    return responder


# remove

def remove_user_strike(
        user: User,
        strike_id: int,
        removal_reason_name: str):
    """
        returns ResponderModel
    """

    try:
        user_strike: UserStrike = (
            update_user_strike_add_removal_reason(
                user_id=user.id,
                strike_id=strike_id,
                removal_reason_name=removal_reason_name))

    except ConflictError as arg:
        return ResponderModel(
            title=f"User Strike already removed",
            description=(
                f"User Strike with ID '{strike_id}' already removed"))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"Unable to remove User Strike",
            description=(
                f"User Strike with user {user.mention} "
                f"or Removal Reason with name {removal_reason_name} "
                f"not found"))

    responder = get_user_strike(
        user_string=user.mention,
        user_strike=user_strike)

    # user ping has not been created
    if responder.content is None:
        responder.content = f"{user.mention}"

    return responder


def delete_user_strike_from_id(strike_id: int):
    """
        returns ResponderModel
    """

    try:
        user_strike: UserStrike = delete_user_strike(
            strike_id=strike_id)

    except ConflictError as arg:
        return ResponderModel(
            title=f"User Strike Not Found",
            description=(
                f"User Strike with ID '{strike_id}' not found"))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"User Strike Deleted",
            description=(
                f"User Strike with ID {strike_id} "
                f"deleted"))

    return ResponderModel(
        title=f"User Strike Not Deleted",
        description=(
            f"User Strike with ID {strike_id} "
            f"not deleted"))
