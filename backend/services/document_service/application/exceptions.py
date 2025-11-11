class ApplicationError(Exception):
    """Base class for application-level exceptions."""

    pass


class JobNotFoundError(ApplicationError):
    """Raised when a specific job is not found."""

    pass


class JobAccessForbiddenError(ApplicationError):
    """Raised when a user tries to access a job that does not belong to them."""

    pass
