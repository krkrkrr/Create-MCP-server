# Create-MCP-server

Create the minimum MCP server with Python - A CLI tool inspired by create-react-app.

## Usage

Create a new MCP server project:

```bash
uvx --from git+https://github.com/krkrkrr/Create-MCP-server create-mcp-server create
```

Or install locally:

```bash
git clone https://github.com/krkrkrr/Create-MCP-server.git
cd Create-MCP-server
uv sync
uv run create-mcp-server create
```

The CLI will interactively prompt you for:
- Project name
- Project description
- Author name

## What gets created

The generated project includes:

- `pyproject.toml` configured for uv package management
- A fastmcp-based MCP server with a healthcheck tool
- README with setup and usage instructions
- Proper Python package structure

## Example

```bash
$ uvx --from git+https://github.com/krkrkrr/Create-MCP-server create-mcp-server create
Project name: my-awesome-server
Project description [An MCP server for my-awesome-server]: My awesome MCP server
Author name [Your Name]: John Doe

✨ Creating MCP server project: my-awesome-server

✅ Successfully created my-awesome-server!

Next steps:
  cd my-awesome-server
  uv sync
  uv run python -m my_awesome_server
```

## Requirements

- Python 3.10+
- uv (https://docs.astral.sh/uv/)

## License

MIT
