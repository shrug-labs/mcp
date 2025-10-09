# OCI API MCP Server

## Overview
This server provides tools to run OCI CLI commands to interact with OCI services.
It includes resources and tools to help with OCI command execution and provide helpful information.

## Running the server
Please follow the guidelines under [Quickstart](../../README.md#quick-start)
## Tools and Resources

### get_oci_command_help
Returns helpful instructions for running an OCI CLI command.
Only provide the command after 'oci', do not include the string 'oci' in your command.

### run_oci_command
Runs an OCI CLI command.
This tool allows you to run OCI CLI commands on the user's behalf.
Only provide the command after 'oci', do not include the string 'oci' in your command.

### get_oci_commands (Resource)
Returns helpful information on various OCI services and related commands.

## Tests
The tests for this server are located in `oracle/oci_api_mcp_server/tests/test_oci_api_tools.py`.
They cover various scenarios for the tools provided by the server, including success and failure cases.

## Implementation Details
The server is implemented in `oracle/oci_api_mcp_server/server.py`.
It uses the FastMCP framework to provide the tools and resources.

<span style="font-size: small;">Copyright (c) 2025, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v1.0 as shown at
https://oss.oracle.com/licenses/upl.</span>
