from opencode import Opencode


def generate_commit(opencode_binary: str, preview: bool = False) -> None:
    with Opencode(opencode_binary=opencode_binary) as oc:
        oc.ask("TODO")
        if preview:
            pass
        pass
