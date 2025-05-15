class AnaylyseMeterUse:
    
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