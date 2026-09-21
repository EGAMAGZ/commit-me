"""Command-line entry point for commit-me."""

import pathlib

import click

from commit_me.exceptions import MissingCliError
from commit_me.util.command import check_required_clis


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=pathlib.Path.cwd(),
)
@click.option("-p", "--preview", is_flag=True)
def commit_me_cli(path: pathlib.Path, preview: bool) -> None:
    """Commit-me cli entrypoint

    Args:
        path: Existing directory to run against.
        preview: Whether to preview the commit without applying it.
    """
    try:
        check_required_clis()
        click.echo(path)
        click.echo(preview)
    except MissingCliError as exception:
        click.echo(exception)


if __name__ == "__main__":
    commit_me_cli()
