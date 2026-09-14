import click
import pathlib

@click.command()
@click.argument("path", type=click.Path(exists=True, path_type=pathlib.Path))
@click.option("-p", "--preview", is_flag=True)
def commit_me_cli(path: pathlib.Path, preview: bool) -> None:

    pass


if __name__ == "__main__":
    commit_me_cli()
