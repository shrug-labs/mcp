import argparse
from logging import Logger

import oci
from fastmcp import FastMCP

logger = Logger("oci_compute_mcp", level="INFO")

mcp = FastMCP("oci_compute")


def get_networking_client():
    # Assumes you have ~/.oci/config with [DEFAULT] set up
    config = oci.config.from_file("~/.oci/config")
    return oci.core.VirtualNetworkClient(config)


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
    parser = argparse.ArgumentParser(
        description="Oracle Cloud Infrastructure Networking MCP server"
    )
    parser.add_argument("port", type=int, help="port number")

    args = parser.parse_args()
    # MCP spec: OpenAPI exposed at /openapi.json, native MCP at /mcp/v1
    # mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
    mcp.run(transport="sse", host="127.0.0.1", port=args.port)
