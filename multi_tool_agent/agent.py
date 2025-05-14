from google.adk.agents import LlmAgent
from google.adk.tools import google_search, FunctionTool
import requests

from multi_tool_agent.beckn_tools.confirm.beckn_confirm import BecknConfirm
from multi_tool_agent.beckn_tools.search.beckn_search import SearchBecknInput
from multi_tool_agent.context.set_context import setAgentContext

# -------------------------------
# Tool 1: Set Monthly Energy Quota
# -------------------------------
user_quota = {}

def set_monthly_quota(kwh: float) -> dict:
    user_quota["limit"] = kwh
    return {"status": "success", "message": f"Monthly quota set to {kwh} kWh"}

set_quota_tool = FunctionTool(
    func=set_monthly_quota
)

def get_monthly_quota() -> dict:
    if "limit" in user_quota:
        return {"status": "success", "quota": user_quota["limit"]}
    else:
        return {"status": "error", "message": "No quota set"}

get_quota_tool = FunctionTool(
    func=get_monthly_quota
)
# -------------------------------
# Tool 2: Fetch Real-World Grid Events (World Engine)
# -------------------------------

def get_grid_load() -> dict:
    try:
        response = requests.get("https://world-engine.api.com/grid-load")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
grid_event_tool = FunctionTool(func=get_grid_load)

def generate_weekly_report(llm_agent=None) -> dict:
    try:
        response = requests.get("<your-world-engine-url>/meter-datasets/1361")
        if response.status_code != 200:
            return {"status": "error", "message": "Failed to fetch meter data"}

        meter_data = response.json()
        readings = meter_data.get("readings", [])
        if not readings:
            return {"status": "error", "message": "No readings found in meter data"}

        total_kwh_used = sum(entry["kwh"] for entry in readings)
        num_days = len(readings)
        avg_daily_usage = total_kwh_used / num_days if num_days else 0

        # Construct summary for the model to reason on
        summary = (
            f"This week's total consumption: {total_kwh_used:.2f} kWh.\n"
            f"Average daily usage: {avg_daily_usage:.2f} kWh.\n"
        )

        # Ask the model for recommendation
        if llm_agent is None:
            recommendation = "Model not provided"
        else:
            prompt = (
                f"{summary}\n"
                "Based on this data, what should the user do this week to optimize energy usage or contribute to the grid? "
                "Be concise and action-oriented."
            )
            response = llm_agent.chat(prompt)
            recommendation = response.text if hasattr(response, "text") else response

        return {
            "status": "success",
            "summary": {
                "total_consumption": f"{total_kwh_used:.2f} kWh",
                "average_daily_usage": f"{avg_daily_usage:.2f} kWh",
                "recommendation": recommendation,
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
weekly_report_tool = FunctionTool(func=lambda: generate_weekly_report(llm_agent=root_agent))


def get_grid_load() -> dict:
    try:
        response = requests.get("https://world-engine.api.com/grid-load")
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
grid_event_tool = FunctionTool(func=get_grid_load)


def get_substations() -> dict:
    try:
        response = requests.get("https://world-engine.api.com/utilities/substations")
        response.raise_for_status()
        return {"status": "success", "substations": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
get_substations_tool = FunctionTool(func=get_substations)

def get_transformers() -> dict:
    try:
        response = requests.get("https://world-engine.api.com/utilities/transformers")
        response.raise_for_status()
        return {"status": "success", "transformers": response.json()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
get_transformers_tool = FunctionTool(func=get_transformers)


confirm_program_tool = FunctionTool(
    func=BecknConfirm.confirm_program,
)

search_beckn_tool = FunctionTool(
    func=SearchBecknInput.search_beckn,
)
    


root_agent = LlmAgent(
    name="personalised_energy_assistant",
    description="Agent that helps manage energy use, savings, and device onboarding.",
    model="gemini-2.0-flash",
    instruction="""
    You help users discover and confirm energy-saving programs using the Beckn protocol.
    After performing a Beckn search, always ask the user which program they would like to confirm.
    If they give a name or ID, use the confirmation tool.
    Prompt for user info if not already provided.
    """,

    global_instruction="""
    Your job is to walk the user through the complete Beckn DFP onboarding flow:
    First, use the Beckn search tool to list available programs.
    Then ask the user which one to choose. Once selected, confirm the program using the confirmation tool.
    Make the conversation feel natural by asking questions to fill any missing fields.
    """,
    # context=context_data,
    tools=[
        # set_quota_tool,
        # get_quota_tool,
        # grid_event_tool,
        # get_substations_tool,
        # get_transformers_tool,
     
        # weekly_report_tool,
        search_beckn_tool,
        confirm_program_tool,
    ],
)
