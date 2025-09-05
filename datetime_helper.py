import datetime

from fastmcp import FastMCP

mcp = FastMCP("datetime_helper")


@mcp.tool
def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return {"current_datetime": current_datetime.isoformat()}


if __name__ == "__main__":
    mcp.run()
