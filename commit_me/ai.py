import pathlib

import rich_click as click
from opencode import Opencode

from commit_me.util.constants import PROMPT


def generate_commit_message(opencode_binary: str, directory: pathlib.Path) -> str:
    with Opencode(
        opencode_binary=opencode_binary,
        directory=str(directory),
    ) as oc:
        return str(oc.ask(prompt=PROMPT))
