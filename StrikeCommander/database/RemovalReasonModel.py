import database.RazBotDB_Presets as preset
from errors.errors_db import (
    NotFoundError,
    ConflictError
)


# Removal Reason Model class

class RemovalReasonModel(object):
    """
        RemovalReasonModel: object for db Removal Reason Model table objects

            Instance Attributes
                `name` (str): Removal Reason name
                `description` (str): Removal Reason description
                `active` (bool): whether or not the Removal Reason is active
                    for adding to users and players
                    default true
    """

    def __init__(self, name: str, description: str, active: bool):
        self.name = name
        self.description = description
        self.active = active


def query_data_to_obj(query_data: tuple):
    """
        take in the tuple of the query data
        and return Removal Reason Model class object

        Args:
            `query_data` (tuple): tuple of Removal Reason Model query
                `name`: str
                `description`: str
                `active`: bool

        Returns:
            obj: `Removal Reason Model` (name: str, description: str,
                active: bool)
    """

    (name, description, active) = query_data

    return RemovalReasonModel(
        name=name, description=description, active=bool(active)
    )


# insert

def insert_removal_reason_model(
        name: str,
        description: str):
    """
        insert Removal Reason Model

        Args:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description

        Raises:
            `ConflictError`: Removal Reason Model with specified name 
                already exists
            `NotFoundError`: Removal Reason Model with specified name 
                not found after insert

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the removal reason is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")
    description = description.replace("\\'", "'")

    name = name.replace("'", "\\'")
    description = description.replace("'", "\\'")

    # check if removal reason model already exists
    try:
        removal_reason_model = select_removal_reason_model_from_name(name=name)

        # removal reason model with given name found, raise error
        raise ConflictError(
            f"Removal Reason Model with name {name} already exists")

    # removal reason model not found, move on with insert
    except NotFoundError:
        pass

    # set up the query
    query = (
        f"INSERT into RemovalReasonModel (name, description) "
        f"VALUES ('{name}', '{description}');"
    )

    # execute update query
    preset.update(query)

    # select and return removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(
            f"Removal Reason Model with name {name} not found after insert"
        )

    return removal_reason_model


# select

def select_removal_reason_model_active():
    """
        selects all active Removal Reason Models

        Args:

        Raises:
            `NotFoundError`: no active Removal Reason Models were found

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the removal reason is active
                for adding to users and players
    """

    # find removal reason model based on active status
    query = (
        f"SELECT name, description, active FROM RemovalReasonModel "
        f"WHERE active = True;"
    )

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no active Removal Reason Models were found"
        )

    removal_reason_model_list: list[RemovalReasonModel] = []

    for data in query_data:
        removal_reason_model_list.append(query_data_to_obj(data))

    return removal_reason_model_list


def select_removal_reason_model_all():
    """
        selects all Removal Reason Models

        Args:

        Raises:
            `NotFoundError`: no Removal Reason Models were found

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the removal reason is active
                for adding to users and players
    """

    # find all removal reason models
    query = (
        f"SELECT name, description, active FROM RemovalReasonModel;"
    )

    # execute and return query
    query_data = preset.select_list(query)

    if len(query_data) == 0:
        raise NotFoundError(
            f"no Removal Reason Models were found"
        )

    removal_reason_model_list: list[RemovalReasonModel] = []

    for data in query_data:
        removal_reason_model_list.append(query_data_to_obj(data))

    return removal_reason_model_list


def select_removal_reason_model_from_name(name: str):
    """
        selects Removal Reason Models from the given name

        Args:
            `name` (str): Removal Reason Model Name

        Raises:
            `NotFoundError`: Removal Reason Model with specified name
                not found

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the Removal Reason is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # find removal reason model based on name
    query = (
        f"SELECT name, description, active FROM RemovalReasonModel "
        f"WHERE name = '{name}';"
    )

    # execute and return query
    data = preset.select(query)

    if data is None:
        raise NotFoundError(
            f"Removal Reason Model with name {name} not found"
        )

    removal_reason_model: RemovalReasonModel = query_data_to_obj(data)

    return removal_reason_model


# update

def update_removal_reason_model_active_toggle(name: str):
    """
        toggles the active value for the specified Removal Reason Model

        Args:
            `name` (str): Removal Reason Model Name

        Raises:
            `NotFoundError`: Removal Reason Model with specified name not found

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the Removal Reason is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # get removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # set up the query toggling the active status
    query = (
        f"UPDATE RemovalReasonModel SET active = "
        f"{not bool(removal_reason_model.active)} "
        f"WHERE name = '{name}';"
    )

    # execute update query
    preset.update(query)

    # select and return removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return removal_reason_model


def update_removal_reason_model_edit(
        name: str,
        description: str):
    """
        edits the given values for a specified Removal Reason Model
            does NOT change name values, use update_removal_reason_model_edit_name

        Args:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description

        Raises:
            `NotFoundError`: Removal Reason Model with specified name not found

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the Removal Reason is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")
    description = description.replace("\\'", "'")

    name = name.replace("'", "\\'")
    description = description.replace("'", "\\'")

    # get removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    query = (f"UPDATE RemovalReasonModel SET description = '{description}' "
             f"WHERE name = '{name}';")

    # execute update query
    preset.update(query)

    # select and return removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return removal_reason_model


def update_removal_reason_model_edit_name(current_name: str, new_name: str):
    """
        edits the name for a specified Removal Reason Model

        Args:
            `current_name` (str): Removal Reason Model's current name
            `new_name` (str): Removal Reason Model's name to change to

        Raises:
            `NotFoundError`: Removal Reason Model with specified name not found after insert
            `ConflictError`: Removal Reason Model with specified name already exists

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the Removal Reason is active
                for adding to users and players
    """

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    current_name = current_name.replace("\\'", "'")
    new_name = new_name.replace("\\'", "'")

    current_name = current_name.replace("'", "\\'")
    new_name = new_name.replace("'", "\\'")

    # get removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(
            name=current_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    # check if updated removal reason model name exists
    try:
        removal_reason_model = select_removal_reason_model_from_name(
            name=new_name)

        # removal reason model with given name found, raise error
        raise ConflictError(
            f"Removal Reason Model with name {new_name} already exists")

    # removal reason model not found, move on with insert
    except NotFoundError:
        pass

    query = (
        f"UPDATE RemovalReasonModel SET name = '{new_name}'"
        f" WHERE name = '{current_name}';"
    )

    # execute update query
    preset.update(query)

    # select and return removal reason model
    try:
        removal_reason_model = select_removal_reason_model_from_name(
            name=new_name)

    except NotFoundError as arg:
        raise NotFoundError(arg)

    return removal_reason_model


# delete

def delete_removal_reason_model(name: str):
    """
        deletes the specified Removal Reason Model
            raises NotFoundError if Removal Reason Model not found after delete

        Args:
            `name` (str): Removal Reason Model Name

        Raises:
            `ConflictError`: Removal Reason Model with specified name does not exist
            `NotFoundError`: Removal Reason Model not found after deletion

        Returns:
            `name` (str): Removal Reason name
            `description` (str): Removal Reason description
            `active` (bool): whether or not the Removal Reason is active
                for adding to users and players
    """

    # search removal reason model and show it was deleted
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError:
        raise ConflictError(
            f"Removal Reason Model with name {name} "
            f"not found")

    # formatting in case of single quote
    # single quote will cause db query error

    # removing formatting for replacing purposes
    name = name.replace("\\'", "'")

    name = name.replace("'", "\\'")

    # set up the query
    query = (
        f"DELETE FROM RemovalReasonModel WHERE name='{name}'"
    )

    # execute delete query
    preset.delete(query)

    # search removal reason model and show it was deleted
    try:
        removal_reason_model = select_removal_reason_model_from_name(name)

    except NotFoundError:
        raise NotFoundError(
            f"Removal Reason Model with name {name} "
            f"deleted correctly")

    return removal_reason_model
