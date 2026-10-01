# Setup Guide

## Prerequisites

- Python 3.13+
- Azure CLI
- An Anthropic API key
- An Azure subscription with a Log Analytics workspace that has Microsoft Sentinel enabled

## 1. Install dependencies

```bash
git clone https://github.com/ronankongala/agentic-soc-sentinel.git
cd agentic-soc-sentinel
pip install anthropic azure-identity azure-monitor-query pandas
```

## 2. Create `src/keys.py`

`src/keys.py` is listed in `.gitignore` and is not in the repo. `executor.py` imports two values from it:

```python
ANTHROPIC_API_KEY = "sk-ant-..."
LOG_ANALYTICS_WORKSPACE_ID = "<workspace-id>"  # the workspace's Workspace ID (a GUID)
```

## 3. Sign in to Azure

```bash
az login
```

The agent authenticates to Log Analytics with `DefaultAzureCredential`, which picks up the Azure CLI login. The signed-in account needs read access to the workspace.

## 4. Run the agent

Run from the repository root, since `main.py` adds `src` to the import path:

```bash
py src/main.py        # or: python src/main.py
```

The agent asks what to investigate, shows the table, fields and time range Claude chose, validates them against the guardrails in `src/guardrails.py`, then prints and runs the KQL query. Before the threat hunt it asks for a model; press Enter to keep the default (`claude-haiku-4-5-20251001`) or type `claude-sonnet-4-6`. Any other value is rejected.

## Notes

- Queries are limited to the tables and fields in `ALLOWED_TABLES` (`AzureActivity`, `SigninLogs`, `SecurityEvent`, `AuditLogs`) and to a 168-hour (7-day) lookback. A guardrail violation exits the program.
- If the query returns no rows or fails, the agent falls back to the 8 sample `AzureActivity` records in `src/sample_data.py` and says so in the output. A new workspace with no ingested activity will hit this path.
