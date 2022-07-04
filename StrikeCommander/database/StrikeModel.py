import database.RazBotDB_Presets as preset
from errors.errors_db import (
    NotFoundError,
    ConflictError
)


# Strike Model class

class StrikeModel(object):
    """
        StrikeModel: object for db Strike Model table objects

            Instance Attributes
                `name` (str): Strike name
                `description` (str): Strike description
                `strike_weight` (int): amount the strike is worth
                    default 1
                `persistent` (bool): whether or not the strike is persistent
                    by default
                    default false
                `rollover_days` (int): amount of rollover days by default
                    default 30
                `active` (bool): whether or not the strike is active
                    for adding to users and players
                    default true
    """

    def __init__(self, name: str, description: str, strike_weight: int,
                 persistent: bool, rollover_days: int, active: bool):
        self.name = name
        self.description = description
        self.strike_weight = strike_weight
        self.persistent = persistent
        self.rollover_days = rollover_days
        self.active = active


def query_data_to_obj(query_data: tuple):
    """
        take in the tuple of the query data
        and return Strike Model class object

        Args:
            `query_data` (tuple): tuple of Strike Model query
                `name`: str
                `description`: str
                `strike_weight`: int
                `persistent`: bool
                `rollover_days`: int
                `active`: bool

        Returns:
            obj: `StrikeModel` (name: str, description: str,
                strike_weight: int, persistent: bool,
                rollover_days: int, active: bool)
    """

    (name, description, strike_weight,
        persistent, rollover_days, active) = query_data

    return StrikeModel(
        name=name, description=description, strike_weight=strike_weight,
        persistent=bool(persistent), rollover_days=rollover_days,
        active=bool(active)
    )


# insert

def insert_strike_model(
        name: str,
        description: str,
        strike_weight: int = 1,
        persistent: bool = False,
        rollover_days: int = 30):
    """
        insert Strike Model

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
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")
    description = description.replace("\\'", "'")

    name = name.replace("'", "\\'")
    description = description.replace("'", "\\'")

    # check if strike model already exists
    try:
        strike_model = select_strike_model_from_name(name=name)

        # strike model with given name found, raise error
        raise ConflictError(f"Strike Model with name {name} already exists")

    # strike model not found, move on with insert
    except NotFoundError:
        pass

    strike_weight = abs(int(strike_weight))
    rollover_days = abs(int(rollover_days))

    # set up the query
    query = (
        f"INSERT into StrikeModel ("
        f"name, description, strike_weight, persistent, rollover_days) "
        f"VALUES ('{name}', '{description}', {strike_weight}, "
        f"{persistent}, {rollover_days});"
    )

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(
            f"Strike Model with name {name} not found after insert"
        )

    return strike_model


# select

def select_strike_model_active():
    """
        selects all active Strike Models

        Args:

        Raises:
            `NotFoundError`: no active Strike Models were found

        Returns:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # find strike model based on active status
    query = (
        f"SELECT name, description, strike_weight, "
        f"persistent, rollover_days, active FROM StrikeModel "
        f"WHERE active = True;"
    )

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no active Strike Models were found"
        )

    strike_model_list: list[StrikeModel] = []

    for data in query_data:
        strike_model_list.append(query_data_to_obj(data))

    return strike_model_list


def select_strike_model_all():
    """
        selects all Strike Models

        Args:

        Raises:
            `NotFoundError`: no Strike Models were found

        Returns:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # find all strike models
    query = (
        f"SELECT name, description, strike_weight, "
        f"persistent, rollover_days, active FROM StrikeModel;"
    )

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no Strike Models were found"
        )

    strike_model_list: list[StrikeModel] = []

    for data in query_data:
        strike_model_list.append(query_data_to_obj(data))

    return strike_model_list


def select_strike_model_from_name(name: str):
    """
        selects Strike Models from the given name

        Args:
            `name` (str): Strike Model Name

        Raises:
            `NotFoundError`: Strike Model with specified name not found

        Returns:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # find strike model based on name
    query = (
        f"SELECT name, description, strike_weight, "
        f"persistent, rollover_days, active FROM StrikeModel "
        f"WHERE name = '{name}';"
    )

    # execute and return query
    data = preset.select(query)

    if data is None:
        raise NotFoundError(
            f"Strike Model with name {name} not found"
        )

    strike_model: StrikeModel = query_data_to_obj(data)

    return strike_model


# update

def update_strike_model_active_toggle(name: str):
    """
        toggles the active value for the specified Strike Model

        Args:
            `name` (str): Strike Model Name

        Raises:
            `NotFoundError`: Strike Model with specified name not found

        Returns:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # get strike model
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query toggling the active status
    query = (
        f"UPDATE StrikeModel SET active = "
        f"{not bool(strike_model.active)} "
        f"WHERE name = '{name}';"
    )

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return strike_model


def update_strike_model_edit(
        name: str,
        description: str = None,
        strike_weight: int = None,
        persistent: bool = None,
        rollover_days: int = None):
    """
        edits the given values for a specified Strike Model
            does NOT change name values, use update_strike_model_edit_name

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
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # get strike model
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # no new data was passed
    if (description is None
        and strike_weight is None
        and persistent is None
            and rollover_days is None):

        return strike_model

    query = f"UPDATE StrikeModel SET "

    # updated description value given
    if description is not None:
        # formatting in case of single quote
        # single quote will cause db query error

        # removing formatting for replacing purposes
        description = description.replace("\\'", "'")

        description = description.replace("'", "\\'")

        query += f"description = '{description}', "

    # updated strike weight value given
    if strike_weight is not None:
        strike_weight = abs(int(strike_weight))

        query += f"strike_weight = {strike_weight}, "

    # updated persistent value given
    if persistent is not None:
        query += f"persistent = {persistent}, "

    # updated rollover days value given
    if rollover_days is not None:
        rollover_days = abs(int(rollover_days))

        query += f"rollover_days = {rollover_days}, "

    # removing trailing ", " from query string
    query = query[:-2]

    query += f" WHERE name = '{name}';"

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return strike_model


def update_strike_model_edit_name(current_name: str, new_name: str):
    """
        edits the name for a specified Strike Model

        Args:
            `current_name` (str): Strike Model's current name
            `new_name` (str): Strike Model's name to change to

        Raises:
            `NotFoundError`: Strike Model with specified name not found after insert
            `ConflictError`: Strike Model with specified name already exists

        Returns:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    current_name = current_name.replace("\\'", "'")
    new_name = new_name.replace("\\'", "'")

    current_name = current_name.replace("'", "\\'")
    new_name = new_name.replace("'", "\\'")

    # get strike model
    try:
        strike_model = select_strike_model_from_name(current_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # check if updated strike model name exists
    try:
        strike_model = select_strike_model_from_name(name=new_name)

        # strike model with given name found, raise error
        raise ConflictError(
            f"Strike Model with name {new_name} already exists")

    # strike model not found, move on with insert
    except NotFoundError:
        pass

    query = (
        f"UPDATE StrikeModel SET name = '{new_name}'"
        f" WHERE name = '{current_name}';"
    )

    # execute update query
    preset.update(query)

    # select and return strike model
    try:
        strike_model = select_strike_model_from_name(new_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return strike_model


# delete

def delete_strike_model(name: str):
    """
        deletes the specified Strike Model
            raises NotFoundError if Strike Model not found after delete

        Args:
            `name` (str): Strike Model Name

        Raises:
            `ConflictError`: Strike Model with specified name does not exist
            `NotFoundError`: Strike Model not found after deletion

        Returns:
            `name` (str): Strike name
            `description` (str): Strike description
            `strike_weight` (int): amount the strike is worth
            `persistent` (bool): whether or not the strike is persistent
                by default
            `rollover_days` (int): amount of rollover days by default
            `active` (bool): whether or not the strike is active
                for adding to users and players
    """

    # search strike model and show it was deleted
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError:
        raise ConflictError(
            f"Strike Model with name {name} "
            f"not found")

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # set up the query
    query = (
        f"DELETE FROM StrikeModel WHERE name='{name}'"
    )

    # execute delete query
    preset.delete(query)

    # search strike model and show it was deleted
    try:
        strike_model = select_strike_model_from_name(name)

    except NotFoundError:
        raise NotFoundError(
            f"Strike Model with name {name} "
            f"deleted correctly")

    return strike_model
