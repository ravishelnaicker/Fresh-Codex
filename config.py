"""
Configuration values for the Fresh-Codex example.

The OpenAI API key, environment size, and maximum allowed steps are
defined directly in code for simplicity.  These values can be edited
as needed without relying on environment variables.
"""

# Hard-coded OpenAI API key (replace with a real key as needed)
OPENAI_API_KEY = "replace-with-your-openai-key"

# Category of the environment size used by the application.
# Valid options: "tiny", "small", "medium", "large-gen".
ENVIRONMENT_SIZE = "small"

# Maximum number of steps the environment will execute
MAX_STEPS = 100
