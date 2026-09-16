import shutil
from typing import TypedDict


class Cli(TypedDict):
    name: str
    cmd: str


REQUIRED_CLIS: list[Cli] = [
    {"name": "Git", "cmd": "git"},
    {"name": "Opencode", "cmd": "opencode"},
]


def is_cli_installed(cli_info: Cli) -> bool:
    return bool(shutil.which(cli_info["cmd"]))


def check_required_clis() -> None:
    pass
