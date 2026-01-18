"""Generator for MCP server projects."""

import re
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape


def sanitize_package_name(project_name: str) -> str:
    """
    Convert a project name to a valid Python package name.
    
    Args:
        project_name: The project name to sanitize
        
    Returns:
        A valid Python package name
    """
    # Replace invalid characters with underscores and convert to lowercase
    package_name = re.sub(r'[^a-zA-Z0-9_]', '_', project_name).lower()

    # Remove leading/trailing underscores
    package_name = package_name.strip('_')

    # If empty or starts with a digit, prepend underscore
    if not package_name or package_name[0].isdigit():
        package_name = '_' + package_name if package_name else '_package'

    return package_name


def generate_mcp_server(project_dir: Path, project_name: str, description: str,
                        author: str):
    """Generate a new MCP server project with fastmcp."""

    # Create project directory
    project_dir.mkdir(parents=True, exist_ok=False)

    # Setup Jinja2 environment
    env = Environment(
        loader=PackageLoader('create_mcp_server', 'templates'),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Convert project name to valid Python package name
    package_name = sanitize_package_name(project_name)

    # Context for templates
    context = {
        'project_name': project_name,
        'package_name': package_name,
        'description': description,
        'author': author,
        'project_path': project_dir.absolute()
    }

    # Create package directory
    package_dir = project_dir / package_name
    package_dir.mkdir(parents=True, exist_ok=True)

    # Generate files from templates
    templates_to_generate = [
        ('pyproject.toml.j2', project_dir / 'pyproject.toml'),
        ('README.md.j2', project_dir / 'README.md'),
        ('__init__.py.j2', package_dir / '__init__.py'),
        ('__main__.py.j2', package_dir / '__main__.py'),
        ('.gitignore.j2', project_dir / '.gitignore'),
    ]

    for template_name, output_path in templates_to_generate:
        template = env.get_template(template_name)
        content = template.render(context)
        output_path.write_text(content)
