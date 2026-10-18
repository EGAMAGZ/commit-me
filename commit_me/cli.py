"""Command-line entry point for commit-me."""

import pathlib

import rich_click as click
from rich.console import Console

from commit_me.ai import generate_commit_message
from commit_me.exceptions import MissingCliError, NoGitRepoError, NoStagedChangesError
from commit_me.util.command import check_required_clis, create_commit, has_stage_changes


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=pathlib.Path.cwd(),
)
@click.option("-p", "--preview", is_flag=True)
def commit_me_cli(directory: pathlib.Path, preview: bool) -> None:
    """Generate a Conventional Commit message with opencode and commit it.

    Args:
        directory: Existing directory of the Git repository to commit in.
        preview: Whether to preview the commit message before committing.
    """
    try:
        clis = check_required_clis()

        contains_stage = has_stage_changes(directory)

        if not contains_stage:
            raise NoStagedChangesError(directory=directory)

        console = Console()
        with console.status("Calling opencode") as status:
            commit_message = generate_commit_message(
                opencode_binary=clis["opencode"]["path"],
                directory=directory,
                on_start=lambda: status.update("Starting opencode"),
                on_thinking=lambda: status.update("Opencode is thinking..."),
                on_progress=lambda _e: None,
                on_finish=lambda: status.update("Done"),
            )

        create_commit(
            message=commit_message,
            directory=directory,
            preview=preview,
        )
    except (MissingCliError, NoGitRepoError, NoStagedChangesError) as exception:
        click.echo(exception, err=True)


if __name__ == "__main__":
    commit_me_cli()
