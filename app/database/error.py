class BaseDBError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundInDBError(BaseDBError):
    def __init__(self, message="Item not found in database"):
        super().__init__(message)


class ConflictWithRequestDBError(BaseDBError):
    def __init__(self, message="Request data conflict with database"):
        super().__init__(message)
