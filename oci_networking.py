import os
from logging import Logger

import oci
from fastmcp import FastMCP

logger = Logger("oci_compute_mcp", level="INFO")

mcp = FastMCP("oci_compute")


def get_networking_client():
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )
    private_key = oci.signer.load_private_key_from_file(config["key_file"])
    token_file = config["security_token_file"]
    token = None
    with open(token_file, "r") as f:
        token = f.read()
    signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
    return oci.core.VirtualNetworkClient(config, signer=signer)


@mcp.tool
def list_vcns(compartment_id: str):
    networking = get_networking_client()
    vcns = networking.list_vcns(compartment_id).data
    return [
        {
            "vcn_id": vcn.id,
            "display_name": vcn.display_name,
            "lifecycle_state": vcn.lifecycle_state,
        }
        for vcn in vcns
    ]


@mcp.tool
def get_vcn(vcn_id: str):
    networking = get_networking_client()
    return networking.get_vcn(vcn_id).data


@mcp.tool
def delete_vcn(vcn_id: str):
    networking = get_networking_client()
    return networking.delete_vcn(vcn_id).data


if __name__ == "__main__":
    # MCP spec: OpenAPI exposed at /openapi.json, native MCP at /mcp/v1
    # mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
    # mcp.run(transport="sse", host="127.0.0.1", port=args.port)
    mcp.run()
