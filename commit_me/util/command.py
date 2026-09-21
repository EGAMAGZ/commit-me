"""Utilities for detecting required command-line tools."""

import shutil
from typing import TypedDict

from commit_me.exceptions import MissingCliError


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


def check_required_clis() -> None:
    """Raise MissingCliError if any required CLI is not installed."""
    missing_clis = [cli["name"] for cli in REQUIRED_CLIS if not is_cli_installed(cli)]
    if missing_clis:
        raise MissingCliError(missing_clis)
