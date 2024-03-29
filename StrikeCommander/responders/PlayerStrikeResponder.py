from responders.ResponderModel import ResponderModel
from database.PlayerStrike import PlayerStrike
from coc.players import Player
from coc.clans import Clan
import datetime

from errors.errors_db import(
    NotFoundError,
    ConflictError)
from database.PlayerStrike import (
    select_player_strike,
    select_player_strike_list_active,
    select_player_strike_list_all,
    insert_player_strike,
    update_player_strike_toggle_persistent,
    update_player_strike_rollover_days,
    update_player_strike_add_removal_reason,
    delete_player_strike)


# read

def find_player_strike(player_tag: str, strike_id: int):
    """
        returns Player Strike
    """

    try:
        player_strike: PlayerStrike = (
            select_player_strike(
                player_tag=player_tag, strike_id=strike_id))

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


def find_player_strike_active(player_tag: str):
    """
        returns active Player Strike list
    """

    try:
        player_strike_list: list[PlayerStrike] = (
            select_player_strike_list_active(player_tag=player_tag))

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike_list


def find_player_strike_all(player_tag: str):
    """
        returns Player Strike list
    """

    try:
        player_strike_list: list[PlayerStrike] = (
            select_player_strike_list_all(player_tag=player_tag))

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike_list


def get_player_strike(
        player: Player,
        user_string: str,
        player_strike: PlayerStrike):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"{player.name} {player.tag} Player Strike"

    # set description
    responder.description = (
        f"Linked User: {user_string}")

    # player strike ending string
    # player strike active string

    # player strike inactive
    # player strike has been removed
    if player_strike.removal_reason_name is not None:
        active_string = f"Inactive\n"
        ending_string = (
            f"Removal Reason: {player_strike.removal_reason_name}\n"
            f"Removal Description: {player_strike.removal_reason_description}")

    # player strike active
    # player strike is marked as persistent
    elif player_strike.persistent:
        active_string = f"Active\n"
        ending_string = f"Persistent: {player_strike.persistent}"

    # player strike inactive
    # current date is after player strike end date
    elif datetime.datetime.now() > player_strike.date_ended:
        active_string = f"Inactive\n"
        ending_string = (
            f"End Date: "
            f"{player_strike.date_ended.strftime('%d %b %Y')}")

    # player strike active
    else:
        time_diff = player_strike.date_ended-datetime.datetime.now()

        active_string = f"Active\n"
        ending_string = (
            f"End Date: "
            f"{player_strike.date_ended.strftime('%d %b %Y')}\n"
            f"Rollover Days: {time_diff.days}")

    responder.field_dict_list.append({
        'name': player_strike.strike_name,
        'value': (
            f"{active_string}"
            f"Player Strike ID: {player_strike.id}\n"
            f"Description: {player_strike.strike_description}\n"
            f"Strikes: **{player_strike.strike_weight}**\n"
            f"Create Date: "
            f"{player_strike.date_created.strftime('%d %b %Y')}\n"
            f"{ending_string}"),
        'inline': False})

    if player_strike.strike_weight >= 6:
        responder.content = (
            f"**"
            f"{user_string}: {player.name} {player.tag} has accumulated "
            f"{player_strike.strike_weight} strikes, "
            f"contact leadership to resolve strikes"
            f"**")

    return responder


def get_player_strike_overview(
        player: Player,
        user_string: str,
        player_strike_list: list[PlayerStrike]):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"{player.name} {player.tag} Active Player Strikes"

    strike_weight_sum = sum(
        player_strike.strike_weight for player_strike in player_strike_list)

    # set description
    responder.description = (
        f"Linked User: {user_string}\n"
        f"Active Player Violations: **{len(player_strike_list)}**\n"
        f"Active Player Strikes: **{strike_weight_sum}**")

    if strike_weight_sum >= 6:
        responder.content = (
            f"**"
            f"{user_string}: {player.name} {player.tag} has accumulated "
            f"{strike_weight_sum} strikes, "
            f"contact leadership to resolve strikes"
            f"**")

    return responder


def get_player_strike_active(
        player: Player,
        user_string: str,
        player_strike_list: list[PlayerStrike]):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"{player.name} {player.tag} Active Player Strikes"

    strike_weight_sum = sum(
        player_strike.strike_weight for player_strike in player_strike_list)

    # set description
    responder.description = (
        f"Linked User: {user_string}\n"
        f"Active Player Violations: **{len(player_strike_list)}**\n"
        f"Active Player Strikes: **{strike_weight_sum}**")

    if strike_weight_sum >= 6:
        responder.content = (
            f"**"
            f"{user_string}: {player.name} {player.tag} has accumulated "
            f"{strike_weight_sum} strikes, "
            f"contact leadership to resolve strikes"
            f"**")

    for player_strike in player_strike_list:

        # player strike ending string
        # player strike active string

        # player strike inactive
        # player strike has been removed
        if player_strike.removal_reason_name is not None:
            active_string = f"Inactive\n"
            ending_string = (
                f"Removal Reason: {player_strike.removal_reason_name}\n"
                f"Removal Description: {player_strike.removal_reason_description}")

        # player strike active
        # player strike is marked as persistent
        elif player_strike.persistent:
            active_string = f"Active\n"
            ending_string = f"Persistent: {player_strike.persistent}"

        # player strike inactive
        # current date is after player strike end date
        elif datetime.datetime.now() > player_strike.date_ended:
            active_string = f"Inactive\n"
            ending_string = (
                f"End Date: "
                f"{player_strike.date_ended.strftime('%d %b %Y')}")

        # player strike active
        else:
            time_diff = player_strike.date_ended-datetime.datetime.now()

            active_string = f"Active\n"
            ending_string = (
                f"End Date: "
                f"{player_strike.date_ended.strftime('%d %b %Y')}\n"
                f"Rollover Days: {time_diff.days}")

        responder.field_dict_list.append({
            'name': player_strike.strike_name,
            'value': (
                f"{active_string}"
                f"Player Strike ID: {player_strike.id}\n"
                f"Description: {player_strike.strike_description}\n"
                f"Strikes: **{player_strike.strike_weight}**\n"
                f"Create Date: "
                f"{player_strike.date_created.strftime('%d %b %Y')}\n"
                f"{ending_string}"),
            'inline': False})

    return responder


def get_player_strike_all(
        player: Player,
        user_string: str,
        player_strike_list: list[PlayerStrike]):
    """
        returns ResponderModel
    """

    responder = ResponderModel()

    # set title
    responder.title = f"{player.name} {player.tag} Player Strikes"

    strike_weight_sum = sum(
        player_strike.strike_weight for player_strike in player_strike_list)

    active_strike_count = 0
    active_strike_weight = 0

    for player_strike in player_strike_list:

        # player strike ending string
        # player strike active string

        # player strike inactive
        # player strike has been removed
        if player_strike.removal_reason_name is not None:
            active_string = f"Inactive\n"

            ending_string = (
                f"Removal Reason: {player_strike.removal_reason_name}\n"
                f"Removal Description: {player_strike.removal_reason_description}")

        # player strike active
        # player strike is marked as persistent
        elif player_strike.persistent:
            active_strike_count = active_strike_count + 1
            active_strike_weight = (
                active_strike_weight + player_strike.strike_weight)

            active_string = f"Active\n"

            ending_string = f"Persistent: {player_strike.persistent}"

        # player strike inactive
        # current date is after player strike end date
        elif datetime.datetime.now() > player_strike.date_ended:

            active_string = f"Inactive\n"

            ending_string = (
                f"End Date: "
                f"{player_strike.date_ended.strftime('%d %b %Y')}")

        # player strike active
        else:
            time_diff = player_strike.date_ended-datetime.datetime.now()

            active_strike_count = active_strike_count + 1
            active_strike_weight = (
                active_strike_weight + player_strike.strike_weight)

            active_string = f"Active\n"

            ending_string = (
                f"End Date: "
                f"{player_strike.date_ended.strftime('%d %b %Y')}\n"
                f"Rollover Days: {time_diff.days}")

        responder.field_dict_list.append({
            'name': player_strike.strike_name,
            'value': (
                f"{active_string}"
                f"Player Strike ID: {player_strike.id}\n"
                f"Description: {player_strike.strike_description}\n"
                f"Strikes: **{player_strike.strike_weight}**\n"
                f"Create Date: "
                f"{player_strike.date_created.strftime('%d %b %Y')}\n"
                f"{ending_string}"),
            'inline': False})

    # set description
    responder.description = (
        f"Linked User: {user_string}\n"
        f"Active Player Violations: **{active_strike_count}**\n"
        f"Active Player Strikes: **{active_strike_weight}**\n"
        f"Player Violations: **{len(player_strike_list)}**\n"
        f"Player Strikes: **{strike_weight_sum}**")

    if active_strike_weight >= 6:
        responder.content = (
            f"**"
            f"{user_string}: {player.name} {player.tag} has accumulated "
            f"{strike_weight_sum} active strikes, "
            f"contact leadership to resolve strikes"
            f"**")

    return responder


# create

def add_player_strike(
        player: Player,
        user_string: str,
        strike_name: str,
        persistent: bool,
        rollover_days: int,
        striker_user_id: int):
    """
        returns ResponderModel
    """

    try:
        player_strike_list: list[PlayerStrike] = insert_player_strike(
            player_tag=player.tag,
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
            title=f"{player.name} {player.tag} Active Player Strikes",
            description=(
                f"Linked User: {user_string}\n"
                f"Active Player Violations: **0**"))

    responder = get_player_strike_overview(
        player=player,
        user_string=user_string,
        player_strike_list=player_strike_list)

    if responder.content is None:
        responder.content = f"{user_string}"

    return responder


# edit

def edit_player_strike_toggle_persistent(
        player: Player,
        strike_id: int,
        user_string: str):
    """
        returns ResponderModel
    """

    try:
        player_strike: PlayerStrike = (
            update_player_strike_toggle_persistent(
                player_tag=player.tag,
                strike_id=strike_id))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"{player.name} {player.tag} Player Strike",
            description=(
                f"Player Strike with given player tag and "
                f"Player Strike ID not found"))

    responder = get_player_strike(
        player=player,
        user_string=user_string,
        player_strike=player_strike)

    if responder.content is None:
        responder.content = f"{user_string}"

    return responder


def edit_player_strike_rollover_days(
        player: Player,
        strike_id: int,
        user_string: str,
        rollover_days: int):
    """
        returns ResponderModel
    """

    try:
        player_strike: PlayerStrike = (
            update_player_strike_rollover_days(
                player_tag=player.tag,
                strike_id=strike_id,
                rollover_days=rollover_days))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"{player.name} {player.tag} Player Strike",
            description=(
                f"Player Strike with given player tag and "
                f"Player Strike ID not found"))

    responder = get_player_strike(
        player=player,
        user_string=user_string,
        player_strike=player_strike)

    if responder.content is None:
        responder.content = f"{user_string}"

    return responder


# remove

def remove_player_strike(
        player: Player,
        strike_id: int,
        removal_reason_name: str,
        user_string: str):
    """
        returns ResponderModel
    """

    try:
        player_strike: PlayerStrike = (
            update_player_strike_add_removal_reason(
                player_tag=player.tag,
                strike_id=strike_id,
                removal_reason_name=removal_reason_name))

    except ConflictError as arg:
        return ResponderModel(
            title=f"Player Strike already removed",
            description=(
                f"Player Strike with ID '{strike_id}' already removed"))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"Unable to remove Player Strike",
            description=(
                f"Player Strike with player tag {player.tag} "
                f"or Removal Reason with name {removal_reason_name} "
                f"not found"))

    responder = get_player_strike(
        player=player,
        user_string=user_string,
        player_strike=player_strike)

    if responder.content is None:
        responder.content = f"{user_string}"

    return responder


def delete_player_strike_from_id(strike_id: int):
    """
        returns ResponderModel
    """

    try:
        player_strike: PlayerStrike = delete_player_strike(
            strike_id=strike_id)

    except ConflictError as arg:
        return ResponderModel(
            title=f"Player Strike Not Found",
            description=(
                f"Player Strike with ID '{strike_id}' not found"))

    except NotFoundError as arg:
        return ResponderModel(
            title=f"Player Strike Deleted",
            description=(
                f"Player Strike with ID {strike_id} "
                f"deleted"))

    return ResponderModel(
        title=f"Player Strike Not Deleted",
        description=(
            f"Player Strike with ID {strike_id} "
            f"not deleted"))
