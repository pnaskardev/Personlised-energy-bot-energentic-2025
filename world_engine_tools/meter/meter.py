import requests

class Meter:
    def get_meter_history():
        try:
            # url="https://world-engine-team14.becknprotocol.io/meter-data-simulator"
            url = "https://world-engine-team14.becknprotocol.io/meter-data-simulator/meter-datasets/1745"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    
    def analyze_meter_data(meter_data: list) -> dict:
        """
        Analyzes meter data and returns raw insights for the agent to interpret.
        """
        insights = {
            "high_voltage_events": 0,
            "low_power_factor_events": 0,
            "total_consumption_kwh": 0,
            "data_points": len(meter_data),
        }

        for reading in meter_data:
            voltage = reading.get("avgVoltage", 0)
            pf = reading.get("powerFactor", 1)
            kwh = reading.get("consumptionKWh", 0)

            if voltage > 240:
                insights["high_voltage_events"] += 1
            if pf < 0.9:
                insights["low_power_factor_events"] += 1
            insights["total_consumption_kwh"] += kwh

        return insights
    
    def get_meter_status() -> dict:
        """
        Fetches and returns the meter status for a given meter ID.

        Args:
            meter_id (int): The ID of the meter to fetch.

        Returns:
            dict: The raw meter data for the agent to analyze.
        """
        url = f"https://world-engine-team14.becknprotocol.io/meter-data-simulator/meters/{1745}?populate[0]=parent&populate[1]=children"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

