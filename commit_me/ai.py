from opencode import Opencode


def generate_commit(opencode_binary: str, preview=False) -> None:
    with Opencode(opencode_binary=opencode_binary) as oc:
        pass
