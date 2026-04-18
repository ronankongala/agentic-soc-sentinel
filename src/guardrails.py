# ============================================
# guardrails.py - Safety Rules and Limits
# ============================================

import sys

# Allowed tables to query in Sentinel
ALLOWED_TABLES = {
    "AzureActivity": [
        "TimeGenerated",
        "OperationName",
        "ActivityStatus",
        "Caller",
        "CallerIpAddress",
        "ResourceGroup",
        "SubscriptionId",
        "Category",
        "Level"
    ],
    "SigninLogs": [
        "TimeGenerated",
        "UserPrincipalName",
        "AppDisplayName",
        "IPAddress",
        "Location",
        "ResultType",
        "ResultDescription",
        "RiskState",
        "ClientAppUsed"
    ],
    "SecurityEvent": [
        "TimeGenerated",
        "Account",
        "AccountType",
        "EventID",
        "Activity",
        "LogonType",
        "IpAddress",
        "WorkstationName",
        "Status"
    ],
    "AuditLogs": [
        "TimeGenerated",
        "OperationName",
        "Result",
        "InitiatedBy",
        "TargetResources",
        "Category",
        "LoggedByService"
    ]
}

# Allowed models
ALLOWED_MODELS = [
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-6"
]

# Max time range in hours
MAX_TIME_RANGE_HOURS = 168  # 7 days


def validate_table_and_fields(table, fields):
    """Validate that table and fields are allowed"""
    print("\nValidating table and fields...")

    # Check table
    if table not in ALLOWED_TABLES:
        print(f"ERROR: Table '{table}' is not in allowed list. Exiting.")
        sys.exit(1)

    # Check fields
    fields_list = [f.strip() for f in fields.split(",")]
    for field in fields_list:
        if field not in ALLOWED_TABLES[table]:
            print(f"ERROR: Field '{field}' is not allowed for table '{table}'. Exiting.")
            sys.exit(1)

    print("✅ Table and fields validated successfully.")
    return True


def validate_model(model):
    """Validate that model is allowed"""
    print("\nValidating model selection...")

    if model not in ALLOWED_MODELS:
        print(f"ERROR: Model '{model}' is not allowed. Exiting.")
        sys.exit(1)

    print(f"✅ Model '{model}' is valid.")
    return True


def validate_time_range(hours):
    """Validate time range is within limits"""
    if hours > MAX_TIME_RANGE_HOURS:
        print(f"ERROR: Time range {hours} hours exceeds maximum of {MAX_TIME_RANGE_HOURS} hours.")
        sys.exit(1)

    print(f"✅ Time range of {hours} hours is within limits.")
    return True