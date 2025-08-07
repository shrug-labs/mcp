# Oracle MCP Server Repository

Repository containing reference implementations of MCP (Model Context Protocol) servers for managing and interacting with Oracle products. Each MCP server under `src/` may be written in a different programming language, demonstrating MCP’s language-agnostic approach.

## What is MCP?

The Model Context Protocol (MCP) enables standardized, language-agnostic machine-to-machine workflows across data, models, and cloud resources. MCP servers implement specific tool suites, exposing them to MCP-compatible clients.

## Project Scope

- **Proof-of-concept/Reference implementations:**  
  This repository is not intended for production use; servers are provided as reference and for exploration, prototyping, and learning.

- **Polyglot architecture:**  
  Each `src/<server-name>/` directory represents a distinct MCP server, and these may use Python, Node.js, Java, or other languages.

## Prerequisites

- Supported OS: Linux, macOS, or Windows (varies by server; check server README)
- Git (for cloning this repository)
- Internet access (for downloading dependencies)
- *Cloud access*: Some servers require Oracle Cloud Infrastructure (OCI) credentials and configuration ([OCI docs](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm))

**Note:**  
Each MCP server has its own specific requirements (e.g., language runtime version, libraries).  
Always see the respective `src/<server>/README.md` for detailed setup instructions.

## Quick Start

1. **Clone this repository:**
    ```sh
    git clone https://github.com/oracle/mcp.git
    cd mcp
    ```

2. **List available MCP servers:**
    ```sh
    ls src/
    ```

3. **Read the appropriate server's README for setup instructions:**
    ```sh
    cat src/<server-name>/README.md
    ```
    - Example: For the Python-based DBTools MCP server:
      ```
      cd src/dbtools-mcp-server/
      cat README.md
      ```

4. **Typical Python Server Setup Example:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate        # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    *(For Node.js/Java/other servers, follow respective instructions in that server’s README)*

## Directory Structure

```
.
├── src/
│   ├── dbtools-mcp-server/     # MCP server (Python example)
│   ├── another-mcp-server/     # (Possible Node.js, Java, or other implementation)
│   └── ...
├── LICENSE.txt
├── README.md
├── CONTRIBUTING.md
└── SECURITY.md
```
Each server subdirectory includes its own `README.md` with language/runtime details, installation, and usage.

## Contributing

This project welcomes contributions from the community. Before submitting a pull 
request, please [review our contribution guide](./CONTRIBUTING.md).

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security
vulnerability disclosure process.

## License
<!-- The correct copyright notice format for both documentation and software
    is "Copyright (c) [year,] year Oracle and/or its affiliates."
    You must include the year the content was first released (on any platform) and
    the most recent year in which it was revised. -->

Copyright (c) 2025 Oracle and/or its affiliates.
 
Released under the Universal Permissive License v1.0 as shown at  
<https://oss.oracle.com/licenses/upl/>.

## Third-Party APIs

Developers choosing to distribute a binary implementation of this project are responsible for obtaining and providing all required licenses and copyright notices for the third-party code used in order to ensure compliance with their respective open source licenses.
