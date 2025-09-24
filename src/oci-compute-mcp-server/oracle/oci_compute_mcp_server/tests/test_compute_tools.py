from unittest.mock import MagicMock, create_autospec, patch

import oci
import pytest
from fastmcp import Client
from oracle.oci_compute_mcp_server.server import mcp


class TestComputeTools:
    @pytest.mark.asyncio
    @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    async def test_list_instances(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_list_response = create_autospec(oci.response.Response)
        mock_list_response.data = [
            oci.core.models.Instance(
                id="instance1",
                display_name="Instance 1",
                lifecycle_state="RUNNING",
                shape="VM.Standard.E2.1",
            )
        ]
        mock_list_response.has_next_page = False
        mock_list_response.next_page = None
        mock_client.list_instances.return_value = mock_list_response

        async with Client(mcp) as client:
            call_tool_result = await client.call_tool(
                "list_instances", {"compartment_id": "test_compartment"}
            )
            result = call_tool_result.structured_content["result"]

            assert len(result) == 1
            assert result[0]["id"] == "instance1"

    @pytest.mark.asyncio
    @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    async def test_launch_instance(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_launch_response = create_autospec(oci.response.Response)
        mock_launch_response.data = oci.core.models.Instance(
            id="instance1", display_name="Instance 1", lifecycle_state="PROVISIONING"
        )
        mock_client.launch_instance.return_value = mock_launch_response

        async with Client(mcp) as client:
            result = (
                await client.call_tool(
                    "launch_instance",
                    {
                        "compartment_id": "test_compartment",
                        "display_name": "test_instance",
                        "availability_domain": "AD1",
                        "image_id": "image1",
                        "subnet_id": "subnet1",
                    },
                )
            ).structured_content

            assert result["id"] == "instance1"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    # async def test_get_instance(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_get_response = create_autospec(oci.response.Response)
    #    mock_get_response.data = oci.core.models.Instance(
    #        id="instance1", display_name="Instance 1", lifecycle_state="RUNNING"
    #    )
    #    mock_client.get_instance.return_value = mock_get_response

    #    async with Client(mcp) as client:
    #        result = (await client.call_tool(
    #            "get_instance",
    #            {
    #                "instance_id": "instance1",
    #            },
    #        )).structured_content

    #        assert result['id'] == "instance1"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    # async def test_get_image(self, mock_get_client):
    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    mock_get_response = create_autospec(oci.response.Response)
    #    mock_get_response.data = oci.core.models.Image(
    #        id="image1",
    #        display_name="Image 1",
    #        operating_system="Oracle Linux",
    #        operating_system_version="8",
    #    )
    #    mock_client.get_image.return_value = mock_get_response

    #    async with Client(mcp) as client:
    #        result = (
    #            await client.call_tool(
    #                "get_image",
    #                {
    #                    "image_id": "image1",
    #                },
    #            )
    #        ).structured_content

    #        assert result.id == "image1"

    @pytest.mark.asyncio
    @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    async def test_list_images(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_list_response = create_autospec(oci.response.Response)
        mock_list_response.data = [
            oci.core.models.Image(
                id="image1",
                display_name="Image 1",
                operating_system="Oracle Linux",
                operating_system_version="8",
            )
        ]
        mock_list_response.has_next_page = False
        mock_list_response.next_page = None
        mock_client.list_images.return_value = mock_list_response

        async with Client(mcp) as client:
            result = (
                await client.call_tool(
                    "list_images",
                    {
                        "compartment_id": "test_compartment",
                    },
                )
            ).structured_content["result"]

            assert len(result) == 1
            assert result[0]["id"] == "image1"

    @pytest.mark.asyncio
    @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    async def test_instance_action(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_action_response = create_autospec(oci.response.Response)
        mock_action_response.data = oci.core.models.Instance(
            id="instance1",
            display_name="Instance 1",
            lifecycle_state="STOPPING",
            shape="VM.Standard.E2.1",
        )
        mock_client.instance_action.return_value = mock_action_response

        async with Client(mcp) as client:
            call_tool_result = await client.call_tool(
                "instance_action",
                {
                    "instance_id": "instance1",
                    "action": "STOP",
                },
            )
            result = call_tool_result.structured_content

            assert result["id"] == "instance1"
            assert result["lifecycle_state"] == "STOPPING"

    # @pytest.mark.asyncio
    # @patch("oracle.oci_compute_mcp_server.utils.client_manager.compute_client")
    # @patch("oracle.oci_compute_mcp_server.server.oci.wait_until")
    # async def test_update_instance_details(self, mock_get_client, mock_wait_until):
    #    ocpus = 2
    #    memory_in_gbs = 16

    #    mock_client = MagicMock()
    #    mock_get_client.return_value = mock_client

    #    new_shape_details = oci.core.models.UpdateInstanceShapeConfigDetails(
    #        ocpus=ocpus, memory_in_gbs=memory_in_gbs,
    #    )

    #    mock_wait_until = MagicMock()
    #    mock_wait_until.return_value = oci.core.models.Instance(
    #        shape_config=new_shape_details,
    #    )

    #    mock_update_response = create_autospec(oci.response.Response)
    #    mock_update_response.data = oci.core.models.Instance(
    #        shape_config=new_shape_details,
    #    )
    #    mock_client.update_instance.return_value = mock_update_response

    #    async with Client(mcp) as client:
    #        result = (
    #            await client.call_tool(
    #                "update_instance_details",
    #                {
    #                    "instance_id": "instance1",
    #                    "ocpus": ocpus,
    #                    "memory_in_gbs": memory_in_gbs,
    #                },
    #            )
    #        ).data

    #        assert result["ocpus"] == ocpus
    #        assert result["memory_in_gbs"] == memory_in_gbs
