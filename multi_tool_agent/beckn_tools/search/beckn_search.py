from typing import Annotated
from pydantic import BaseModel, Field


class SearchBecknInput(BaseModel):
    domain: Annotated[str, Field(description="The domain to search in. Usually 'deg:schemes'.")]
    item_name: Annotated[str, Field(description="The name of the item to search for, like 'Program' or 'Device'.")]

    def search_beckn():
        import requests
        import json
        import uuid
        import time
        transaction_id = str(uuid.uuid4())
        message_id = str(uuid.uuid4())
        timestamp = str(int(time.time()))
        url = "https://bap-ps-client-deg-team14.becknprotocol.io/search"

        payload = json.dumps({
        "context": {
            "domain": "deg:schemes",
            "action": "search",
            "location": {
            "country": {
                "code": "USA"
            },
            "city": {
                "code": "NANP:628"
            }
            },
            "version": "1.1.0",
            "bap_id": "bap-ps-network-deg-team14.becknprotocol.io",
            "bap_uri": "https://bap-ps-network-deg-team14.becknprotocol.io/",
            "bpp_id": "bpp-ps-network-deg-team14.becknprotocol.io",
            "bpp_uri": "https://bpp-ps-network-deg-team14.becknprotocol.io/",
            "transaction_id": transaction_id,
            "message_id": message_id,
            "timestamp": timestamp
        },
        "message": {
            "intent": {
            "item": {
                "descriptor": {
                "name": "Program"
                }
            }
            }
        }
        })
        headers = {
        'Content-Type': 'application/json'
        }

        try:
            # response = requests.request("POST", url, headers=headers, data=payload)

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload,
                # timeout=10
            )
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Search request failed: {str(e)}"
            }