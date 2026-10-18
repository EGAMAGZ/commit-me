"""Utilities for detecting required command-line tools."""

import pathlib
import shutil
import subprocess
from typing import TypedDict, Never

import rich_click as click

from commit_me.exceptions import MissingCliError, NoGitRepoError


class Cli(TypedDict):
    """Metadata for a command-line tool that must be available."""

    name: str
    cmd: str


REQUIRED_CLIS: list[Cli] = [
    {"name": "Git", "cmd": "git"},
    {"name": "Opencode", "cmd": "opencode"},
]


def is_cli_installed(cli_info: Cli) -> bool:
    """Return whether the given CLI is present on the PATH.

    Args:
        cli_info: Metadata of the CLI to look up.

    Returns:
        True if the CLI command was found on the PATH.
    """
    return bool(shutil.which(cli_info["cmd"]))


def check_required_clis() -> dict[str, dict] | Never:
    """Raise MissingCliError if any required CLI is not installed."""
    missing_clis = [cli["name"] for cli in REQUIRED_CLIS if not is_cli_installed(cli)]
    if missing_clis:
        raise MissingCliError(cli_names=missing_clis)

    return {cli["cmd"]: {"path": shutil.which(cli["cmd"])} for cli in REQUIRED_CLIS}


def create_commit(
    *,
    message: str,
    directory: pathlib.Path,
    preview: bool,
) -> None:
    """Create a Git commit with the given message, optionally after a preview.

    Args:
        message: Commit message to use.
        directory: Directory of the Git repository to commit in.
        preview: Whether to show the message and ask for confirmation first.
    """

    def git_commit() -> None:
        """Run `git commit` with the message in the target directory."""
        subprocess.run(
            args=["git", "commit", "-m", f"{message}"],
            cwd=str(directory),
            check=True,
        )

    if preview:
        click.echo(f"Proposed commit message:\n\n{message}")
        if click.confirm("Create this commit?"):
            git_commit()
    else:
        git_commit()


def has_stage_changes(directory: pathlib.Path) -> bool:
    """Return whether the repository has staged changes.

    Args:
        directory: Directory of the Git repository to check.

    Returns:
        True if there are staged changes.

    Raises:
        NoGitRepoError: If the directory is not inside a Git repository.
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        text=True,
        capture_output=True,
        cwd=str(directory),
    )
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    raise NoGitRepoError(directory=directory)
