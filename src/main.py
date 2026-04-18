# ============================================
# main.py - Agentic SOC Analyst Entry Point
# ============================================

import sys
import time
sys.path.append("src")

from executor import (
    get_query_context,
    sanitize_query_context,
    display_query_context,
    build_kql_query,
    query_log_analytics,
    process_log_results,
    execute_threat_hunt,
    display_threats
)
from guardrails import (
    validate_table_and_fields,
    validate_model,
    validate_time_range
)
from model_management import DEFAULT_MODEL


def main():
    print("="*50)
    print("🛡️  AGENTIC SOC ANALYST")
    print("Powered by Claude AI + Microsoft Sentinel")
    print("="*50)

    # ---- Step 1: Get user input ----
    print("\nSOC Analyst at your service.")
    user_message = input("What would you like to investigate?\n> ")

    if not user_message.strip():
        print("No input provided. Exiting.")
        sys.exit(0)

    # ---- Step 2: Get query context from Claude ----
    query_context = get_query_context(user_message)

    if not query_context:
        print("Failed to derive query context. Exiting.")
        sys.exit(1)

    # Sanitize query context
    query_context = sanitize_query_context(query_context)

    # Display what Claude decided
    display_query_context(query_context)

    # ---- Step 3: Validate against guardrails ----
    validate_table_and_fields(
        query_context["table_name"],
        query_context["fields"]
    )

    validate_time_range(query_context["time_range_hours"])

    # ---- Step 4: Build and run KQL query ----
    kql_query = build_kql_query(query_context)
    print(f"\n📊 KQL Query:\n{kql_query}")

    table_results = query_log_analytics(
        kql_query,
        query_context["time_range_hours"]
    )

    # ---- Step 5: Process logs ----
    log_data, record_count = process_log_results(table_results)

    # Fallback to sample data if no live data
    if not log_data:
        print("\n⚠️  No live Sentinel data found.")
        print("📂 Loading sample data for demonstration...")
        from sample_data import SAMPLE_AZURE_ACTIVITY_LOGS
        log_data = SAMPLE_AZURE_ACTIVITY_LOGS
        record_count = 8
        print(f"✅ Loaded {record_count} sample records.")
    else:
        print(f"\n✅ {record_count} records returned from Sentinel.")

    # ---- Step 6: Select model ----
    print(f"\n🤖 Default model: {DEFAULT_MODEL}")
    model_choice = input(
        "Press Enter to continue or type a different model name: "
    ).strip()

    model = model_choice if model_choice else DEFAULT_MODEL
    validate_model(model)

    # ---- Step 7: Execute threat hunt ----
    print("\n🔍 Starting threat hunt...")
    start_time = time.time()

    threats = execute_threat_hunt(
        user_message,
        query_context["table_name"],
        log_data,
        model
    )

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    print(f"\n⏱️  Hunt completed in {duration} seconds.")
    print(f"Found {len(threats)} potential threat(s).")

    input("\nPress Enter to see results...")

    # ---- Step 8: Display threats ----
    display_threats(threats)

    print("\n" + "="*50)
    print("✅ Investigation complete.")
    print("="*50)


if __name__ == "__main__":
    main()