import os
from logging import Logger

import oci
from fastmcp import FastMCP
from oci.monitoring.models import SummarizeMetricsDataDetails

logger = Logger("oci_metrics_mcp", level="INFO")

mcp = FastMCP("oci_metrics")


def get_monitoring_client():
    logger.info("entering get_monitoring_client")
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )

    private_key = oci.signer.load_private_key_from_file(config["key_file"])
    token_file = config["security_token_file"]
    token = None
    with open(token_file, "r") as f:
        token = f.read()
    signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
    return oci.monitoring.MonitoringClient(config, signer=signer)


@mcp.tool
def get_compute_instance_cpu_utilization(
    compartment_id: str, instance_id: str, start_time: str, end_time: str
):
    monitoring_client = get_monitoring_client()
    namespace = "oci_computeagent"
    query = f'CpuUtilization[1m]{{resourceId=~"{instance_id}"}}.mean()'

    datapoints = monitoring_client.summarize_metrics_data(
        compartment_id=compartment_id,
        summarize_metrics_data_details=SummarizeMetricsDataDetails(
            namespace=namespace,
            query=query,
            start_time=start_time,
            end_time=end_time,
            resolution="1m",
        ),
    ).data

    result = []
    for datapoint in datapoints:
        for aggregated_datapoint in datapoint.aggregated_datapoints:
            result.append(
                {
                    "timestamp": aggregated_datapoint.timestamp,
                    "value": aggregated_datapoint.value,
                }
            )
    return result


@mcp.tool
def get_compute_instance_memory_utilization(
    compartment_id: str, instance_id: str, start_time: str, end_time: str
):
    monitoring_client = get_monitoring_client()
    namespace = "oci_computeagent"
    query = f'MemoryUtilization[1m]{{resourceId=~"{instance_id}"}}.mean()'

    datapoints = monitoring_client.summarize_metrics_data(
        compartment_id=compartment_id,
        summarize_metrics_data_details=SummarizeMetricsDataDetails(
            namespace=namespace,
            query=query,
            start_time=start_time,
            end_time=end_time,
            resolution="1m",
        ),
    ).data

    result = []
    for datapoint in datapoints:
        for aggregated_datapoint in datapoint.aggregated_datapoints:
            result.append(
                {
                    "timestamp": aggregated_datapoint.timestamp,
                    "value": aggregated_datapoint.value,
                }
            )
    return result


if __name__ == "__main__":
    mcp.run()
