from __future__ import annotations

"""Application entrypoint.

This module wires the FastAPI application together, adds CORS middleware
and includes the API routes defined in `routes.py`.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure environment variables are loaded early in the process
import config  # noqa: F401  pylint: disable=unused-import

from routes import router

app = FastAPI()

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
app.include_router(router)

# ---------------------------------------------------------------------------
# Debug Entry Point (only used when `python main.py`)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)