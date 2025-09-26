import json
import os
import subprocess
from logging import Logger
from typing import Annotated

import oci
from fastmcp import FastMCP

logger = Logger(__name__, level="INFO")

mcp = FastMCP(name="oracle.oci-api-mcp-server")


@mcp.resource("resource://oci-api-commands")
def get_oci_commands() -> str:
    try:
        # Run OCI CLI command using subprocess
        result = subprocess.run(
            ["oci", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


@mcp.tool
def get_oci_command_help(command: str) -> str:
    """Returns helpful instructions for running an OCI CLI command.
    Only provide the command after 'oci', do not include the string 'oci'
    in your command.

    CLI commands are structured as <service> <resource> <action>; you can get
    help at the service level, resource level or action level, respectively:
        1. compute
        2. compute instance
        3. compute instance list

    If your request for help for a specific command
    returns an error, make your requests successively less specific;
    example:
        1. compute instance list
        2. compute instance
        3. compute
    """
    try:
        # Run OCI CLI command using subprocess
        result = subprocess.run(
            ["oci"] + command.split() + ["--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


@mcp.tool
def run_oci_command(
    command: Annotated[
        str,
        "The OCI CLI command to run. Do not include 'oci' in your command",
    ],
) -> dict:
    """Runs an OCI CLI command.
    Only provide the command after 'oci', do not include the string 'oci'
    in your command.
    """

    print(command)

    profile = os.getenv("OCI_CONFIG_PROFILE", oci.config.DEFAULT_PROFILE)

    # Run OCI CLI command using subprocess
    try:
        result = subprocess.run(
            [
                "oci",
                "--profile",
                profile,
                "--auth",
                "security_token",
            ]
            + command.split(),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return {
            "error": e.stderr,
            "output": e.stdout,
        }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
