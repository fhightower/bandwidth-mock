from dataclasses import dataclass
from typing import Any, Callable, Optional
import uuid


STATUS_CALLBACK_ENDPOINT = "text_messages/status_callback/"
INBOUND_CALLBACK_ENDPOINT = "text_messages/inbound/"

CallbackPayloadCreatorResponse = list[dict[str, Any]]


@dataclass
class CallbackPayloadCreator:
    create: Callable[[str, str, str, str], CallbackPayloadCreatorResponse]
    endpoint: str


def _create_error_payload(
    lead_number: str, agent_number: str, message_id: str, *_
) -> CallbackPayloadCreatorResponse:
    return [
        {
            "time": "2024-02-15T16:34:52.255182Z",
            "type": "message-failed",
            "to": lead_number,
            "description": "foo-bar",
            "message": {
                "id": message_id,
                "owner": agent_number,
                "applicationId": "...",
                "time": "2024-02-15T16:34:51.007000Z",
                "segmentCount": 1,
                "direction": "out",
                "to": [lead_number],
                "from": agent_number,
                "text": "",
                "tag": "",
            },
        }
    ]


create_error_payload = CallbackPayloadCreator(
    create=_create_error_payload,
    endpoint=STATUS_CALLBACK_ENDPOINT,
)


def _create_success_payload(
    lead_number: str, agent_number: str, message_id: str, *_
) -> CallbackPayloadCreatorResponse:
    return [
        {
            "time": "2024-02-15T16:34:52.255182Z",
            "type": "message-delivered",
            "to": lead_number,
            "description": "foo-bar",
            "message": {
                "id": message_id,
                "owner": agent_number,
                "applicationId": "...",
                "time": "",
                "segmentCount": 1,
                "direction": "out",
                "to": [lead_number],
                "from": agent_number,
                "text": "",
                "tag": "",
            },
        }
    ]


create_success_payload = CallbackPayloadCreator(
    create=_create_success_payload,
    endpoint=STATUS_CALLBACK_ENDPOINT,
)


def _create_inbound_payload(
    lead_number: str,
    agent_number: str,
    message_body_updates: Optional[dict[str, Any]] = None,
) -> CallbackPayloadCreatorResponse:
    if not message_body_updates:
        message_body_updates = {}

    message_body = {
        "id": uuid.uuid4().hex,
        "time": "",
        "to": [agent_number],
        "from": lead_number,
        "text": "Hi!",
        "media": [],
        "applicationId": "",
        "owner": lead_number,
        "direction": "in",
        "segmentCount": 1,
    }

    message_body.update(message_body_updates)

    return [
        {
            "type": "message-received",
            "time": "",
            "description": "Incoming message received",
            "to": agent_number,
            "message": message_body,
        }
    ]


def _create_inbound_text_only_payload(
    lead_number: str, agent_number: str, *_
) -> CallbackPayloadCreatorResponse:
    return _create_inbound_payload(lead_number, agent_number)


create_inbound_payload = CallbackPayloadCreator(
    create=_create_inbound_text_only_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)


def _create_inbound_echo_payload(
    lead_number: str, agent_number: str, _: str, message: str
) -> CallbackPayloadCreatorResponse:
    message_to_echo = message[len("echo:") :].strip()
    return _create_inbound_payload(lead_number, agent_number, {"text": message_to_echo})


create_echo_payload = CallbackPayloadCreator(
    create=_create_inbound_echo_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)


def _create_help_payload(
    lead_number: str, agent_number: str, *_
) -> CallbackPayloadCreatorResponse:
    from bandwidth_mock.commands import COMMAND_PROCESSOR_MAP

    message = "Available commands: " + ", ".join(
        k for k in COMMAND_PROCESSOR_MAP.keys() if k != "_default"
    )
    return _create_inbound_payload(lead_number, agent_number, {"text": message})


create_help_payload = CallbackPayloadCreator(
    create=_create_help_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)


def _create_media_only_payload(
    lead_number: str, agent_number: str, *_
) -> CallbackPayloadCreatorResponse:
    message_body = {
        "media": [
            "https://dev.bandwidth.com/img/dev-docs-logo.svg",
        ],
        "text": "",
    }

    return _create_inbound_payload(lead_number, agent_number, message_body)


create_media_only_payload = CallbackPayloadCreator(
    create=_create_media_only_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)


def _create_media_and_text_payload(
    lead_number: str, agent_number: str, *_
) -> CallbackPayloadCreatorResponse:
    message_body = {
        "media": [
            "https://dev.bandwidth.com/img/dev-docs-logo.svg",
        ],
        "text": "Message w/ media",
    }
    return _create_inbound_payload(lead_number, agent_number, message_body)


create_media_and_text_payload = CallbackPayloadCreator(
    create=_create_media_and_text_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)


def _create_multiple_recipients_payload(
    lead_number: str, agent_number: str, *_
) -> CallbackPayloadCreatorResponse:
    message_body = {
        "text": "Message sent to multiple recipients",
        "to": [agent_number, "1234567890"],
    }
    return _create_inbound_payload(lead_number, agent_number, message_body)


create_multiple_recipients_payload = CallbackPayloadCreator(
    create=_create_multiple_recipients_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)
