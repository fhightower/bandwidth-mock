import asyncio
import os
from typing import Any
import uuid

from fastapi import BackgroundTasks, FastAPI
import requests

from bandwidth_mock.commands import get_message_payload_creators


app = FastAPI()

BASE_URL = "http://localhost:5555/api"


async def send_callback(url: str, callback_payload: list[dict[str, Any]]):
    await asyncio.sleep(5)
    requests.post(url, json=callback_payload)


@app.post("/new")
def mock_outbound_reponse(request: dict, background_tasks: BackgroundTasks):
    lead_number = request["to"][0]
    agent_number = request["from"]
    message = request["text"]
    callback_payload_creators = get_message_payload_creators(message)
    message_id = uuid.uuid4().hex

    for creator in callback_payload_creators:
        background_tasks.add_task(
            send_callback,
            os.path.join(BASE_URL, creator.endpoint),
            creator.create(lead_number, agent_number, message_id),
        )

    return {"id": message_id}
