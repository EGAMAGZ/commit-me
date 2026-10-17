from opencode import Opencode


def generate_commit(opencode_binary: str, _preview: bool = False) -> None:
    with Opencode(opencode_binary=opencode_binary) as _oc:
        pass
