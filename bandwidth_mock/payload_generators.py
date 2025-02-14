from dataclasses import dataclass
from typing import Any, Callable
import uuid


STATUS_CALLBACK_ENDPOINT = "text_messages/status_callback/"
INBOUND_CALLBACK_ENDPOINT = "text_messages/inbound/"

CallbackPayloadCreatorResponse = list[dict[str, Any]]


@dataclass
class CallbackPayloadCreator:
    create: Callable[[str, str, str], CallbackPayloadCreatorResponse]
    endpoint: str


def _create_error_payload(
    lead_number: str, agent_number: str, message_id: str
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
    lead_number: str, agent_number: str, message_id: str
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
    lead_number: str, agent_number: str, *_
) -> CallbackPayloadCreatorResponse:
    return [
        {
            "type": "message-received",
            "time": "",
            "description": "Incoming message received",
            "to": agent_number,
            "message": {
                "id": uuid.uuid4().hex,
                "time": "",
                "to": [agent_number],
                "from": lead_number,
                "text": "Hi!",
                "applicationId": "",
                "owner": lead_number,
                "direction": "in",
                "segmentCount": 1,
            },
        }
    ]


create_inbound_payload = CallbackPayloadCreator(
    create=_create_inbound_payload,
    endpoint=INBOUND_CALLBACK_ENDPOINT,
)
