import os
from pathlib import Path


def create_symbolic_links(dotfiles_repo: Path, xdg_dir: Path):
    config_dir = dotfiles_repo / ".config"

    for item in config_dir.iterdir():
        link_path = xdg_dir / item.name

        if not link_path.exists():
            link_path.symlink_to(item, target_is_directory=True)
            print(f"Created symbolic link: {link_path} -> {item}")
        else:
            print(
                f"Skipped symbolic link creation for {link_path} as it already exists."
            )


def main():
    dotfiles_repo = Path.cwd()
    xdg_config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

    create_symbolic_links(dotfiles_repo, xdg_config_dir)


if __name__ == "__main__":
    main()
