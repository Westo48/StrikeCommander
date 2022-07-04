from datetime import datetime
import database.RazBotDB_Presets as preset

from errors.errors_db import (
    NotFoundError,
    ConflictError)

from database.StrikeModel import (
    select_strike_model_from_name)

from database.RemovalReasonModel import (
    select_removal_reason_model_from_name)


# User Strike class

class UserStrike(object):
    """
        UserStrike: object for db User Strike table objects

            Instance Attributes
                `id` (in): ID of the User Strike
                `user_id` (int): discord user id of the user 
                    the strike belongs to
                `strike_name` (str): name of the
                    User Strike's Strike Model
                `strike_description` (str): description of the
                    User Strike's Strike Model
                `strike_weight` (str): weight of the
                    User Strike's Strike Model
                `persistent` (bool): whether or not the
                    User Strike is persistent
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
        self, id: int, user_id: int,
        strike_name: str, strike_description: str,
        strike_weight: str, persistent: bool,
        date_created: datetime, date_ended: datetime,
        removal_reason_name: str, removal_reason_description: str,
        striker_user_id: int
    ):
        self.id = id
        self.user_id = user_id
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
        and return User Strike class object

        Args:
            `query_data` (tuple): tuple of User Strike query
                `id`: int
                `user_id`: int
                `strike_name`: str
                `strike_description`: str
                `strike_weight`: str
                `persistent`: bool
                `date_created`: datetime
                `date_ended`: datetime
                `removal_reason_name`: str
                `removal_reason_description`: str
                `striker_user_id`: int

        Returns:
            obj: `UserStrike` (
                `id`: int,
                `user_id`: int,
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
        id, user_id, strike_name,
        strike_description, strike_weight,
        persistent, date_created, date_ended,
        removal_reason_name, removal_reason_description,
        striker_user_id
    ) = query_data

    return UserStrike(
        id=id,
        user_id=user_id,
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

def insert_user_strike(
    strike_name: str,
    user_id: int,
    striker_user_id: int,
    persistent: bool = None,
    rollover_days: int = None
):
    """
        insert User Strike

        Args:
            `strike_name` (str): name of the
                User Strike's Strike Model
            `user_id` (int): discord user id of the user 
                to add the strike to
            `striker_user_id` (int): discord user id of striker
            `persistent` (bool, optional): whether or not the
                User Strike is persistent
                default None
            `rollover_days` (int, optional): amount of rollover days by default
                defaults None

        Raises:
            `ConflictError`: Strike Model with specified name not found
            `NotFoundError`: User has no active User Strikes after insert

        Returns: `active_user_strikes` (list[UserStrike]): (
            `id`: int,
            `user_id`: int,
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
        f"insert into UserStrike ( "
        f"strike, "
        f"discord_id, "
        f"persistent, "
        f"date_created, "
        f"date_ended,  "
        f"removal_reason, "
        f"striker_user_id "
        f") "
        f"VALUES ( "
        f"(SELECT id from StrikeModel "
        f"WHERE name = '{strike_name}'), "
        f"{user_id}, "
        f"{persistent}, "
        f"now(), "
        f"date_add(now(), INTERVAL {rollover_days} DAY), "
        f"null, "
        f"{striker_user_id} "
        f");")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        user_strike = select_user_strike_list_active(user_id=user_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike


# select

def select_user_strike_list_active(user_id: int):
    """
        selects active User Strikes

        Args:
            `user_id` (int): discord user id of the user
                to list strikes

        Raises:
            `NotFoundError`: no User Strikes for user id found 

        Returns: `active_user_strikes` (list[UserStrike]): (
            `id`: int,
            `user_id`: int,
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

    # find user strikes based on user id
    query = (
        f"SELECT UserStrike.id as id, "
        f"UserStrike.discord_id as user_id, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"UserStrike.persistent as persistent, "
        f"UserStrike.date_created as date_created, "
        f"UserStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"UserStrike.striker_user_id as striker_user_id "
        f"FROM UserStrike "
        f"INNER JOIN StrikeModel ON UserStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON UserStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE UserStrike.discord_id = {user_id} "
        f"AND ( "
        f"now() < UserStrike.date_ended "
        f"OR UserStrike.persistent = True "
        f") "
        f"AND UserStrike.removal_reason IS NULL;")

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no active User Strikes for {user_id} found")

    user_strike_list: list[UserStrike] = []

    for data in query_data:
        user_strike_list.append(query_data_to_obj(data))

    return user_strike_list

# only for admin users


def select_user_strike_list_all(user_id: int):
    """
        selects User Strikes

        Args:
            `user_id` (int): discord user id of the user
                to list strikes

        Raises:
            `NotFoundError`: no User Strikes for user id found 

        Returns: `active_user_strikes` (list[UserStrike]): (
            `id`: int,
            `user_id`: int,
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

    # find user strikes based on user id
    query = (
        f"SELECT UserStrike.id as id, "
        f"UserStrike.discord_id as user_id, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"UserStrike.persistent as persistent, "
        f"UserStrike.date_created as date_created, "
        f"UserStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"UserStrike.striker_user_id as striker_user_id "
        f"FROM UserStrike "
        f"INNER JOIN StrikeModel ON UserStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON UserStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE UserStrike.discord_id = {user_id};")

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no User Strikes for {user_id} found")

    user_strike_list: list[UserStrike] = []

    for data in query_data:
        user_strike_list.append(query_data_to_obj(data))

    return user_strike_list


def select_user_strike(user_id: int, strike_id: int):
    """
        selects User Strike from given user id and strike id

        Args:
            `user_id` (int): discord user id of the user
            `strike_id` (int): id of the User Strike

        Raises:
            `NotFoundError`: User Strike with given user id and strike id
                not found

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # find user strikes based on user id
    query = (
        f"SELECT UserStrike.id as id, "
        f"UserStrike.discord_id as user_id, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"UserStrike.persistent as persistent, "
        f"UserStrike.date_created as date_created, "
        f"UserStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"UserStrike.striker_user_id as striker_user_id "
        f"FROM UserStrike "
        f"INNER JOIN StrikeModel ON UserStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON UserStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE UserStrike.discord_id = {user_id} "
        f"AND UserStrike.id = {strike_id};")

    # execute and return query
    data = preset.select(query)

    if data is None:
        raise NotFoundError(
            f"User Strike with user id {user_id} "
            f"and strike id {strike_id} not found"
        )

    user_strike: UserStrike = query_data_to_obj(data)

    return user_strike


# only for admin users
def select_user_strike_from_id(strike_id: int):
    """
        selects User Strike from given strike id

        Args:
            `strike_id` (int): id of the User Strike

        Raises:
            `NotFoundError`: User Strike with given strike id
                not found

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # find user strikes based on user id
    query = (
        f"SELECT UserStrike.id as id, "
        f"UserStrike.discord_id as user_id, "
        f"StrikeModel.name as strike_name, "
        f"StrikeModel.description as strike_description, "
        f"StrikeModel.strike_weight as strike_weight, "
        f"UserStrike.persistent as persistent, "
        f"UserStrike.date_created as date_created, "
        f"UserStrike.date_ended as date_ended, "
        f"RemovalReasonModel.name as removal_reason_name, "
        f"RemovalReasonModel.description as removal_reason_description, "
        f"UserStrike.striker_user_id as striker_user_id "
        f"FROM UserStrike "
        f"INNER JOIN StrikeModel ON UserStrike.strike = StrikeModel.id "
        f"LEFT JOIN RemovalReasonModel ON UserStrike.removal_reason = RemovalReasonModel.id "
        f"WHERE UserStrike.id = {strike_id};")

    # execute and return query
    data = preset.select(query)

    if data is None:
        raise NotFoundError(
            f"User Strike with strike id {strike_id} not found"
        )

    user_strike: UserStrike = query_data_to_obj(data)

    return user_strike


# update

def update_user_strike_toggle_persistent(user_id: int, strike_id: int):
    """
        toggles the `persistent` value for the specified User Strike

        Args:
            `user_id` (int): discord user id of the user
            `strike_id` (int): id of the User Strike

        Raises:
            `NotFoundError`: User Strike with given user id and strike id
                not found

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # get user strike
    try:
        user_strike = select_user_strike(
            user_id=user_id,
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query toggling the persistent status
    query = (
        f"UPDATE UserStrike SET persistent "
        f"= {not bool(user_strike.persistent)} "
        f"WHERE discord_id = {user_id} "
        f"AND id = {user_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        user_strike = select_user_strike(
            user_id=user_id, strike_id=user_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike


# only for super user
def update_user_strike_toggle_persistent_from_id(strike_id: int):
    """
        toggles the `persistent` value for the specified User Strike

        Args:
            `strike_id` (int): id of the User Strike

        Raises:
            `NotFoundError`: User Strike with given strike id
                not found

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # get user strike
    try:
        user_strike = select_user_strike_from_id(
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query toggling the persistent status
    query = (
        f"UPDATE UserStrike SET persistent "
        f"= {not bool(user_strike.persistent)} "
        f"WHERE id = {user_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        user_strike = select_user_strike_from_id(
            strike_id=user_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike


def update_user_strike_add_removal_reason(
    user_id: int, strike_id: int, removal_reason_name: str
):
    """
        adds a removal reason to the User Strike

        Args:
            `user_id` (int): discord user id of the user
            `strike_id` (int): id of the User Strike
            `removal_reason_name` (str): Removal Reason name

        Raises:
            `NotFoundError`: User Strike with given user id and strike id
                not found
            `ConflictError`: User Strike already has removal reason

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # get user strike
    try:
        user_strike = select_user_strike(
            user_id=user_id,
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    try:
        removal_reason = select_removal_reason_model_from_name(
            name=removal_reason_name
        )

    except NotFoundError as arg:
        raise NotFoundError(arg)

    if user_strike.removal_reason_name is not None:
        raise ConflictError(
            f"User Strike id {id} already has "
            f"removal reason '{user_strike.removal_reason_name}'")

    # set up the query adding a removal reason the persistent status
    query = (
        f"UPDATE UserStrike SET removal_reason = ( "
        f"SELECT id FROM RemovalReasonModel "
        f"WHERE name = '{removal_reason_name}') "
        f"WHERE discord_id = {user_id} "
        f"AND id = {strike_id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        user_strike = select_user_strike(
            user_id=user_id, strike_id=user_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike


# only for super user
def update_user_strike_add_removal_reason_from_id(
    strike_id: int, removal_reason_name: str
):
    """
        adds a removal reason to the User Strike

        Args:
            `strike_id` (int): id of the User Strike
            `removal_reason_name` (str): Removal Reason name

        Raises:
            `NotFoundError`: User Strike with given user id and strike id
                not found
            `ConflictError`: User Strike already has removal reason

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # get user strike
    try:
        user_strike = select_user_strike_from_id(
            strike_id=strike_id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    try:
        removal_reason = select_removal_reason_model_from_name(
            name=removal_reason_name
        )

    except NotFoundError as arg:
        raise NotFoundError(arg)

    if user_strike.removal_reason_name is not None:
        raise ConflictError(
            f"User Strike id {user_strike.id} already has "
            f"removal reason '{user_strike.removal_reason_name}'")

    # set up the query adding a removal reason the persistent status
    query = (
        f"UPDATE UserStrike SET removal_reason = ( "
        f"SELECT id FROM RemovalReasonModel "
        f"WHERE name = '{removal_reason_name}') "
        f"WHERE id = {user_strike.id};")

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        user_strike = select_user_strike_from_id(
            strike_id=user_strike.id)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return user_strike


# delete

def delete_user_strike(strike_id: int):
    """
        deletes the specified User Strike

        Args:
            `strike_id` (int): id of the User Strike

        Raises:
            `NotFoundError`: User Strike not found after deletion
            `ConflictError`: User Strike with specified id does not exist

        Returns: `user_strike` (UserStrike): (
            `id`: int,
            `user_id`: int,
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

    # check if user strike is created
    try:
        user_strike = select_user_strike_from_id(strike_id=strike_id)

    except NotFoundError:
        raise ConflictError(
            f"User Strike with id {strike_id} "
            f"not found")

    # set up the query
    query = (
        f"DELETE FROM UserStrike WHERE id='{strike_id}'"
    )

    # execute delete query
    preset.delete(query)

    # search user strike and show it was deleted
    try:
        user_strike = select_user_strike_from_id(strike_id=strike_id)

    except NotFoundError:
        raise NotFoundError(
            f"User Strike with id {strike_id} "
            f"deleted correctly")

    return user_strike
