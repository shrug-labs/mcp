from unittest.mock import MagicMock, create_autospec, patch

import oci
import pytest
from fastmcp import Client
from oracle.oci_networking_mcp_server.server import mcp


class TestNetworkingTools:
    @pytest.mark.asyncio
    @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    async def test_list_vcns(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_list_response = create_autospec(oci.response.Response)
        mock_list_response.data = [
            oci.core.models.Vcn(
                id="vcn1", display_name="VCN 1", lifecycle_state="AVAILABLE"
            )
        ]
        mock_client.list_vcns.return_value = mock_list_response

        async with Client(mcp) as client:
            result = (
                await client.call_tool(
                    "list_vcns",
                    {
                        "compartment_id": "compartment1",
                    },
                )
            ).structured_content["result"]

            assert len(result) == 1
            assert result[0]["vcn_id"] == "vcn1"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    # async def test_get_vcn(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_get_response = create_autospec(oci.response.Response)
    #    mock_get_response.data = oci.core.models.Vcn(
    #        id="vcn1", display_name="VCN 1", lifecycle_state="AVAILABLE"
    #    )
    #    mock_client.get_vcn.return_value = mock_get_response

    #    async with Client(mcp) as client:
    #        result = await client.call_tool(
    #            "get_vcn",
    #            {
    #                "vcn_id": "vcn1",
    #            },
    #        ).data

    #        assert result.id == "vcn1"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    # async def test_create_vcn(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_create_response = create_autospec(oci.response.Response)
    #    mock_create_response.data = oci.core.models.Vcn(
    #        id="vcn1", display_name="VCN 1", lifecycle_state="PROVISIONING"
    #    )
    #    mock_client.create_vcn.return_value = mock_create_response

    #    async with Client(mcp) as client:
    #        result = (
    #            await client.call_tool(
    #                "create_vcn",
    #                {
    #                    "compartment_id": "compartment1",
    #                    "cidr_block": "10.0.0.0/16",
    #                    "display_name": "VCN 1",
    #                },
    #            )
    #        ).data

    #        assert result.id == "vcn1"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    # async def test_delete_vcn(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_delete_response = create_autospec(oci.response.Response)
    #    mock_delete_response.data = MagicMock()
    #    mock_client.delete_vcn.return_value = mock_delete_response

    #    async with Client(mcp) as client:
    #        result = (
    #            await client.call_tool(
    #                "delete_vcn",
    #                {
    #                    "vcn_id": "vcn1",
    #                },
    #            )
    #        ).data

    #        assert result is not None

    # @pytest.mark.asyncio
    # @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    # async def test_create_subnet(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_create_response = create_autospec(oci.response.Response)
    #    mock_create_response.data = oci.core.models.Subnet(
    #        id="subnet1", display_name="Subnet 1", lifecycle_state="PROVISIONING"
    #    )
    #    mock_client.create_subnet.return_value = mock_create_response

    #    async with Client(mcp) as client:
    #        result = (
    #            await client.call_tool(
    #                "create_subnet",
    #                {
    #                    "vcn_id": "vcn1",
    #                    "compartment_id": "compartment1",
    #                    "cidr_block": "10.0.1.0/24",
    #                    "display_name": "Subnet 1",
    #                },
    #            )
    #        ).data

    #        assert result.id == "subnet1"

    @pytest.mark.asyncio
    @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    async def test_list_subnets(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_list_response = create_autospec(oci.response.Response)
        mock_list_response.data = [
            oci.core.models.Subnet(
                id="subnet1",
                vcn_id="vcn1",
                display_name="Subnet 1",
                lifecycle_state="AVAILABLE",
            )
        ]
        mock_client.list_subnets.return_value = mock_list_response

        async with Client(mcp) as client:
            result = (
                await client.call_tool(
                    "list_subnets",
                    {
                        "compartment_id": "compartment1",
                        "vcn_id": "vcn1",
                    },
                )
            ).structured_content["result"]

            assert len(result) == 1
            assert result[0]["subnet_id"] == "subnet1"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_networking_mcp_server.server.get_networking_client")
    # async def test_get_subnet(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_get_response = create_autospec(oci.response.Response)
    #    mock_get_response.data = oci.core.models.Subnet(
    #        id="subnet1",
    #        vcn_id="vcn1",
    #        display_name="Subnet 1",
    #        lifecycle_state="AVAILABLE",
    #    )
    #    mock_client.get_subnet.return_value = mock_get_response

    #    async with Client(mcp) as client:
    #        result = (
    #            await client.call_tool(
    #                "get_subnet",
    #                {
    #                    "subnet_id": "subnet1",
    #                },
    #            )
    #        ).data

    #        assert result.id == "subnet1"
