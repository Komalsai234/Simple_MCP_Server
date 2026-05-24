import os
import functools
import logging
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mcp-server")

mcp = FastMCP(
    "my-server",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
)

def log_tool(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_args = ", ".join(
            [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        logger.info(f"TOOL CALLED: {func.__name__}({call_args})")
        try:
            result = func(*args, **kwargs)
            logger.info(f"TOOL RESULT: {func.__name__} -> {result!r}")
            return result
        except Exception as e:
            logger.exception(f"TOOL ERROR: {func.__name__} -> {e}")
            raise
    return wrapper

@mcp.tool()
@log_tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
@log_tool
def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting MCP server on {mcp.settings.host}:{mcp.settings.port}")
    mcp.run(transport="streamable-http")
