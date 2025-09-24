from logging import Logger
from typing import Annotated

from fastmcp import FastMCP
from oracle.oci_compute_mcp_server.models import (
    Image,
    Instance,
)
from oracle.oci_compute_mcp_server.utils import (
    create_instance,
    discover_image,
    discover_images,
    discover_instance,
    discover_instances,
    perform_instance_action,
)

logger = Logger(__name__, level="INFO")

mcp = FastMCP(name="oracle.oci-compute-mcp-server")


@mcp.tool
async def list_instances(compartment_id: str) -> list[Instance]:
    """List Instances in a given compartment"""
    try:
        logger.info("Discovering Instances")
        return discover_instances(compartment_id)

    except Exception as e:
        logger.error(f"Error in list_instances tool: {str(e)}")
        raise


@mcp.tool
async def get_instance(instance_id: str) -> Instance:
    """Get Instance with a given instance OCID"""
    try:
        logger.info("Discovering Instance")
        return discover_instance(instance_id)

    except Exception as e:
        logger.error(f"Error in get_instance tool: {str(e)}")
        raise


@mcp.tool
def launch_instance(
    compartment_id: str,
    display_name: str,
    availability_domain: str,
    subnet_id: str,
    image_id: str,
    shape: Annotated[str, "Instance shape"] = "VM.Standard.A1.Flex",
) -> Instance:
    """Create a new Instance"""
    try:
        logger.info("Creating Instance")
        return create_instance(
            compartment_id,
            display_name,
            availability_domain,
            image_id,
            subnet_id,
            shape,
        )

    except Exception as e:
        logger.error(f"Error in launch_instance tool: {str(e)}")
        raise


# @mcp.tool
# def terminate_instance(instance_id: str):
#    compute = get_compute_client()
#    response = compute.terminate_instance(instance_id)
#    return {
#        "status": "terminated",
#        "opc_request_id": response.headers.get("opc-request-id"),
#    }


@mcp.tool
def list_images(compartment_id: str, operating_system: str = None) -> list[Image]:
    """List images in a given compartment, optionally filtered by operating system"""
    try:
        logger.info("Discovering Images")
        return discover_images(
            compartment_id=compartment_id, operating_system=operating_system
        )

    except Exception as e:
        logger.error(f"Error in list_images tool: {str(e)}")
        raise


@mcp.tool
def get_image(image_id: str) -> Image:
    """Get Image with a given image OCID"""
    try:
        logger.info("Discovering Image")
        return discover_image(image_id)

    except Exception as e:
        logger.error(f"Error in get_image tool: {str(e)}")
        raise


@mcp.tool
def instance_action(
    instance_id: str,
    action: Annotated[
        str,
        "The action to be performed. The action can only be one of these values: START, STOP, RESET, SOFTSTOP, SOFTRESET, SENDDIAGNOSTICINTERRUPT, DIAGNOSTICREBOOT, REBOOTMIGRATE",  # noqa
    ],
) -> Instance:
    """Perform the desired action on a given instance"""
    try:
        logger.info("Performing instance action")
        return perform_instance_action(instance_id, action)

    except Exception as e:
        logger.error(f"Error in instance_action tool: {str(e)}")
        raise


# TODO: commenting this out until create instance gets fixed as well
# @mcp.tool
# def update_instance_details(
#     instance_id: str,
#     ocpus: Annotated[int, "Number of CPUs allocated to the instance"],
#     memory_in_gbs: Annotated[
#         int, "Amount of memory in gigabytes (GB) allocated to the instance"
#     ],
# ) -> dict:
#     """Update instance details; this may restart the instance so warn the user"""
#     compute_client = get_compute_client()

#     shape_config_details = oci.core.models.UpdateInstanceShapeConfigDetails(
#         ocpus=ocpus, memory_in_gbs=memory_in_gbs
#     )

#     update_instance_details = oci.core.models.UpdateInstanceDetails(
#         shape_config=shape_config_details
#     )

#     try:
#         compute_client.update_instance(
#             instance_id=instance_id, update_instance_details=update_instance_details
#         )

#         get_response = compute_client.get_instance(instance_id)

#         final_response = oci.wait_until(
#             client=compute_client,
#             response=get_response,
#             evaluate_response=lambda x: x.data.shape_config.ocpus == ocpus
#             and x.data.shape_config.memory_in_gbs == memory_in_gbs,
#             max_interval_seconds=5,
#             max_wait_seconds=240,
#         )

#         return {
#             "instance_id": instance_id,
#             "ocpus": final_response.data.shape_config.ocpus,
#             "memory_in_gbs": final_response.data.shape_config.memory_in_gbs,
#         }
#     except oci.exceptions.ServiceError as e:
#         return {
#             "error_code": e.code,
#             "message": e.message,
#         }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
