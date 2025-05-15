from google.adk.agents import LlmAgent
from google.adk.tools import google_search, FunctionTool
import requests

from multi_tool_agent.beckn_tools.confirm.beckn_confirm import BecknConfirm
from multi_tool_agent.beckn_tools.search.beckn_search import SearchBecknInput

from world_engine_tools.meter.meter import Meter

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

get_meter_data_tool = FunctionTool(
    func = Meter.get_meter_history,
)

analyze_meter_data_tool = FunctionTool(
    func=Meter.analyze_meter_data,
)

get_current_meter_status_tool = FunctionTool(
    func=Meter.get_meter_status,
)

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

    The usermay also ask for meter history and analysis its your job to get the meter data and analyze it.
    If the user asks for a weekly report, use the generate_weekly_report tool.
    If the user asks for a monthly quota, use the set_quota_tool to set it.
    """,

    global_instruction="""
    Your job is to walk the user through the complete Beckn DFP onboarding flow:
    First, use the Beckn search tool to list available programs.
    Then ask the user which one to choose. Once selected, confirm the program using the confirmation tool.
    Make the conversation feel natural by asking questions to fill any missing fields.

    The usermay also ask for meter history and analysis its your job to get the meter data and analyze it.
    If the user asks for a weekly report, use the generate_weekly_report tool.
    If the user asks for a monthly quota, use the set_quota_tool to set it.
    """,
    # context=context_data,
    tools=[
        set_quota_tool,
        get_quota_tool,

        search_beckn_tool,
        confirm_program_tool,
        get_meter_data_tool,
        analyze_meter_data_tool,
        get_current_meter_status_tool
    ],
)
