"""Exceptions raised by the commit-me package."""


class MissingCliError(Exception):
    """Raised when one or more required CLIs are missing or not on the PATH."""

    MESSAGE_TEMPLATE: str = "Missing or not added to path cli(s): {cli_names}"
    cli_names: list[str]

    def __init__(self, cli_names: list[str]) -> None:
        """Initialize the error with the names of the missing CLIs.

        Args:
            cli_names: Names of the CLIs that are missing.
        """
        self.cli_names = cli_names
        super().__init__(self.MESSAGE_TEMPLATE.format(cli_names=cli_names))
