class MeterHistory:
    def get_meter_history():
        import requests
        try:
            # url="https://world-engine-team14.becknprotocol.io/meter-data-simulator"
            url = "https://world-engine-team14.becknprotocol.io/meter-data-simulator/meter-datasets/1664"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
