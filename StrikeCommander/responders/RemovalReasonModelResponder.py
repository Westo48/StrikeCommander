from database.RemovalReasonModel import RemovalReasonModel
from responders.ResponderModel import ResponderModel
from errors.errors_db import (
    NotFoundError,
    ConflictError
)
from database.RemovalReasonModel import (
    insert_removal_reason_model,
    select_removal_reason_model_from_name,
    select_removal_reason_model_all,
    select_removal_reason_model_active,
    update_removal_reason_model_edit,
    update_removal_reason_model_edit_name,
    update_removal_reason_model_active_toggle,
    delete_removal_reason_model
)


def get_removal_reason_model_active():
    """
        returns ResponderModel
    """

    try:
        removal_reason_models: list[RemovalReasonModel] = (
            select_removal_reason_model_active())

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = "Active Removal Reason Models"

    # set description
    description = f"count: {len(removal_reason_models)}"

    field_dict_list = []

    for removal_reason_model in removal_reason_models:
        field_dict_list.append({
            'name': removal_reason_model.name,
            'value': (
                f"description: {removal_reason_model.description}"
            )
        })

    return ResponderModel(
        title=title, description=description,
        field_dict_list=field_dict_list
    )


def get_removal_reason_model_all():
    """
        returns ResponderModel
    """

    try:
        removal_reason_models: list[RemovalReasonModel] = (
            select_removal_reason_model_all())

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = "All Removal Reason Models"

    # set description
    description = f"count: {len(removal_reason_models)}"

    field_dict_list = []

    for removal_reason_model in removal_reason_models:
        field_dict_list.append({
            'name': removal_reason_model.name,
            'value': (
                f"active: {removal_reason_model.active}\n"
                f"description: {removal_reason_model.description}"
            )
        })

    return ResponderModel(
        title=title, description=description,
        field_dict_list=field_dict_list
    )


def update_removal_reason_model(
    name: str,
    description: str
):
    """
        returns ResponderModel
    """

    try:
        removal_reason_model = update_removal_reason_model_edit(
            name=name,
            description=description
        )

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Updated {removal_reason_model.name}"

    # set description
    embed_description = (
        f"active: {removal_reason_model.active}\n"
        f"description: {removal_reason_model.description}"
    )

    return ResponderModel(
        title=title, description=embed_description
    )


def update_removal_reason_model_name(
    current_name: str, new_name: str
):
    """
        returns ResponderModel
    """

    try:
        removal_reason_model = update_removal_reason_model_edit_name(
            current_name=current_name,
            new_name=new_name
        )

    except ConflictError as arg:
        return ResponderModel(
            title=f"could not update Removal Reason Model",
            description=f"{arg}"
        )

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Updated {removal_reason_model.name}"

    # set description
    embed_description = (
        f"active: {removal_reason_model.active}\n"
        f"description: {removal_reason_model.description}"
    )

    return ResponderModel(
        title=title, description=embed_description
    )


def update_removal_reason_model_toggle(name: str):
    """
        returns ResponderModel
    """

    try:
        removal_reason_model = update_removal_reason_model_active_toggle(
            name=name)

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Updated {removal_reason_model.name}"

    # set description
    description = (
        f"active: {removal_reason_model.active}\n"
        f"description: {removal_reason_model.description}"
    )

    return ResponderModel(
        title=title, description=description
    )


def add_removal_reason_model(
    name: str,
    description: str
):
    """
        returns ResponderModel
    """

    if (
        name is None
        or description is None
    ):
        return ResponderModel(
            title="could not add Removal Reason Model",
            description="supply all applicable data"
        )

    try:
        removal_reason_model = insert_removal_reason_model(
            name=name,
            description=description
        )

    except ConflictError as arg:
        return ResponderModel(
            title=f"could not add Removal Reason Model",
            description=f"{arg}"
        )

    except NotFoundError as arg:
        return ResponderModel(
            title=f"not found",
            description=f"{arg}"
        )

    # set title
    title = f"Added {removal_reason_model.name}"

    # set description
    description = (
        f"active: {removal_reason_model.active}\n"
        f"description: {removal_reason_model.description}"
    )

    return ResponderModel(
        title=title, description=description
    )


def remove_removal_reason_model(name: str):
    """
        returns ResponderModel
    """

    try:
        removal_reason_model = delete_removal_reason_model(name=name)

    except ConflictError as arg:
        return ResponderModel(
            title=f"could not find Removal Reason Model",
            description=f"{name} was not found"
        )
    except NotFoundError as arg:
        return ResponderModel(
            title=f"deleted Removal Reason Model",
            description=f"{name} was deleted"
        )

    # set title
    title = f"could not delete Removal Reason Model"

    # set description
    description = (
        f"{name} could not be deleted"
    )

    return ResponderModel(
        title=title, description=description
    )
