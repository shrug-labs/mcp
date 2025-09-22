from datetime import datetime

from fastmcp import FastMCP

mcp = FastMCP(name="oracle.datetime-helper-mcp-server")


@mcp.tool
def get_current_datetime() -> dict:
    current_datetime = datetime.now()
    return {"current_datetime": current_datetime.isoformat()}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
