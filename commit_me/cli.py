import pathlib

import click


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=pathlib.Path.cwd(),
)
@click.option("-p", "--preview", is_flag=True)
def commit_me_cli(path: pathlib.Path, preview: bool) -> None:
    click.echo(path)
    click.echo(preview)


if __name__ == "__main__":
    commit_me_cli()
