import os

import oci
from fastmcp import FastMCP

mcp = FastMCP(name="oracle.oci-identity-mcp-server")


def get_identity_client():
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )
    private_key = oci.signer.load_private_key_from_file(config["key_file"])
    token_file = config["security_token_file"]
    with open(token_file, "r") as f:
        token = f.read()
    signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
    return oci.identity.IdentityClient(config, signer=signer)


@mcp.tool
def list_compartments(tenancy_id: str) -> list[dict]:
    identity = get_identity_client()
    compartments = identity.list_compartments(tenancy_id).data
    return [
        {
            "id": compartment.id,
            "name": compartment.name,
            "description": compartment.description,
            "lifecycle_state": compartment.lifecycle_state,
        }
        for compartment in compartments
    ]


@mcp.tool
def get_tenancy_info(tenancy_id: str) -> dict:
    identity = get_identity_client()
    tenancy = identity.get_tenancy(tenancy_id).data
    return {
        "id": tenancy.id,
        "name": tenancy.name,
        "description": tenancy.description,
        "home_region_key": tenancy.home_region_key,
    }


@mcp.tool
def get_current_tenancy() -> dict:
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )
    tenancy_id = config["tenancy"]
    identity = get_identity_client()
    tenancy = identity.get_tenancy(tenancy_id).data
    return {
        "id": tenancy.id,
        "name": tenancy.name,
        "description": tenancy.description,
        "home_region_key": tenancy.home_region_key,
    }


@mcp.tool
def create_auth_token(user_id: str) -> dict:
    identity = get_identity_client()
    token = identity.create_auth_token(user_id=user_id).data
    return {
        "token": token.token,
        "description": token.description,
        "lifecycle_state": token.lifecycle_state,
    }


@mcp.tool
def get_current_user() -> dict:
    identity = get_identity_client()
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )
    user_id = config["user"]
    user = identity.get_user(user_id).data
    return {
        "id": user.id,
        "name": user.name,
        "description": user.description,
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
