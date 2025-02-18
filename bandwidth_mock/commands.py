from bandwidth_mock.payload_generators import (
    create_error_payload,
    create_inbound_payload,
    create_success_payload,
    create_media_only_payload,
    create_media_and_text_payload,
    create_multiple_recipients_payload,
    CallbackPayloadCreator,
)

CallbackPayloadCreators = list[CallbackPayloadCreator]


DEFAULT_KEY = "_default"

COMMAND_PROCESSOR_MAP: dict[str, CallbackPayloadCreators] = {
    "fail": [create_error_payload],
    "in:med-txt": [
        create_success_payload,
        create_media_and_text_payload,
    ],  # Media (mms) with text
    "in:med": [create_success_payload, create_media_only_payload],  # Media (mms)
    "in:mult": [
        create_success_payload,
        create_multiple_recipients_payload,
    ],  # Multiple recipients
    "in": [create_success_payload, create_inbound_payload],
    DEFAULT_KEY: [create_success_payload],
}


def get_message_payload_creators(message: str) -> CallbackPayloadCreators:
    cleaned_message = message.strip().lower()
    for command, processor in COMMAND_PROCESSOR_MAP.items():
        if cleaned_message.startswith(command):
            return processor
    return COMMAND_PROCESSOR_MAP[DEFAULT_KEY]
