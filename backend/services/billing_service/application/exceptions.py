class ApplicationError(Exception):
    """Base class for application-level exceptions."""

    pass


class InsufficientBalanceError(ApplicationError):
    """Raised when a charge is attempted with insufficient funds."""

    pass


class UserNotFoundError(ApplicationError):
    """Raised when a balance or transactions are requested for a non-existent user."""

    pass
