"""CLI adapter for BlackDuck AI Command using Click"""

import sys
import json
import click
from .types import BlackDuckInitInput
from .blackduck_init import blackduck_init
from .logger import get_logger

logger = get_logger(__name__)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """BlackDuck AI Command - Initialize BlackDuck scanning via CLI"""
    pass


@cli.command()
@click.option(
    "--project",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    help="Path to the project directory",
)
@click.option(
    "--polaris-token",
    required=True,
    envvar="POLARIS_TOKEN",
    help="Polaris authentication token (or set POLARIS_TOKEN env var)",
)
@click.option(
    "--server",
    required=False,
    envvar="BLACKDUCK_SERVER_URL",
    default=None,
    help="BlackDuck server URL (optional for now, or set BLACKDUCK_SERVER_URL env var)",
)
@click.option(
    "--api-token",
    required=False,
    envvar="BLACKDUCK_API_TOKEN",
    default=None,
    help="BlackDuck API token (optional, or set BLACKDUCK_API_TOKEN env var)",
)
@click.option(
    "--include-dev",
    is_flag=True,
    default=False,
    help="Include development dependencies in scan",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Output results as JSON",
)
def init(project, polaris_token, server, api_token, include_dev, output_json):
    """Initialize BlackDuck scanning for a project"""

    logger.info("BlackDuck CLI init command started")

    try:
        # Create input
        input_data = BlackDuckInitInput(
            project_path=project,
            polaris_token=polaris_token,
            server_url=server,
            api_token=api_token,
            include_dev_deps=include_dev,
        )

        # Execute
        result = blackduck_init(input_data)

        # Output
        if output_json:
            # JSON output
            output_dict = result.model_dump()
            click.echo(json.dumps(output_dict, indent=2))
        else:
            # Human-readable output
            if result.success:
                click.secho("✅ Success!", fg="green", bold=True)
                click.echo(f"Message: {result.message}")
                click.echo(f"Scan ID: {result.scan_id}")
                click.echo(f"Config: {result.config_path}")
                click.echo(f"Output: {result.output_file}")

                if result.details:
                    click.echo("\nDetails:")
                    for key, value in result.details.items():
                        if isinstance(value, dict):
                            click.echo(f"  {key}:")
                            for sub_key, sub_value in value.items():
                                click.echo(f"    {sub_key}: {sub_value}")
                        else:
                            click.echo(f"  {key}: {value}")
            else:
                click.secho("❌ Failed!", fg="red", bold=True)
                click.echo(f"Message: {result.message}")
                if result.error:
                    click.echo(f"Error: {result.error}")

        # Exit with appropriate code
        sys.exit(0 if result.success else 1)

    except click.BadParameter as e:
        click.secho(f"❌ Invalid parameter: {str(e)}", fg="red")
        logger.error(f"Invalid parameter: {str(e)}")
        sys.exit(1)
    except Exception as e:
        click.secho(f"❌ Error: {str(e)}", fg="red")
        logger.error(f"CLI error: {str(e)}", exc_info=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information"""
    click.echo("BlackDuck AI Command v1.0.0")
    click.echo("Platform-agnostic BlackDuck initialization for Claude, Copilot, and more")


def main():
    """Entry point for CLI"""
    cli()


if __name__ == "__main__":
    main()
