"""
Copyright (c) 2025, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v1.0 as shown at
https://oss.oracle.com/licenses/upl.
"""

import os
from logging import Logger
from typing import Annotated

import oci
from fastmcp import FastMCP

from . import __project__, __version__

logger = Logger(__name__, level="INFO")

mcp = FastMCP(name=__project__)


def get_networking_client():
    config = oci.config.from_file(
        profile_name=os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)
    )
    user_agent_name = __project__.split("oracle.", 1)[1].split("-server", 1)[0]
    config["additional_user_agent"] = f"{user_agent_name}/{__version__}"
    private_key = oci.signer.load_private_key_from_file(config["key_file"])
    token_file = config["security_token_file"]
    token = None
    with open(token_file, "r") as f:
        token = f.read()
    signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
    return oci.core.VirtualNetworkClient(config, signer=signer)


@mcp.tool
def list_vcns(compartment_id: str) -> list[dict]:
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


@mcp.tool
def create_vcn(compartment_id: str, cidr_block: str, display_name: str):
    networking = get_networking_client()
    vcn_details = oci.core.models.CreateVcnDetails(
        compartment_id=compartment_id, cidr_block=cidr_block, display_name=display_name
    )
    return networking.create_vcn(vcn_details).data


@mcp.tool
def create_subnet(vcn_id: str, compartment_id: str, cidr_block: str, display_name: str):
    networking = get_networking_client()
    subnet_details = oci.core.models.CreateSubnetDetails(
        compartment_id=compartment_id,
        vcn_id=vcn_id,
        cidr_block=cidr_block,
        display_name=display_name,
    )
    return networking.create_subnet(subnet_details).data


@mcp.tool
def list_subnets(compartment_id: str, vcn_id: str = None) -> list[dict]:
    networking = get_networking_client()
    subnets = networking.list_subnets(compartment_id, vcn_id=vcn_id).data
    return [
        {
            "subnet_id": subnet.id,
            "vcn_id": subnet.vcn_id,
            "display_name": subnet.display_name,
            "lifecycle_state": subnet.lifecycle_state,
        }
        for subnet in subnets
    ]


@mcp.tool
def get_subnet(subnet_id: str):
    networking = get_networking_client()
    return networking.get_subnet(subnet_id).data


@mcp.tool(
    name="list_security_lists",
    description="Lists the security lists in the specified VCN and compartment. "
    "If the VCN ID is not provided, then the list includes the security lists from all "
    "VCNs in the specified compartment.",
)
def list_security_lists(
    compartment_id: Annotated[str, "Compartment ocid"],
    vcn_id: Annotated[str, "VCN ocid"] = None,
) -> list[dict]:
    networking = get_networking_client()
    security_lists = networking.list_security_lists(compartment_id, vcn_id=vcn_id).data
    return [
        {
            "security_list_id": security_list.id,
            "display_name": security_list.display_name,
            "lifecycle_state": security_list.lifecycle_state,
            "vcn_id": security_list.vcn_id,
        }
        for security_list in security_lists
    ]


@mcp.tool(name="get_security_list", description="Gets the security list's information.")
def get_security_list(security_list_id: Annotated[str, "security list id"]):
    networking = get_networking_client()
    return networking.get_security_list(security_list_id).data


@mcp.tool(
    name="list_network_security_group",
    description="Lists either the network security groups in the specified compartment,"
    "or those associated with the specified VLAN. You must specify either a vlanId or"
    "a compartmentId, but not both. If you specify a vlanId, all other parameters are "
    "ignored.",
)
def list_network_security_groups(
    compartment_id: Annotated[str, "compartment ocid"],
    vlan_id: Annotated[str, "vlan ocid"] = None,
    vcn_id: Annotated[str, "vcn ocid"] = None,
) -> list[dict]:
    networking = get_networking_client()
    nsg_list = networking.list_network_security_groups(
        compartment_id=compartment_id, vlan_id=vlan_id, vcn_id=vcn_id
    ).data
    return [
        {
            "nsg_id": nsg.id,
            "display_name": nsg.display_name,
            "lifecycle_state": nsg.lifecycle_state,
        }
        for nsg in nsg_list
    ]


@mcp.tool(
    name="get_network_security_group",
    description="Gets the specified network security group's information.",
)
def get_network_security_group(network_security_group_id: Annotated[str, "nsg id"]):
    networking = get_networking_client()
    return networking.get_network_security_group(network_security_group_id).data


def main():
    mcp.run()


if __name__ == "__main__":
    main()
