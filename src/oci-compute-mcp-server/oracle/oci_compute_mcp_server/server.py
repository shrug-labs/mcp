import os
from logging import Logger
from typing import Annotated

import oci
from fastmcp import FastMCP

logger = Logger(__name__, level="INFO")

mcp = FastMCP(name="oracle.oci-compute-mcp-server")


def get_compute_client():
    logger.info("entering get_compute_client")
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )

    private_key = oci.signer.load_private_key_from_file(config["key_file"])
    token_file = config["security_token_file"]
    token = None
    with open(token_file, "r") as f:
        token = f.read()
    signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
    return oci.core.ComputeClient(config, signer=signer)


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
    image_id: str,
    subnet_id: str,
    shape: Annotated[str, "Instance shape"] = "VM.Standard.A1.Flex",
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
def get_image(image_id: str):
    compute = get_compute_client()
    return compute.get_image(image_id).data


@mcp.tool
def list_images(compartment_id: str, operating_system: str = None):
    """List images, optionally filtered by operating system"""
    compute = get_compute_client()
    images = compute.list_images(compartment_id).data

    if operating_system:
        images = [img for img in images if img.operating_system == operating_system]

    return [
        {
            "id": img.id,
            "display_name": img.display_name,
            "operating_system": img.operating_system,
            "operating_system_version": img.operating_system_version,
        }
        for img in images
    ]


@mcp.tool
def instance_action(instance_id: str, action: str):
    compute = get_compute_client()
    response = compute.instance_action(instance_id, action)
    return {"status": action, "opc_request_id": response.headers.get("opc-request-id")}


@mcp.tool
def update_instance_details(
    instance_id: str,
    ocpus: Annotated[int, "Number of CPUs allocated to the instance"],
    memory_in_gbs: Annotated[
        int, "Amount of memory in gigabytes (GB) allocated to the instance"
    ],
):
    """Update instance details; this may restart the instance so warn the user"""
    compute_client = get_compute_client()

    shape_config_details = oci.core.models.UpdateInstanceShapeConfigDetails(
        ocpus=ocpus, memory_in_gbs=memory_in_gbs
    )

    update_instance_details = oci.core.models.UpdateInstanceDetails(
        shape_config=shape_config_details
    )

    try:
        compute_client.update_instance(
            instance_id=instance_id, update_instance_details=update_instance_details
        )

        get_response = compute_client.get_instance(instance_id)

        final_response = oci.wait_until(
            client=compute_client,
            response=get_response,
            evaluate_response=lambda x: x.data.shape_config.ocpus == ocpus
            and x.data.shape_config.memory_in_gbs == memory_in_gbs,
            max_interval_seconds=5,
            max_wait_seconds=240,
        )

        return {
            "instance_id": instance_id,
            "ocpus": final_response.data.shape_config.ocpus,
            "memory_in_gbs": final_response.data.shape_config.memory_in_gbs,
        }
    except oci.exceptions.ServiceError as e:
        return {
            "error_code": e.code,
            "message": e.message,
        }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
