"""CLI interface for create-mcp-server."""

import click
import sys
import re
from pathlib import Path
from .generator import generate_mcp_server, sanitize_package_name


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

    # Allowed characters: word chars, spaces, hyphen, dot
    _allowed_re = re.compile(r'^[\w\s\-.]+$')

    def _prompt_validated(prompt_text, default=None):
        while True:
            if default is not None:
                value = click.prompt(prompt_text, default=default, type=str)
            else:
                value = click.prompt(prompt_text, type=str)

            if value and _allowed_re.match(value):
                return value

            click.echo(
                'Invalid input: only letters, numbers, underscore, space, hyphen and dot are allowed. Please try again.',
                err=True)

    # Interactive prompts if values not provided (with validation)
    if not project_name:
        project_name = _prompt_validated('Project name')

    if not description:
        description = click.prompt('Project description',
                                   default=f'An MCP server for {project_name}',
                                   type=str)

    if not author:
        author = _prompt_validated('Author name', default='Your Name')
    else:
        # If author provided via option, validate and re-prompt if invalid
        if not _allowed_re.match(author):
            click.echo(
                'Author contains invalid characters. Please re-enter interactively.',
                err=True)
            author = _prompt_validated('Author name', default='Your Name')

    # If project_name provided via argument, validate and re-prompt if invalid
    if project_name and not _allowed_re.match(project_name):
        click.echo(
            'Project name contains invalid characters. Please re-enter interactively.',
            err=True)
        project_name = _prompt_validated('Project name')

    # Validate project name
    if not project_name or not project_name.strip():
        click.echo('Error: Project name cannot be empty', err=True)
        sys.exit(1)

    # Replace whitespace in project name with hyphens for directory/name
    project_name = re.sub(r"\s+", "-", project_name.strip())

    # Create project directory
    project_dir = Path.cwd() / project_name

    if project_dir.exists():
        click.echo(f'Error: Directory "{project_name}" already exists',
                   err=True)
        sys.exit(1)

    click.echo(f'\n✨ Creating MCP server project: {project_name}')

    try:
        generate_mcp_server(project_dir=project_dir,
                            project_name=project_name,
                            description=description,
                            author=author)

        # Get the sanitized package name for instructions
        package_name = sanitize_package_name(project_name)

        click.echo(f'\n✅ Successfully created {project_name}!')
        click.echo(f'\nNext steps:')
        click.echo(f'  cd {project_name}')
        click.echo(
            f'  uv run --directory {project_dir.resolve()} -m {package_name}')

    except Exception as e:
        click.echo(f'\n❌ Error creating project: {e}', err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
