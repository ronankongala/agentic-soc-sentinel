# ============================================
# executor.py - Core Agent Functions
# ============================================

import json
from datetime import timedelta
import anthropic
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from keys import (
    ANTHROPIC_API_KEY,
    LOG_ANALYTICS_WORKSPACE_ID
)
from prompt_management import (
    SYSTEM_PROMPT_TOOL_SELECTION,
    TOOLS,
    build_threat_hunt_prompt,
    SYSTEM_PROMPT_THREAT_HUNT
)
from model_management import DEFAULT_MODEL, MAX_OUTPUT_TOKENS


# ---- Initialize Clients ----
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
azure_credential = DefaultAzureCredential()
logs_client = LogsQueryClient(azure_credential)


def get_query_context(user_message, model=DEFAULT_MODEL):
    """
    Claude Call #1
    Takes user natural language and returns structured
    query context using Claude tools
    """
    print("\n🔍 Analyzing your request...")

    response = anthropic_client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT_TOOL_SELECTION,
        messages=[
            {"role": "user", "content": user_message}
        ],
        tools=TOOLS,
        tool_choice={"type": "any"}
    )

    # Extract tool use response
    for block in response.content:
        if block.type == "tool_use":
            return block.input

    return None


def sanitize_query_context(query_context):
    """Ensure all fields exist in query context"""
    defaults = {
        "table_name": "",
        "fields": "",
        "time_range_hours": 96,
        "device_name": "",
        "caller": "",
        "about_individual_user": False,
        "about_individual_host": False,
        "about_nsg": False,
        "rationale": ""
    }

    for key, value in defaults.items():
        if key not in query_context:
            query_context[key] = value

    return query_context


def display_query_context(query_context):
    """Display the query context to user"""
    print("\n" + "="*50)
    print("📋 LOG SEARCH PARAMETERS FINALIZED")
    print("="*50)
    print(f"Table        : {query_context['table_name']}")
    print(f"Fields       : {query_context['fields']}")
    print(f"Time Range   : {query_context['time_range_hours']} hours")
    print(f"Device       : {query_context['device_name'] or 'All'}")
    print(f"Caller       : {query_context['caller'] or 'All'}")
    print(f"User Query   : {query_context['about_individual_user']}")
    print(f"Host Query   : {query_context['about_individual_host']}")
    print(f"NSG Query    : {query_context['about_nsg']}")
    print("="*50)
    print(f"\n📝 Rationale: {query_context['rationale']}")


def build_kql_query(query_context):
    """Build KQL query from query context"""
    table = query_context["table_name"]
    fields = query_context["fields"]
    hours = query_context["time_range_hours"]
    device = query_context["device_name"]
    caller = query_context["caller"]

    # Base query
    query = f"{table}\n"
    query += f"| where TimeGenerated >= ago({hours}h)\n"

    # Add filters if specific targets mentioned
    if device:
        query += f'| where Computer contains "{device}" '
        query += f'or WorkstationName contains "{device}"\n'

    if caller:
        query += f'| where Caller contains "{caller}" '
        query += f'or UserPrincipalName contains "{caller}"\n'

    # Project only needed fields
    query += f"| project {fields}\n"
    query += "| order by TimeGenerated desc"

    return query


def query_log_analytics(query, time_range_hours):
    """Query Azure Log Analytics workspace"""
    print("\n⚡ Querying Azure Sentinel logs...")

    try:
        response = logs_client.query_workspace(
            workspace_id=LOG_ANALYTICS_WORKSPACE_ID,
            query=query,
            timespan=timedelta(hours=time_range_hours)
        )

        if response.status == LogsQueryStatus.SUCCESS:
            table = response.tables[0]
            if not table.rows:
                print("⚠️  No live data found. Using sample data for demonstration.")
                return None
            return table
        else:
            print(f"Query error: {response.partial_error}")
            return None

    except Exception as e:
        print(f"Log Analytics error: {e}")
        return None


def process_log_results(table):
    """Convert log results to string for Claude"""
    if not table or not table.rows:
        return None, 0

    columns = [col.name for col in table.columns]
    records = []

    for row in table.rows:
        record = dict(zip(columns, row))
        records.append(str(record))

    log_string = "\n".join(records)
    record_count = len(table.rows)

    return log_string, record_count


def execute_threat_hunt(user_message, table_name, log_data, model=DEFAULT_MODEL):
    """
    Claude Call #2
    Execute the actual threat hunt using Claude
    """
    print("\n🎯 Executing threat hunt...")

    # Build the full prompt
    user_prompt = build_threat_hunt_prompt(user_message, table_name, log_data)

    response = anthropic_client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=SYSTEM_PROMPT_THREAT_HUNT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    raw_response = response.content[0].text

    # Parse JSON response
    try:
        clean = raw_response.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()

        result = json.loads(clean)
        return result.get("findings", [])

    except Exception as e:
        print(f"Response parsing error: {e}")
        return []


def display_threats(threats):
    """Display threat findings to user"""
    if not threats:
        print("\n✅ No threats found.")
        return

    print(f"\n🚨 Found {len(threats)} potential threat(s):")

    for i, threat in enumerate(threats, 1):
        print("\n" + "="*50)
        print(f"THREAT #{i}: {threat.get('title', 'Unknown')}")
        print("="*50)
        print(f"Description    : {threat.get('description', '')}")
        print(f"Confidence     : {threat.get('confidence_rating', '')}")

        miter = threat.get("miter", {})
        if miter:
            print(f"MITRE Tactic   : {miter.get('tactic', '')}")
            print(f"MITRE Technique: {miter.get('technique', '')}")

        iocs = threat.get("indicators_of_compromise", [])
        if iocs:
            print(f"IOCs           : {', '.join(iocs)}")

        recs = threat.get("recommendations", [])
        if recs:
            print(f"Recommendations: {', '.join(recs)}")

        print(f"Notes          : {threat.get('notes', '')}")