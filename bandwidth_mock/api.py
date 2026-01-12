import asyncio
import os
from typing import Any
import uuid

from fastapi import BackgroundTasks, FastAPI
from fastapi import Response
import requests

from bandwidth_mock.commands import get_message_payload_creators


app = FastAPI()

BASE_URL = "http://localhost:5555/api"
DELAY_SECONDS = 1


async def send_callback(url: str, callback_payload: list[dict[str, Any]]):
    await asyncio.sleep(DELAY_SECONDS)
    requests.post(url, json=callback_payload)


@app.post("/messages")
def mock_messages_response(request: dict, background_tasks: BackgroundTasks):
    lead_number = request["to"][0]
    agent_number = request["from"]
    message = request["text"]
    callback_payload_creators = get_message_payload_creators(message)
    message_id = uuid.uuid4().hex

    for creator in callback_payload_creators:
        background_tasks.add_task(
            send_callback,
            os.path.join(BASE_URL, creator.endpoint),
            creator.create(lead_number, agent_number, message_id, message),
        )

    return {"id": message_id}


@app.get("/tndetails", response_class=Response)
def mock_tndetails():
    xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<TelephoneNumberResponse>
  <TelephoneNumberDetails>
    <CampaignFullyProvisioned>true</CampaignFullyProvisioned>
  </TelephoneNumberDetails>
</TelephoneNumberResponse>"""
    return Response(content=xml_content, media_type="application/xml")
