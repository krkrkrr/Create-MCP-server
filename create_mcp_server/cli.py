"""CLI interface for create-mcp-server."""

import click
import sys
from pathlib import Path
from .generator import generate_mcp_server


@click.group()
def main():
    """Create MCP Server - A CLI tool to scaffold MCP server projects."""
    pass


@main.command()
@click.argument('project_name', required=False)
@click.option('--description', '-d', help='Project description')
@click.option('--author', '-a', help='Author name')
def create(project_name, description, author):
    """Create a new MCP server project."""
    
    # Interactive prompts if values not provided
    if not project_name:
        project_name = click.prompt('Project name', type=str)
    
    if not description:
        description = click.prompt(
            'Project description',
            default=f'An MCP server for {project_name}',
            type=str
        )
    
    if not author:
        author = click.prompt(
            'Author name',
            default='Your Name',
            type=str
        )
    
    # Validate project name
    if not project_name or not project_name.strip():
        click.echo('Error: Project name cannot be empty', err=True)
        sys.exit(1)
    
    # Create project directory
    project_dir = Path.cwd() / project_name
    
    if project_dir.exists():
        click.echo(f'Error: Directory "{project_name}" already exists', err=True)
        sys.exit(1)
    
    click.echo(f'\n✨ Creating MCP server project: {project_name}')
    
    try:
        generate_mcp_server(
            project_dir=project_dir,
            project_name=project_name,
            description=description,
            author=author
        )
        
        click.echo(f'\n✅ Successfully created {project_name}!')
        click.echo(f'\nNext steps:')
        click.echo(f'  cd {project_name}')
        click.echo(f'  uv sync')
        click.echo(f'  uv run python -m {project_name.replace("-", "_")}')
        
    except Exception as e:
        click.echo(f'\n❌ Error creating project: {e}', err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
