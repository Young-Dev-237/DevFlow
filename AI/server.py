import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("DevFlow")

API_URL = os.getenv(
    "DEVFLOW_API_URL",
    "http://127.0.0.1:8000/api",
)


@mcp.tool()
def check_backend() -> str:
    """Check whether the DevFlow backend is reachable."""
    try:
        response = httpx.get(
            f"{API_URL.rstrip('/')}/",
            timeout=5.0,
        )
        return f"Backend responded with HTTP {response.status_code}"
    except httpx.HTTPError as exc:
        return f"Backend connection failed: {exc}"


@mcp.tool()
def summarize_task(task_title: str, description: str) -> str:
    """Prepare a task summary for an AI assistant."""
    return (
        f"Task: {task_title}\n"
        f"Description: {description}\n"
        "Summarize the objective, expected result, "
        "and possible implementation steps."
    )


if __name__ == "__main__":
    mcp.run()
