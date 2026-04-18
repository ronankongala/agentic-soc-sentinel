# ============================================
# sample_data.py - Sample logs for testing
# ============================================

SAMPLE_AZURE_ACTIVITY_LOGS = """
TimeGenerated: 2026-04-17 19:00:00, OperationName: Delete Virtual Machine, ActivityStatus: Succeeded, Caller: unknown.user@gmail.com, CallerIpAddress: 185.220.101.45, ResourceGroup: soc-agent-rg, Category: Administrative, Level: Critical
TimeGenerated: 2026-04-17 18:45:00, OperationName: Create Role Assignment, ActivityStatus: Succeeded, Caller: unknown.user@gmail.com, CallerIpAddress: 185.220.101.45, ResourceGroup: soc-agent-rg, Category: Administrative, Level: Critical
TimeGenerated: 2026-04-17 18:30:00, OperationName: Update Security Policy, ActivityStatus: Succeeded, Caller: kongala.r@northeastern.edu, CallerIpAddress: 129.10.0.1, ResourceGroup: soc-agent-rg, Category: Security, Level: Warning
TimeGenerated: 2026-04-17 18:00:00, OperationName: Delete Storage Account, ActivityStatus: Failed, Caller: unknown.user@gmail.com, CallerIpAddress: 185.220.101.45, ResourceGroup: soc-agent-rg, Category: Administrative, Level: Critical
TimeGenerated: 2026-04-17 17:45:00, OperationName: List Storage Account Keys, ActivityStatus: Succeeded, Caller: unknown.user@gmail.com, CallerIpAddress: 185.220.101.45, ResourceGroup: soc-agent-rg, Category: Administrative, Level: Warning
TimeGenerated: 2026-04-17 17:30:00, OperationName: Create Virtual Machine, ActivityStatus: Succeeded, Caller: kongala.r@northeastern.edu, CallerIpAddress: 129.10.0.1, ResourceGroup: soc-agent-rg, Category: Administrative, Level: Informational
TimeGenerated: 2026-04-17 17:00:00, OperationName: Delete Network Security Group, ActivityStatus: Succeeded, Caller: unknown.user@gmail.com, CallerIpAddress: 45.141.84.85, ResourceGroup: soc-agent-rg, Category: Administrative, Level: Critical
TimeGenerated: 2026-04-17 16:45:00, OperationName: Update Firewall Rules, ActivityStatus: Succeeded, Caller: unknown.user@gmail.com, CallerIpAddress: 45.141.84.85, ResourceGroup: soc-agent-rg, Category: Security, Level: Critical
"""