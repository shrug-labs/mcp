import os
from logging import Logger

import oci
from oracle.oci_compute_mcp_server.models import (
    Image,
    Instance,
    map_image,
    map_instance,
)

logger = Logger(__name__, level="INFO")


class ComputeClientManager:
    """Manages OCI clients for Compute operations"""

    def __init__(self):
        """Initialize the client manager."""
        self._compute_client = None

    def get_auth(self):
        config = oci.config.from_file(
            profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
        )

        private_key = oci.signer.load_private_key_from_file(config["key_file"])
        token_file = config["security_token_file"]
        token = None
        with open(token_file, "r") as f:
            token = f.read()
        signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
        return config, signer

    _compute_client: oci.core.ComputeClient

    def compute_client(self):
        """Create the Compute client"""
        try:
            config, signer = self.get_auth()
            self._compute_client = oci.core.ComputeClient(config, signer=signer)
            logger.info("Created new Compute client")
        except Exception as e:
            logger.error(f"Error creating Compute client: {str(e)}")
            raise

        return self._compute_client


client_manager = ComputeClientManager()


def discover_instances(compartment_id: str) -> list[Instance]:
    """
    Discover all Instances
    Returns: List of Instances
    """
    instances: list[Instance] = []

    try:
        # List Instances
        client = client_manager.compute_client()

        response: oci.response.Response = None
        has_next_page = True
        next_page: str = None

        while has_next_page:
            response = client.list_instances(
                compartment_id=compartment_id, page=next_page
            )
            has_next_page = response.has_next_page
            next_page = response.next_page if hasattr(response, "next_page") else None

            data: list[oci.core.models.Instance] = response.data
            for d in data:
                instance = map_instance(d)
                instances.append(instance)

        logger.info(f"Found {len(instances)} Instances")
        return instances

    except Exception as e:
        logger.error(f"Error discovering Instances: {str(e)}")
        raise


def discover_instance(instance_id: str) -> Instance:
    """
    Discover a specific Instance
    Returns: Instance
    """
    try:
        # Get Instance
        client = client_manager.compute_client()

        response: oci.response.Response = client.get_instance(instance_id=instance_id)
        data: oci.core.models.Instance = response.data
        logger.info("Found Instance")
        return map_instance(data)

    except Exception as e:
        logger.error(f"Error discovering Instance: {str(e)}")
        raise


def create_instance(
    compartment_id: str,
    display_name: str,
    availability_domain: str,
    image_id: str,
    subnet_id: str,
    shape: str,
) -> Instance:
    """
    Launch an Instance
    Returns: Instance
    """
    try:
        # Create Instance
        client = client_manager.compute_client()

        # Build shape config for Flex shapes
        shape_config = None
        try:
            if isinstance(shape, str) and "Flex" in shape:
                shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(
                    ocpus=1, memory_in_gbs=6
                )
        except Exception:
            shape_config = None

        launch_details = oci.core.models.LaunchInstanceDetails(
            compartment_id=compartment_id,
            display_name=display_name,
            availability_domain=availability_domain,
            shape=shape,
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                image_id=image_id
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=subnet_id),
            shape_config=shape_config,
        )

        response: oci.response.Response = client.launch_instance(launch_details)
        data: oci.core.models.Instance = response.data
        logger.info("Launched Instance")
        return map_instance(data)

    except Exception as e:
        logger.error(f"Error launching Instance: {str(e)}")
        raise


def discover_images(compartment_id: str, operating_system: str) -> list[Image]:
    """
    Discover all Images
    Returns: List of Images
    """
    images: list[Image] = []

    try:
        # List Images
        client = client_manager.compute_client()

        response: oci.response.Response = None
        has_next_page = True
        next_page: str = None

        while has_next_page:
            response = client.list_images(compartment_id=compartment_id, page=next_page)
            has_next_page = response.has_next_page
            next_page = response.next_page if hasattr(response, "next_page") else None

            data: list[oci.core.models.Image] = response.data
            if operating_system:
                data = [img for img in data if img.operating_system == operating_system]

            for d in data:
                image = map_image(d)
                images.append(image)

        logger.info(f"Found {len(images)} Images")
        return images

    except Exception as e:
        logger.error(f"Error discovering Images: {str(e)}")
        raise


def discover_image(image_id: str) -> Image:
    """
    Discover a specific Image
    Returns: Image
    """
    try:
        # Get Image
        client = client_manager.compute_client()

        response: oci.response.Response = client.get_image(image_id=image_id)
        data: oci.core.models.Image = response.data
        logger.info("Found Image")
        return map_image(data)

    except Exception as e:
        logger.error(f"Error discovering Image: {str(e)}")
        raise


def perform_instance_action(instance_id: str, action: str) -> Instance:
    """
    Performs an action on an instance
    Returns: Instance
    """
    try:
        client = client_manager.compute_client()

        response: oci.response.Response = client.instance_action(instance_id, action)
        data: oci.core.models.Instance = response.data
        logger.info("Performed instance action")
        return map_instance(data)

    except Exception as e:
        logger.error(f"Error performing instance action: {str(e)}")
        raise
