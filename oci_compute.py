from logging import Logger

import oci
from fastmcp import FastMCP

logger = Logger("oci_compute_mcp", level="INFO")

mcp = FastMCP("oci_compute")


def get_compute_client():
    logger.info("entering get_compute_client")
    config = oci.config.from_file()
    return oci.core.ComputeClient(config)


@mcp.tool
def list_instances(compartment_id: str):
    compute = get_compute_client()
    instances = compute.list_instances(compartment_id).data
    return [
        {
            "instance_id": inst.id,
            "display_name": inst.display_name,
            "lifecycle_state": inst.lifecycle_state,
            "shape": inst.shape,
        }
        for inst in instances
    ]


@mcp.tool
def launch_instance(
    compartment_id: str,
    display_name: str,
    availability_domain: str,
    shape: str,
    image_id: str,
    subnet_id: str,
):
    compute = get_compute_client()
    launch_details = oci.core.models.LaunchInstanceDetails(
        compartment_id=compartment_id,
        display_name=display_name,
        availability_domain=availability_domain,
        shape=shape,
        image_id=image_id,
        subnet_id=subnet_id,
    )
    instance = compute.launch_instance(launch_details).data
    return {
        "id": instance.id,
        "display_name": instance.display_name,
        "lifecycle_state": instance.lifecycle_state,
    }


@mcp.tool
def get_instance(instance_id: str):
    compute = get_compute_client()
    return compute.get_instance(instance_id).data


# @mcp.tool
# def terminate_instance(instance_id: str):
#    compute = get_compute_client()
#    response = compute.terminate_instance(instance_id)
#    return {
#        "status": "terminated",
#        "opc_request_id": response.headers.get("opc-request-id"),
#    }


@mcp.tool
def instance_action(instance_id: str, action: str):
    compute = get_compute_client()
    response = compute.instance_action(instance_id, action)
    return {"status": action, "opc_request_id": response.headers.get("opc-request-id")}


if __name__ == "__main__":

    # MCP spec: OpenAPI exposed at /openapi.json, native MCP at /mcp/v1
    # mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")

    # mcp.run(transport="sse", host="127.0.0.1", port=args.port)
    mcp.run()
