from typing import TypedDict, Never

class Cli(TypedDict):
    name: str
    cmd: str


REQUIRED_CLIS : list[Cli]= [
    {
        "name": "Git",
        "cmd": "git -v"
    },
    {
        "name": "Opencode",
        "cmd": "opencode -v"
    }
]



