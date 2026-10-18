"""Exceptions raised by the commit-me package."""

import pathlib


class MissingCliError(Exception):
    """Raised when one or more required CLIs are missing or not on the PATH."""

    MESSAGE_TEMPLATE: str = "Missing or not added to path cli(s): {cli_names}"
    cli_names: list[str]

    def __init__(self, *, cli_names: list[str]) -> None:
        """Initialize the error with the names of the missing CLIs.

        Args:
            cli_names: Names of the CLIs that are missing.
        """
        self.cli_names = cli_names
        super().__init__(self.MESSAGE_TEMPLATE.format(cli_names=",".join(cli_names)))


class NoGitRepoError(Exception):
    MESSAGE = "No Git repository found in: {directory}"

    def __init__(self, *, directory: pathlib.Path) -> None:
        super().__init__(self.MESSAGE.format(directory=str(directory.absolute())))


class NoStagedChangesError(Exception):
    MESSAGE = "No staged changes found in: {directory}"

    def __init__(self, *, directory: pathlib.Path) -> None:
        super().__init__(self.MESSAGE.format(directory=str(directory.absolute())))
