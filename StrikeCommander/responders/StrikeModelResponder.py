from database.StrikeModel import StrikeModel
from responders.ResponderModel import ResponderModel
from errors.errors_db import (
    NotFoundError,
    ConflictError
)
from database.StrikeModel import (
    select_strike_model_from_name,
    select_strike_model_active,
    select_strike_model_all,
    insert_strike_model,
    update_strike_model_active_toggle,
    update_strike_model_edit,
    update_strike_model_edit_name,
    delete_strike_model
)


def get_strike_model_from_name(name: str):
    """
        returns ResponderModel
    """

    try:
        strike_model: StrikeModel = select_strike_model_from_name(name=name)

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Strike Model"

    # set description
    description = f"{strike_model.name}"

    field_dict_list = []

    field_dict_list.append({
        'name': strike_model.name,
        'value': (
            f"Description: {strike_model.description}\n"
            f"Strikes: {strike_model.strike_weight}\n"
            f"Persistent: {strike_model.persistent}\n"
            f"Rollover Days: {strike_model.rollover_days}"
        )
    })

    return ResponderModel(
        title=title, description=description,
        field_dict_list=field_dict_list
    )


def get_strike_model_active():
    """
        returns ResponderModel
    """

    try:
        strike_models: list[StrikeModel] = select_strike_model_active()

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = "Active Strike Models"

    # set description
    description = f"count: {len(strike_models)}"

    field_dict_list = []

    for strike_model in strike_models:
        field_dict_list.append({
            'name': strike_model.name,
            'value': (
                f"Description: {strike_model.description}\n"
                f"Strikes: {strike_model.strike_weight}\n"
                f"Persistent: {strike_model.persistent}\n"
                f"Rollover Days: {strike_model.rollover_days}"
            )
        })

    return ResponderModel(
        title=title, description=description,
        field_dict_list=field_dict_list
    )


def get_strike_model_all():
    """
        returns ResponderModel
    """

    try:
        strike_models: list[StrikeModel] = select_strike_model_all()

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = "All Strike Models"

    # set description
    description = f"count: {len(strike_models)}"

    field_dict_list = []

    for strike_model in strike_models:
        field_dict_list.append({
            'name': strike_model.name,
            'value': (
                f"Active: {strike_model.active}\n"
                f"Description: {strike_model.description}\n"
                f"Strikes: {strike_model.strike_weight}\n"
                f"Persistent: {strike_model.persistent}\n"
                f"Rollover Days: {strike_model.rollover_days}"
            )
        })

    return ResponderModel(
        title=title, description=description,
        field_dict_list=field_dict_list
    )


def update_strike_model(
    name: str,
    description: str = None,
    strike_weight: int = None,
    persistent: bool = None,
    rollover_days: int = None
):
    """
        returns ResponderModel
    """

    try:
        strike_model = update_strike_model_edit(
            name=name,
            description=description,
            strike_weight=strike_weight,
            persistent=persistent,
            rollover_days=rollover_days
        )

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Updated {strike_model.name}"

    # set description
    embed_description = (
        f"Active: {strike_model.active}\n"
        f"Description: {strike_model.description}\n"
        f"Strikes: {strike_model.strike_weight}\n"
        f"Persistent: {strike_model.persistent}\n"
        f"Rollover Days: {strike_model.rollover_days}"
    )

    return ResponderModel(
        title=title, description=embed_description
    )


def update_strike_model_name(
    current_name: str, new_name: str
):
    """
        returns ResponderModel
    """

    try:
        strike_model = update_strike_model_edit_name(
            current_name=current_name,
            new_name=new_name
        )

    except ConflictError as arg:
        return ResponderModel(
            title=f"could not update Strike Model",
            description=f"{arg}"
        )

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Updated {strike_model.name}"

    # set description
    embed_description = (
        f"Active: {strike_model.active}\n"
        f"Description: {strike_model.description}\n"
        f"Strikes: {strike_model.strike_weight}\n"
        f"Persistent: {strike_model.persistent}\n"
        f"Rollover Days: {strike_model.rollover_days}"
    )

    return ResponderModel(
        title=title, description=embed_description
    )


def update_strike_model_toggle(name: str):
    """
        returns ResponderModel
    """

    try:
        strike_model = update_strike_model_active_toggle(
            name=name)

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Updated {strike_model.name}"

    # set description
    description = (
        f"Active: {strike_model.active}\n"
        f"Description: {strike_model.description}\n"
        f"Strikes: {strike_model.strike_weight}\n"
        f"Persistent: {strike_model.persistent}\n"
        f"Rollover Days: {strike_model.rollover_days}"
    )

    return ResponderModel(
        title=title, description=description
    )


def add_strike_model(
    name: str,
    description: str,
    strike_weight: int,
    persistent: bool,
    rollover_days: int
):
    """
        returns ResponderModel
    """

    if (
        name is None
        or description is None
        or strike_weight is None
        or persistent is None
        or rollover_days is None
    ):
        return ResponderModel(
            title="could not add Strike Model",
            description="supply all applicable data"
        )

    try:
        strike_model = insert_strike_model(
            name=name,
            description=description,
            strike_weight=strike_weight,
            persistent=persistent,
            rollover_days=rollover_days
        )

    except ConflictError as arg:
        return ResponderModel(
            title=f"could not add Strike Model",
            description=f"{arg}"
        )

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Added {strike_model.name}"

    # set description
    description = (
        f"Active: {strike_model.active}\n"
        f"Description: {strike_model.description}\n"
        f"Strikes: {strike_model.strike_weight}\n"
        f"Persistent: {strike_model.persistent}\n"
        f"Rollover Days: {strike_model.rollover_days}"
    )

    return ResponderModel(
        title=title, description=description
    )


def remove_strike_model(name: str):
    """
        returns ResponderModel
    """

    try:
        strike_model = delete_strike_model(name=name)

    except ConflictError as arg:
        return ResponderModel(
            title=f"could not find Strike Model",
            description=f"{name} was not found"
        )
    except NotFoundError as arg:
        return ResponderModel(
            title=f"deleted Strike Model",
            description=f"{name} was deleted"
        )

    # set title
    title = f"could not delete Strike Model"

    # set description
    description = (
        f"{name} could not be deleted"
    )

    return ResponderModel(
        title=title, description=description
    )
