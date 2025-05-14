
import requests, json, time
class BecknConfirm:
    def confirm_program(provider_id: str, item_id: str, fulfillment_id: str, name: str, phone: str, email: str, transaction_id: str, message_id: str):
    

        url = "https://bap-ps-client-deg-team14.becknprotocol.io/confirm"
        timestamp = str(int(time.time()))

        payload = {
            "context": {
                "domain": "deg:schemes",
                "action": "confirm",
                "location": {
                    "country": {"code": "USA"},
                    "city": {"code": "NANP:628"}
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
                "order": {
                    "provider": {"id": provider_id},
                    "items": [{"id": item_id}],
                    "fulfillments": [{
                        "id": fulfillment_id,
                        "customer": {
                            "person": {"name": name},
                            "contact": {
                                "phone": phone,
                                "email": email
                            }
                        }
                    }]
                }
            }
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return {
                "status": "success",
                "message": "The program has been successfully confirmed and onboarded.",
                "response": response.json()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Confirmation failed: {str(e)}"
            }
