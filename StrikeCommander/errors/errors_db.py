class NotFoundError(Exception):
    """requested data not found in DB"""
    pass


class ConflictError(Exception):
    """requested insert already in DB"""
    pass
