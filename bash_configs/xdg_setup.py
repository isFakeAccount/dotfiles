from os import getenv
from pathlib import Path
from typing import NamedTuple


class XDGPath(NamedTuple):
    path: Path
    is_file: bool


def create_xdg_structure(xdg_paths: list[XDGPath]):
    for xdg_path in xdg_paths:
        xdg_path.path.parent.mkdir(parents=True, exist_ok=True)
        if xdg_path.is_file:
            xdg_path.path.touch(exist_ok=True)
            print(f"Created file: {xdg_path.path}")
        else:
            xdg_path.path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {xdg_path.path}")



def main():
    xdg_data_home = Path(getenv("XDG_DATA_HOME", Path.home() / ".local/share"))
    xdg_state_home = Path(getenv("XDG_STATE_HOME", Path.home() / ".local/state"))

    xdg_paths = [
        XDGPath(path=xdg_state_home / "bash" / "history", is_file=True),
        XDGPath(path=xdg_state_home / "less" / "history", is_file=True),
        XDGPath(path=xdg_data_home / "gnupg", is_file=False),
    ]

    create_xdg_structure(xdg_paths)


if __name__ == "__main__":
    main()
