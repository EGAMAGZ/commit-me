"""Exceptions raised by the commit-me package."""

import pathlib


class MissingCliError(Exception):
    """Raised when one or more required CLIs are missing or not on the PATH."""

    MESSAGE_TEMPLATE: str = (
        "Required CLI(s) not found on PATH: {cli_names}."
        " Install them and make sure they are available in your shell."
    )
    cli_names: list[str]

    def __init__(self, *, cli_names: list[str]) -> None:
        """Initialize the error with the names of the missing CLIs.

        Args:
            cli_names: Names of the CLIs that are missing.
        """
        self.cli_names = cli_names
        super().__init__(self.MESSAGE_TEMPLATE.format(cli_names=", ".join(cli_names)))


class NoGitRepoError(Exception):
    """Raised when the target directory is not inside a Git repository."""

    MESSAGE = (
        "No Git repository found in: {directory}."
        " Run inside a repository or pass a path to one."
    )

    def __init__(self, *, directory: pathlib.Path) -> None:
        """Initialize the error with the directory that is not a repository.

        Args:
            directory: Directory that was checked for a Git repository.
        """
        super().__init__(self.MESSAGE.format(directory=str(directory.absolute())))


class NoStagedChangesError(Exception):
    """Raised when the repository has no staged changes to commit."""

    MESSAGE = (
        "No staged changes found in: {directory}."
        " Stage your changes first with `git add`."
    )

    def __init__(self, *, directory: pathlib.Path) -> None:
        """Initialize the error with the directory that has no staged changes.

        Args:
            directory: Directory of the repository that was checked.
        """
        super().__init__(self.MESSAGE.format(directory=str(directory.absolute())))
