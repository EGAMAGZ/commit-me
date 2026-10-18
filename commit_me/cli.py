"""Command-line entry point for commit-me."""

import pathlib

import rich_click as click
from rich.console import Console

from commit_me.ai import generate_commit_message
from commit_me.exceptions import (
    MissingCliError,
    RepoWithoutChangesError,
    NoGitRepoError,
)
from commit_me.util.command import check_required_clis, create_commit, has_changes


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=pathlib.Path.cwd(),
)
@click.option("-p", "--preview", is_flag=True)
def commit_me_cli(directory: pathlib.Path, preview: bool) -> None:
    """Commit-me cli entrypoint

    Args:
        path: Existing directory to run against.
        preview: Whether to preview the commit without applying it.
    """
    try:
        clis = check_required_clis()

        contains_changes = has_changes(directory)
        if not contains_changes:
            raise RepoWithoutChangesError

        console = Console()
        with console.status("Calling opencode") as status:
            commit_message = generate_commit_message(
                opencode_binary=clis["opencode"]["path"],
                directory=directory,
                on_start=lambda: status.update("Starting opencode"),
                on_thinking=lambda: status.update("Opencode is thinking..."),
                on_progress=lambda e: None,
                on_finish=lambda: status.update("Finish"),
            )

        create_commit(
            message=commit_message,
            directory=directory,
            preview=preview,
        )
    except MissingCliError as exception:
        click.echo(exception)
    except RepoWithoutChangesError as exception:
        click.echo(exception)
    except NoGitRepoError as exception:
        click.echo(exception)


if __name__ == "__main__":
    commit_me_cli()
