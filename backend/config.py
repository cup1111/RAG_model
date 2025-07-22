from __future__ import annotations

"""Global configuration and environment loading.

This module is imported for its side-effects: it loads the .env file
and validates that the required OPENAI_API_KEY is present so the rest
of the application can safely rely on it being set.
"""

import os
from dotenv import load_dotenv

# Load variables from .env if present (does nothing if file is absent)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable not set. Please configure it in .env or export it directly!"
    ) 