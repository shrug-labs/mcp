from datetime import datetime
from unittest.mock import patch

import pytest
from fastmcp import Client
from oracle.datetime_helper_mcp_server.server import mcp


class TestDatetimeHelperTools:
    @pytest.mark.asyncio
    @patch("oracle.datetime_helper_mcp_server.server.datetime")
    async def test_get_current_datetime(self, mock_datetime):
        async with Client(mcp) as client:
            now = datetime(1970, 1, 1, 0, 0, 0)
            mock_datetime.now.return_value = now
            result = (await client.call_tool("get_current_datetime", {})).data
            assert "current_datetime" in result
            assert result["current_datetime"] == now.isoformat()
            assert isinstance(result["current_datetime"], str)

    @pytest.mark.asyncio
    async def test_get_current_datetime_format(self):
        async with Client(mcp) as client:
            result = (await client.call_tool("get_current_datetime", {})).data
            assert "current_datetime" in result
            assert isinstance(result["current_datetime"], str)
            try:
                datetime.fromisoformat(result["current_datetime"])
            except ValueError:
                pytest.fail("current_datetime is not in ISO format")
