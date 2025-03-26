import os
import time
from typing import Any
import uuid

import requests

from bandwidth_mock.commands import get_message_payload_creators


BASE_URL = "http://localhost:5555/api"
DELAY_SECONDS = 1


def send_callback(url: str, callback_payload: list[dict[str, Any]]):
    requests.post(url, json=callback_payload)


def mock_messages_response(request: dict) -> tuple[dict, str]:
    lead_number = request["to"][0]
    agent_number = request["from"]
    message = request["text"]
    callback_payload_creators = get_message_payload_creators(message)
    message_id = uuid.uuid4().hex

    for creator in callback_payload_creators:
        send_callback(
            os.path.join(BASE_URL, creator.endpoint),
            creator.create(lead_number, agent_number, message_id),
        )
        time.sleep(DELAY_SECONDS)
    return {"id": message_id}, "application/json"


def mock_tndetails(_) -> tuple[str, str]:
    xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<TelephoneNumberResponse>
  <TelephoneNumberDetails>
    <CampaignFullyProvisioned>true</CampaignFullyProvisioned>
  </TelephoneNumberDetails>
</TelephoneNumberResponse>"""
    return xml_content, "application/xml"
