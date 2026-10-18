# commit-me

[![PyPI version](https://img.shields.io/pypi/v/commit-me.svg)](https://pypi.org/project/commit-me/)
[![PyPI - Python versions](https://img.shields.io/pypi/pyversions/commit-me.svg)](https://pypi.org/project/commit-me/)
[![PyPI downloads](https://img.shields.io/pypi/dm/commit-me.svg)](https://pypi.org/project/commit-me/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/EGAMAGZ/commit-me/actions/workflows/ci.yml/badge.svg)](https://github.com/EGAMAGZ/commit-me/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Generate [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) messages for your staged changes with [opencode](https://opencode.ai) and commit them in one step.

`commit-me` inspects the staged diff of a Git repository, asks an opencode session for a single accurate commit message, and creates the commit. It never invents metadata and will not modify files or history.

## Requirements

- Python 3.14+
- [Git](https://git-scm.com/) on your `PATH`
- [opencode](https://opencode.ai) on your `PATH`

## Install

With [uv](https://docs.astral.sh/uv/):

```sh
uv tool install commit-me
```

With [pipx](https://pipx.pypa.io/):

```sh
pipx install commit-me
```

With pip:

```sh
pip install commit-me
```

## Usage

Stage your changes, then run:

```sh
python -m commit_me.cli
```

Options:

| Option | Description |
| --- | --- |
| `-p`, `--preview` | Show the proposed message and ask for confirmation before committing. |
| `-m`, `--model` | opencode model to use (default: `opencode/big-pickle`). |
| `DIRECTORY` | Path to the Git repository (default: current directory). |

Preview a message without committing:

```sh
python -m commit_me.cli --preview
```

## Development

```sh
uv sync --group dev
uv run ty check
uv run ruff check .
uv run ruff format --check .
```

## License

MIT — see [LICENSE](LICENSE).
