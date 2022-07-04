
class ResponderModel(object):
    """
        ResponderModel: object for responder functions

            Instance Attributes
                `title` (str): title for embed
                    default None
                `description` (str): description for embed
                    default None
                `field_dict_list` (list): list of dicts for embed fields{name, value, inline (default: True)} 
                    default []
    """

    def __init__(
        self, title: str = None,
        description: str = None,
        field_dict_list: list[dict] = []
    ):
        self.title = title
        self.description = description
        self.field_dict_list = field_dict_list
