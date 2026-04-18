# ============================================
# model_management.py - Model Configuration
# ============================================

# Default model to use
DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Available models with their properties
MODELS = {
    "claude-haiku-4-5-20251001": {
        "max_input_tokens": 200000,
        "max_output_tokens": 4096,
        "input_cost_per_million": 0.80,
        "output_cost_per_million": 4.00,
        "description": "Fast and cheap - good for most tasks"
    },
    "claude-sonnet-4-6": {
        "max_input_tokens": 200000,
        "max_output_tokens": 8096,
        "input_cost_per_million": 3.00,
        "output_cost_per_million": 15.00,
        "description": "Balanced - better reasoning"
    }
}

# Current tier for rate limiting
CURRENT_TIER = 1

# Max output tokens to control cost
MAX_OUTPUT_TOKENS = 4096