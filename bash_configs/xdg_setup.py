from os import getenv
from pathlib import Path
from typing import NamedTuple
from git import GitConfigParser


class XDGPath(NamedTuple):
    path: Path
    is_file: bool
    mode: int


def create_global_gitconfig():
    programming_dir = Path.home() / "Programming"
    ifinclude_paths: list[Path] = []
    for subdir in programming_dir.iterdir():
        ifinclude_paths.append(subdir.resolve())

    git_config_path = (
        Path(__file__).parent.parent.resolve() / ".config" / "git" / "config"
    )
    with GitConfigParser(git_config_path, read_only=False) as config_parser:
        config_parser.set_value("init", "defaultBranch", "master")

        for ifinclude_path in ifinclude_paths:
            config_parser.set_value(
                f'includeIf "gitdir:{ifinclude_path}/"',
                "path",
                f"{ifinclude_path}/.gitconfig",
            )


def create_xdg_structure(xdg_paths: list[XDGPath]):
    for xdg_path in xdg_paths:
        if xdg_path.is_file:
            xdg_path.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            xdg_path.path.touch(mode=xdg_path.mode, exist_ok=True)
            print(f"Created file: {xdg_path.path}")
        else:
            xdg_path.path.mkdir(mode=xdg_path.mode, parents=True, exist_ok=True)
            print(f"Created directory: {xdg_path.path}")


def main():
    xdg_data_home = Path(getenv("XDG_DATA_HOME", Path.home() / ".local/share"))
    xdg_state_home = Path(getenv("XDG_STATE_HOME", Path.home() / ".local/state"))

    xdg_paths = [
        XDGPath(path=xdg_state_home / "bash" / "history", is_file=True, mode=0o600),
        XDGPath(path=xdg_state_home / "less" / "history", is_file=True, mode=0o600),
        XDGPath(path=xdg_data_home / "gnupg", is_file=False, mode=0o700),
        XDGPath(path=xdg_data_home / "nvm", is_file=False, mode=0o700),
    ]

    create_xdg_structure(xdg_paths)
    create_global_gitconfig()


if __name__ == "__main__":
    main()
