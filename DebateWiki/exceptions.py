class CoreError(Exception):
    """Base exception class for Core modules and internal use."""

    pass


class UserError(Exception):
    """Base exception class raised as a byproduct of misconfiguration."""

    pass


class CommandLineError(Exception):
    """Base exception raised when there is an issue with the command line interface."""

    pass


class ArgumentNotFoundError(CommandLineError):
    """Exception raised when an argument required in the CLI is not found."""

    def __init__(self, message):
        super().__init__(message)
