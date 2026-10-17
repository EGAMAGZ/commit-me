from opencode import Opencode


def generate_commit(opencode_binary: str) -> None:
    with Opencode(opencode_binary=opencode_binary) as oc:
        pass
