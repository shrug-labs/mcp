from unittest.mock import MagicMock, create_autospec, patch

import oci
import pytest
from fastmcp import Client
from oracle.oci_monitoring_mcp_server.server import mcp


class TestMonitoringTools:
    @pytest.mark.asyncio
    @patch("oracle.oci_monitoring_mcp_server.server.get_monitoring_client")
    async def test_get_compute_instance_cpu_utilization(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_summarize_response = create_autospec(oci.response.Response)
        mock_summarize_response.data = [
            oci.monitoring.models.MetricData(
                aggregated_datapoints=[
                    MagicMock(timestamp="2023-01-01T00:00:00Z", value=50.0)
                ]
            )
        ]
        mock_client.summarize_metrics_data.return_value = mock_summarize_response

        async with Client(mcp) as client:
            result = (
                await client.call_tool(
                    "get_compute_instance_cpu_utilization",
                    {
                        "compartment_id": "compartment1",
                        "instance_id": "instance1",
                        "start_time": "2023-01-01T00:00:00Z",
                        "end_time": "2023-01-01T01:00:00Z",
                    },
                )
            ).structured_content["result"]

            assert len(result) == 1
            assert result[0]["value"] == 50.0

    @pytest.mark.asyncio
    @patch("oracle.oci_monitoring_mcp_server.server.get_monitoring_client")
    async def test_get_compute_instance_memory_utilization(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_summarize_response = create_autospec(oci.response.Response)
        mock_summarize_response.data = [
            oci.monitoring.models.MetricData(
                aggregated_datapoints=[
                    MagicMock(timestamp="2023-01-01T00:00:00Z", value=60.0)
                ]
            )
        ]
        mock_client.summarize_metrics_data.return_value = mock_summarize_response

        async with Client(mcp) as client:
            result = (
                await client.call_tool(
                    "get_compute_instance_memory_utilization",
                    {
                        "compartment_id": "compartment1",
                        "instance_id": "instance1",
                        "start_time": "2023-01-01T00:00:00Z",
                        "end_time": "2023-01-01T01:00:00Z",
                    },
                )
            ).structured_content["result"]

            assert len(result) == 1
            assert result[0]["value"] == 60.0
