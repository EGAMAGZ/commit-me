"""Generate commit messages by streaming an opencode session."""

import pathlib
from collections.abc import Callable
from typing import Any, TypedDict

from opencode import Opencode
from opencode._stream_events import (
    MessagePartDeltaProps,
    MessagePartUpdatedProps,
    MessageUpdatedProps,
    SessionStatusProps,
    parse_stream_event,
)

from commit_me.util.constants import PROMPT

type Callback = Callable[[], None]
type ProgressCallback = Callable[[str], None]
type EventCallback = Callable[[dict[str, Any]], None]

Handlers = TypedDict(
    "Handlers",
    {
        "message.updated": EventCallback,
        "message.part.updated": EventCallback,
        "message.part.delta": EventCallback,
        "session.status": EventCallback,
    },
)


def make_handler(callback: EventCallback) -> EventCallback:
    """Wrap an event callback into a stream event handler.

    Args:
        callback: Callback invoked with the event properties.

    Returns:
        A handler suitable for the handlers mapping.
    """

    def handler(props: dict[str, Any]) -> None:
        callback(props)

    return handler


def generate_commit_message(
    opencode_binary: str,
    directory: pathlib.Path,
    *,
    on_start: Callback,
    on_thinking: Callback,
    on_progress: ProgressCallback,
    on_finish: Callback,
) -> str:
    """Generate a Conventional Commit message from the staged changes.

    Starts an opencode session in the given directory, streams its response,
    and assembles the assistant's text parts into a single commit message.

    Args:
        opencode_binary: Path to the opencode executable.
        directory: Directory of the Git repository to analyze.
        on_start: Called before the opencode session starts.
        on_thinking: Called once when opencode starts thinking.
        on_progress: Called with each streamed text delta.
        on_finish: Called once the message has been assembled.

    Returns:
        The generated commit message.
    """
    assistant_message_ids: set[str] = set()
    part_message_ids: dict[str, str] = {}
    part_texts: dict[str, str] = {}
    part_deltas: dict[str, list[str]] = {}
    part_order: list[str] = []

    thinking_notified = False

    def notify_thinking() -> None:
        nonlocal thinking_notified

        if not thinking_notified:
            thinking_notified = True
            on_thinking()

    def handle_message_updated(props: dict[str, Any]) -> None:
        event = MessageUpdatedProps.model_construct(**props)
        info = event.info

        if info.get("role") == "assistant":
            message_id = info.get("id")
            if message_id:
                assistant_message_ids.add(message_id)

            notify_thinking()

    def handle_part_updated(props: dict[str, Any]) -> None:
        event = MessagePartUpdatedProps.model_construct(**props)
        part = event.part

        if part.get("type") != "text":
            return

        part_id = part.get("id")
        message_id = part.get("messageID")

        if not part_id:
            return

        if part_id not in part_order:
            part_order.append(part_id)

        if message_id:
            part_message_ids[part_id] = message_id

        if "text" in part:
            part_texts[part_id] = part.get("text", "")

    def handle_part_delta(props: dict[str, Any]) -> None:
        event = MessagePartDeltaProps.model_construct(**props)

        if event.field != "text" or not event.delta:
            return

        part_id = event.partID
        part_deltas.setdefault(part_id, []).append(event.delta)

        on_progress(event.delta)

    def handle_status(props: dict[str, Any]) -> None:
        event = SessionStatusProps.model_construct(**props)
        status = event.status.get("type")

        if status == "busy":
            notify_thinking()

    handlers: Handlers = {
        "message.updated": make_handler(handle_message_updated),
        "message.part.updated": make_handler(handle_part_updated),
        "message.part.delta": make_handler(handle_part_delta),
        "session.status": make_handler(handle_status),
    }

    on_start()

    with Opencode(
        opencode_binary=opencode_binary,
        directory=str(directory),
    ) as oc:
        session = oc.create_session()
        response = oc.client.event_subscribe()

        oc.client.session_send(
            session.id,
            {"parts": [{"type": "text", "text": PROMPT}]},
        )

        for line in response.iter_lines():
            if not line.startswith("data: "):
                continue

            event = parse_stream_event(line[6:])
            props = event.properties

            if props.get("sessionID") not in (None, session.id):
                continue

            handler = handlers.get(event.type)
            if handler:
                handler(props)

            if event.type == "session.idle":
                break

            if event.type == "session.status":
                status = SessionStatusProps.model_construct(**props)
                if status.status.get("type") == "idle":
                    break
        response.close()

    result_parts: list[str] = []

    for part_id in part_order:
        if part_message_ids.get(part_id) not in assistant_message_ids:
            continue

        if part_id in part_texts:
            result_parts.append(part_texts[part_id])
        else:
            result_parts.append("".join(part_deltas.get(part_id, [])))

    on_finish()

    return "".join(result_parts).strip()
