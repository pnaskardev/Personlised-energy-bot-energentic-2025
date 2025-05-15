import requests

class GridUtilities:

    def __init__(self):
        pass

    def load_utilities()-> dict:
        url = f"https://world-engine-team14.becknprotocol.io/meter-data-simulator/utility/detailed"
        try:
            response = requests.get(url)
            
            response.raise_for_status()
            utilities_object = response.json()["utilities"][0]
            substations = utilities_object["substations"][0]
            transforms = substations["transformers"][0]
            meters = transforms["meters"][0]
            energyResource = meters["energyResource"]
            ders = energyResource["ders"]
            return utilities_object["substations"][0]
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def grid_load() -> dict:
        
        url = f"https://world-engine-team14.becknprotocol.io/meter-data-simulator/grid-loads"
        try:
            response = requests.get(url)
            print(response.data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def analyze_grid_load(grid_data: list) -> str:
        summary = []
        for entry in grid_data:
            transformer = entry["transformer"]
            substation = transformer["substation"]

            load_kw = entry.get("current_transformer_load", 0)
            capacity_kw = transformer.get("max_capacity_KW", 1)
            utilization_percent = round((load_kw / capacity_kw) * 100, 2)

            summary.append({
                "transformer_id": transformer["id"],
                "transformer_name": transformer["name"],
                "city": transformer["city"],
                "substation_name": substation["name"],
                "load_kw": load_kw,
                "capacity_kw": capacity_kw,
                "utilization_percent": utilization_percent
            })

        return summary