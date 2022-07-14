from datetime import datetime
import database.RazBotDB_Presets as preset

from errors.errors_db import (
    NotFoundError,
    ConflictError)

from database.StrikeModel import (
    select_strike_model_from_name,
    query_data_to_obj as strike_model_data_to_obj)

from database.RemovalReasonModel import (
    select_removal_reason_model_from_name)


# Player Strike class

class PlayerStrike(object):
    """
        PlayerStrike
        ----------
        object for db Player Strike table objects

        Instance Attributes
        ----------
        `id` (in): ID of the Player Strike
        `player_tag` (str): clash of clans player tag 
            the strike belongs to
        `strike_name` (str): name of the
            Player Strike's Strike Model
        `strike_description` (str): description of the
            Player Strike's Strike Model
        `strike_weight` (str): weight of the
            Player Strike's Strike Model
        `persistent` (bool): whether or not the
            Player Strike is persistent
            default false
        `date_created` (datetime): date time the strike was created
            default now()
        `date_ended` (datetime): date time the strike will be made inactive
        `removal_reason_name` (str): name of the 
            removal reason's Removal Reason Model
        `removal_reason_description` (str): description of the 
            removal reason's Removal Reason Model
        `striker_user_id` (int): discord user id of striker
    """

    def __init__(
        self, id: int, player_tag: str,
        strike_name: str, strike_description: str,
        strike_weight: str, persistent: bool,
        date_created: datetime, date_ended: datetime,
        removal_reason_name: str, removal_reason_description: str,
        striker_user_id: int
    ):
        self.id = id
        self.player_tag = player_tag
        self.strike_name = strike_name
        self.strike_description = strike_description
        self.strike_weight = strike_weight
        self.persistent = persistent
        self.date_created = date_created
        self.date_ended = date_ended
        self.removal_reason_name = removal_reason_name
        self.removal_reason_description = removal_reason_description
        self.striker_user_id = striker_user_id


def query_data_to_obj(query_data: tuple):
    """
        take in the tuple of the query data
        and return Player Strike class object

        Args
        ----------
        `query_data` (tuple): tuple of Player Strike query
            `id`: int
            `player_tag`: str
            `strike_name`: str
            `strike_description`: str
            `strike_weight`: str
            `persistent`: bool
            `date_created`: datetime
            `date_ended`: datetime
            `removal_reason_name`: str
            `removal_reason_description`: str
            `striker_user_id`: int

        Returns
        ----------
        obj: `PlayerStrike` (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
        )
    """

    (
        id, player_tag, strike_name,
        strike_description, strike_weight,
        persistent, date_created, date_ended,
        removal_reason_name, removal_reason_description,
        striker_user_id
    ) = query_data

    return PlayerStrike(
        id=id,
        player_tag=player_tag,
        strike_name=strike_name,
        strike_description=strike_description,
        strike_weight=strike_weight,
        persistent=bool(persistent),
        date_created=date_created,
        date_ended=date_ended,
        removal_reason_name=removal_reason_name,
        removal_reason_description=removal_reason_description,
        striker_user_id=striker_user_id
    )


# insert

def insert_player_strike(
    player_tag: str,
    strike_name: str,
    striker_user_id: int,
    persistent: bool = None,
    rollover_days: int = None
):
    """
        insert Player Strike

        Args
        ----------
        `player_tag` (str): clash of clans player tag 
            to add the strike to
        `strike_name` (str): name of the
            Player Strike's Strike Model
        `striker_user_id` (int): discord user id of striker
        `persistent` (bool, optional): whether or not the
            Player Strike is persistent
            default None
        `rollover_days` (int, optional): amount of rollover days by default
            defaults None

        Raises:
        ----------
        `ConflictError`: Strike Model with specified name not found
        `NotFoundError`: Player has no active Player Strikes after insert

        Returns:
        ----------
        `active_player_strikes` (list[PlayerStrike]): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
        )
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    strike_name = strike_name.replace("\\'", "'")

    strike_name = strike_name.replace("'", "\\'")

    # check if strike model exists
    try:
        strike_model = select_strike_model_from_name(
            name=strike_name)

    # strike model not found, cannot add strike with no strike model
    except NotFoundError:
        raise ConflictError(
            f"Strike Model with name {strike_name} not found")

    # if persistent is not provided
    # then set it to the strike model default
    if persistent is None:
        persistent = strike_model.persistent

    # if rollover days is not provided
    # then set it to the strike model default
    if rollover_days is None:
        rollover_days = strike_model.rollover_days

    rollover_days = abs(int(rollover_days))

    # set up the query
    query = (
        f"insert into PlayerStrike ( "
        f"strike, "
        f"player_tag, "
        f"persistent, "
        f"date_created, "
        f"date_ended,  "
        f"removal_reason, "
        f"striker_user_id "
        f") "
        f"VALUES ( "
        f"(SELECT id from StrikeModel "
        f"WHERE name = '{strike_name}'), "
        f"'{player_tag}', "
        f"{persistent}, "
        f"now(), "
        f"date_add(now(), INTERVAL {rollover_days} DAY), "
        f"null, "
        f"{striker_user_id} "
        f");")

    # execute update query
    preset.update(query)

    # select and return player strike
    try:
        player_strike = select_player_strike_list_active(player_tag=player_tag)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


# select

def select_player_strike_list_active(player_tag: str):
    """
        selects active Player Strikes

        Args
        ----------
        `player_tag` (str): clash of clans player tag
            to list strikes

        Raises
        ----------
        `NotFoundError`: no Player Strikes for player tag found 

        Returns
        ----------
        `active_player_strikes` (list[PlayerStrike]): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
        )
    """

    # find player strikes based on player tag
    query = (
        f"SELECT PlayerStrike.id as id, "
        f"PlayerStrike.player_tag as player_tag, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"PlayerStrike.persistent as persistent, "
        f"PlayerStrike.date_created as date_created, "
        f"PlayerStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"PlayerStrike.striker_user_id as striker_user_id "
        f"FROM PlayerStrike "
        f"INNER JOIN StrikeModel ON PlayerStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON PlayerStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE PlayerStrike.player_tag = '{player_tag}' "
        f"AND (now() < PlayerStrike.date_ended "
        f"OR PlayerStrike.persistent = True) "
        f"AND PlayerStrike.removal_reason IS NULL;")

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no active Player Strikes for {player_tag} found")

    player_strike_list: list[PlayerStrike] = []

    for data in query_data:
        player_strike_list.append(query_data_to_obj(data))

    return player_strike_list


# only for admin users
def select_player_strike_list_all(player_tag: str):
    """
        selects Player Strikes

        Args
        ----------
        `player_tag` (str): clash of clans player tag
            to list strikes

        Raises
        ----------
        `NotFoundError`: no Player Strikes for player tag found 

        Returns
        ----------
        `active_player_strikes` (list[PlayerStrike]): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
        )
    """

    # find player strikes based on player tag
    query = (
        f"SELECT PlayerStrike.id as id, "
        f"PlayerStrike.player_tag as player_tag, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"PlayerStrike.persistent as persistent, "
        f"PlayerStrike.date_created as date_created, "
        f"PlayerStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"PlayerStrike.striker_user_id as striker_user_id "
        f"FROM PlayerStrike "
        f"INNER JOIN StrikeModel ON PlayerStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON PlayerStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE PlayerStrike.player_tag = '{player_tag}';")

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no Player Strikes for {player_tag} found")

    player_strike_list: list[PlayerStrike] = []

    for data in query_data:
        player_strike_list.append(query_data_to_obj(data))

    return player_strike_list


def select_player_strike(player_tag: str, strike_id: int):
    """
        selects Player Strike from given player tag and strike id

        Args
        ----------
        `player_tag` (str): clash of clans player tag
        `strike_id` (int): id of the Player Strike

        Raises
        ----------
        `NotFoundError`: Player Strike with given player tag and strike id
            not found

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
        )
    """

    # find player strikes based on player tag
    query = (
        f"SELECT PlayerStrike.id as id, "
        f"PlayerStrike.player_tag as player_tag, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"PlayerStrike.persistent as persistent, "
        f"PlayerStrike.date_created as date_created, "
        f"PlayerStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"PlayerStrike.striker_user_id as striker_user_id "
        f"FROM PlayerStrike "
        f"INNER JOIN StrikeModel ON PlayerStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON PlayerStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE PlayerStrike.player_tag = '{player_tag}' "
        f"AND PlayerStrike.id = {strike_id};")

    # execute and return query
    data = preset.select(query)

    if data is None:
        raise NotFoundError(
            f"Player Strike with player tag {player_tag} "
            f"and strike id {strike_id} not found"
        )

    player_strike: PlayerStrike = query_data_to_obj(data)

    return player_strike


# only for admin users
def select_player_strike_from_id(strike_id: int):
    """
        selects Player Strike from given strike id

        Args
        ----------
        `strike_id` (int): id of the Player Strike

        Raises
        ----------
        `NotFoundError`: Player Strike with given strike id
            not found

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
        )
    """

    # find player strikes based on player tag
    query = (
        f"SELECT PlayerStrike.id as id, "
        f"PlayerStrike.player_tag as player_tag, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"PlayerStrike.persistent as persistent, "
        f"PlayerStrike.date_created as date_created, "
        f"PlayerStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"PlayerStrike.striker_user_id as striker_user_id "
        f"FROM PlayerStrike "
        f"INNER JOIN StrikeModel ON PlayerStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON PlayerStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE PlayerStrike.id = {strike_id};")

    # execute and return query
    data = preset.select(query)

    if data is None:
        raise NotFoundError(
            f"Player Strike with strike id {strike_id} not found"
        )

    player_strike: PlayerStrike = query_data_to_obj(data)

    return player_strike


# update

def update_player_strike_toggle_persistent(player_tag: str, strike_id: int):
    """
        toggles the `persistent` value for the specified Player Strike

        Args
        ----------
        `player_tag` (str): clash of clans player tag
        `strike_id` (int): id of the Player Strike

        Raises
        ----------
        `NotFoundError`: Player Strike with given player tag and strike id
            not found

        Returns:
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    # get player strike
    try:
        player_strike = select_player_strike(
            player_tag=player_tag,
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query toggling the persistent status
    query = (
        f"UPDATE PlayerStrike SET persistent = "
        f"{not bool(player_strike.persistent)} "
        f"WHERE player_tag = '{player_tag}' "
        f"AND id = {player_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        player_strike = select_player_strike(
            player_tag=player_tag, strike_id=player_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


# only for super user
def update_player_strike_toggle_persistent_from_id(strike_id: int):
    """
        toggles the `persistent` value for the specified Player Strike

        Args
        ----------
        `strike_id` (int): id of the Player Strike

        Raises
        ----------
        `NotFoundError`: Player Strike with given strike id
            not found

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    # get player strike
    try:
        player_strike = select_player_strike_from_id(
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query toggling the persistent status
    query = (
        f"UPDATE PlayerStrike SET persistent "
        f"= {not bool(player_strike.persistent)} "
        f"WHERE id = {player_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        player_strike = select_player_strike_from_id(
            strike_id=player_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


def update_player_strike_rollover_days(
        player_tag: str, strike_id: int, rollover_days: int):
    """
        edits the `date ended` value for the specified Player Strike

        Args
        ----------
        `player_tag` (str): clash of clans player tag
        `strike_id` (int): id of the Player Strike
        `rollover_days` (int, optional): amount of rollover days

        Raises
        ----------
        `NotFoundError`: Player Strike with given player tag and strike id
            not found

        Returns:
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    rollover_days = abs(int(rollover_days))

    # get player strike
    try:
        player_strike = select_player_strike(
            player_tag=player_tag,
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query updating the date ended value
    query = (
        f"UPDATE PlayerStrike SET date_ended = "
        f"date_add(now(), INTERVAL {rollover_days} DAY) "
        f"WHERE player_tag = '{player_tag}' "
        f"AND id = {player_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        player_strike = select_player_strike(
            player_tag=player_tag, strike_id=player_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


# only for super user
def update_player_strike_rollover_days_from_id(strike_id: int, rollover_days: int):
    """
        edits the `date ended` value for the specified Player Strike

        Args
        ----------
        `strike_id` (int): id of the Player Strike
        `rollover_days` (int, optional): amount of rollover days

        Raises
        ----------
        `NotFoundError`: Player Strike with given strike id
            not found

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    rollover_days = abs(int(rollover_days))

    # get player strike
    try:
        player_strike = select_player_strike_from_id(
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query updating the ended date value
    query = (
        f"UPDATE PlayerStrike SET date_ended = "
        f"date_add(now(), INTERVAL {rollover_days} DAY) "
        f"WHERE id = {player_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        player_strike = select_player_strike_from_id(
            strike_id=player_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


def update_player_strike_add_removal_reason(
    player_tag: str, strike_id: int, removal_reason_name: str
):
    """
        adds a removal reason to the Player Strike

        Args
        ----------
        `player_tag` (str): clash of clans player tag
        `strike_id` (int): id of the Player Strike
        `removal_reason_name` (str): Removal Reason name

        Raises
        ----------
        `NotFoundError`: Player Strike with given player tag and strike id
            not found
        `NotFoundError`: Removal Reason Model with specified name
            not found
        `ConflictError`: Player Strike already has removal reason

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    removal_reason_name = removal_reason_name.replace("\\'", "'")

    removal_reason_name = removal_reason_name.replace("'", "\\'")

    # get player strike
    try:
        player_strike = select_player_strike(
            player_tag=player_tag,
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    try:
        removal_reason = select_removal_reason_model_from_name(
            name=removal_reason_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    if player_strike.removal_reason_name is not None:
        raise ConflictError(
            f"Player Strike id {player_strike.id} already has "
            f"removal reason '{player_strike.removal_reason_name}'")

    # set up the query adding a removal reason the persistent status
    query = (
        f"UPDATE PlayerStrike SET removal_reason = ( "
        f"SELECT id FROM RemovalReasonModel "
        f"WHERE name = '{removal_reason_name}') "
        f"WHERE player_tag = '{player_tag}' "
        f"AND id = {strike_id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        player_strike = select_player_strike(
            player_tag=player_tag, strike_id=player_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


# only for super user
def update_player_strike_add_removal_reason_from_id(
    strike_id: int, removal_reason_name: str
):
    """
        adds a removal reason to the Player Strike

        Args
        ----------
        `strike_id` (int): id of the Player Strike
        `removal_reason_name` (str): Removal Reason name

        Raises
        ----------
        `NotFoundError`: Player Strike with given player tag and strike id
            not found
        `ConflictError`: Player Strike already has removal reason

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    removal_reason_name = removal_reason_name.replace("\\'", "'")

    removal_reason_name = removal_reason_name.replace("'", "\\'")

    # get player strike
    try:
        player_strike = select_player_strike_from_id(
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    try:
        removal_reason = select_removal_reason_model_from_name(
            name=removal_reason_name
        )

    except NotFoundError as arg:
        raise NotFoundError(arg)

    if player_strike.removal_reason_name is not None:
        raise ConflictError(
            f"Player Strike id {player_strike.id} already has "
            f"removal reason '{player_strike.removal_reason_name}'")

    # set up the query adding a removal reason the persistent status
    query = (
        f"UPDATE PlayerStrike SET removal_reason = ( "
        f"SELECT id FROM RemovalReasonModel "
        f"WHERE name = '{removal_reason_name}') "
        f"WHERE id = {player_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        player_strike = select_player_strike_from_id(
            strike_id=player_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return player_strike


# delete

def delete_player_strike(strike_id: int):
    """
        deletes the specified Player Strike

        Args
        ----------
        `strike_id` (int): id of the Player Strike

        Raises
        ----------
        `NotFoundError`: Player Strike not found after deletion
        `ConflictError`: Player Strike with specified id does not exist

        Returns
        ----------
        `player_strike` (PlayerStrike): (
            `id`: int,
            `player_tag`: str,
            `strike_name`: str,
            `strike_description`: str,
            `strike_weight`: str,
            `persistent`: bool,
            `date_created`: datetime,
            `date_ended`: datetime,
            `removal_reason_name`: str,
            `removal_reason_description`: str,
            `striker_user_id`: int
    """

    # check if player strike is created
    try:
        player_strike = select_player_strike_from_id(strike_id=strike_id)

    except NotFoundError:
        raise ConflictError(
            f"Player Strike with id {strike_id} "
            f"not found")

    # set up the query
    query = (
        f"DELETE FROM PlayerStrike WHERE id='{strike_id}'"
    )

    # execute delete query
    preset.delete(query)

    # search player strike and show it was deleted
    try:
        player_strike = select_player_strike_from_id(strike_id=strike_id)

    except NotFoundError:
        raise NotFoundError(
            f"Player Strike with id {strike_id} "
            f"deleted correctly")

    return player_strike
