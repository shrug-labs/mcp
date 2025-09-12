import os
from logging import Logger

import oci
from fastmcp import FastMCP

logger = Logger("oci_migration_mcp", level="INFO")

mcp = FastMCP("oci_migration")


def get_migration_client():
    logger.info("entering get_migration_client")
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )
    private_key = oci.signer.load_private_key_from_file(config["key_file"])
    token_file = config["security_token_file"]
    token = None
    with open(token_file, "r") as f:
        token = f.read()
    signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
    return oci.cloud_migrations.MigrationClient(config, signer=signer)


@mcp.tool
def get_migration(migration_id: str):
    """
    Get details for a specific Migration Project by OCID.
    Args:
        migration_id (str): OCID of the migration project.
    Returns:
        dict: Migration project details.
    """
    client = get_migration_client()
    return client.get_migration(migration_id).data


@mcp.tool
def list_migrations(compartment_id: str, lifecycle_state: str = None):
    """
    List Migration Projects for a compartment, optionally filtered by lifecycle state.
    Args:
        compartment_id (str): OCID of the compartment.
        lifecycle_state (str, optional): Filter by lifecycle state.
    Returns:
        list of dict: Each dict is a migration object.
    """
    client = get_migration_client()
    list_args = {"compartment_id": compartment_id}

    if lifecycle_state is not None:
        list_args["lifecycle_state"] = lifecycle_state

    migrations = client.list_migrations(**list_args).data.items
    return [
        {
            "id": migration.id,
            "display_name": migration.display_name,
            "compartment_id": migration.compartment_id,
            "lifecycle_state": migration.lifecycle_state,
            "lifecycle_details": migration.lifecycle_details,
            "time_created": migration.time_created,
            "replication_schedule_id": migration.replication_schedule_id,
            "is_completed": migration.is_completed,
        }
        for migration in migrations
    ]


if __name__ == "__main__":
    # MCP spec: OpenAPI exposed at /openapi.json, native MCP at /mcp/v1
    # mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
    # mcp.run(transport="sse", host="127.0.0.1", port=args.port)
    mcp.run()
