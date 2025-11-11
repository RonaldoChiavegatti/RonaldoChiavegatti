class ApplicationError(Exception):
    """Base class for application-level exceptions."""

    pass


class AgentNotFoundError(ApplicationError):
    """Raised when a specific agent is not found."""

    pass


class InsufficientBalanceError(ApplicationError):
    """Raised when the billing service reports insufficient funds."""

    pass
