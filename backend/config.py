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

# ---------------------------------------------------------------------------
# Temporary compatibility patch
# ---------------------------------------------------------------------------
try:
    from openai import OpenAI  # type: ignore

    _orig_openai_init = OpenAI.__init__  # type: ignore[attr-defined]

    def _patched_openai_init(self, *args, **kwargs):  # noqa: ANN001
        kwargs.pop("proxies", None)
        return _orig_openai_init(self, *args, **kwargs)

    if _orig_openai_init is not _patched_openai_init:  # type: ignore[comparison-overlap]
        OpenAI.__init__ = _patched_openai_init  # type: ignore[method-assign]
except Exception:  # pragma: no cover
    pass 