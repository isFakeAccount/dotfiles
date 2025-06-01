#!/usr/bin/env python3
from pathlib import Path
from posixpath import expanduser

from git import GitConfigParser
from platformdirs import user_config_path, user_data_path

CHEZMOI_DIR = user_data_path("chezmoi", False)


def create_local_git_config(account_name: str, email: str) -> Path:
    """
    Creates a local .gitconfig file for a given account in a generated directory based on the account name.

    :param account_name: The name for this Git account.
    :param email: The email for this Git account.
    :return: The path to the created .gitconfig file.
    """

    git_configs_dir = CHEZMOI_DIR / "git_configs" / account_name.replace(" ", "_")
    git_configs_dir.mkdir(parents=True, exist_ok=True)
    gitconfig_path = git_configs_dir / ".gitconfig"

    with GitConfigParser(gitconfig_path, read_only=False) as account_config:
        account_config.set_value("user", "name", account_name)
        account_config.set_value("user", "email", email)

    return gitconfig_path


def create_symlinks_for_all_gitconfigs() -> list[Path]:
    """
    Loops through all directories in git_configs and prompts the user to provide
    a file path for creating a symlink to each .gitconfig. Returns a list of paths
    where the symlinks have been created.

    :return: List of paths to the directories where the symlinks have been created.
    """
    git_configs_base_dir = CHEZMOI_DIR / "git_configs"
    symlink_paths: set[Path] = set()

    for account_dir in git_configs_base_dir.iterdir():
        if not account_dir.is_dir() or not (account_dir / ".gitconfig").exists():
            continue

        target_gitconfig_path = account_dir / ".gitconfig"
        symlink_path = Path(
            input(
                f"Enter the file path where you want to create the symlink for {account_dir.name}_gitconfig: "
            ).strip()
        ).expanduser().absolute()
        symlink_gitconfig_path = symlink_path / ".gitconfig"
        if symlink_gitconfig_path.exists() or symlink_gitconfig_path.is_symlink():
            symlink_gitconfig_path.unlink()

        symlink_gitconfig_path.symlink_to(target_gitconfig_path)
        print(f"Symlinked {symlink_gitconfig_path} -> {target_gitconfig_path}")

        symlink_paths.add(symlink_path)

    return list(symlink_paths)


def create_global_gitconfig(git_account_dirs: list[Path]) -> None:
    """
    This function creates a global Git config with includeIf set to correct paths.

    It assumes that git_account_dirs contains the paths to the directories with .gitconfig files.
    It adds includeIf entries to the global Git config based on these directories.

    :param git_account_dirs: List of paths to directories containing .gitconfig files.
    """
    git_global_config_dir = user_config_path("git", False)
    git_global_config_dir.mkdir(parents=True, exist_ok=True)

    git_config_path = git_global_config_dir / "config"
    git_config_path.touch(exist_ok=True)

    with GitConfigParser(git_config_path, read_only=False) as config_parser:
        # Set default branch to 'master'
        config_parser.set_value("init", "defaultBranch", "master")
        # Enable GPG signing for commits
        config_parser.set_value("commit", "gpgSign", "true")
        # Enable rebase by default when pulling
        config_parser.set_value("pull", "rebase", "true")
        # Add a useful alias for a better log view
        config_parser.set_value("alias", "lg", "log --oneline --graph --decorate --all")
        # Set the default editor to Neovim
        config_parser.set_value("core", "editor", "code")
        # Improve diff readability with word-based coloring
        config_parser.set_value("diff", "colorMoved", "zebra")
        # Enable auto-completion for Git commands
        config_parser.set_value("completion", "bash", "true")
        # Set submodule to update automatically on git pull
        config_parser.set_value("submodule", "recurse", True)

        for account_dir in git_account_dirs:
            if account_dir.is_dir() and (account_dir / ".gitconfig").exists():
                symlink_path = account_dir / ".gitconfig"

                config_parser.set_value(
                    f'includeIf "gitdir:{account_dir}/"',
                    "path",
                    str(symlink_path),
                )

    print("Updated global Git config with includeIf settings for .gitconfig files.")


def main() -> None:
    num_accounts = int(
        input(
            "How many Git accounts do you want to set up? (enter 0 to skip this step): "
        )
    )

    if num_accounts == 0:
        print("Skipping Git Account setup.")
        return None

    for i in range(num_accounts):
        print(f"\nSetting up Git account {i + 1}:")
        name = input("Enter the name for this Git account: ").strip()
        email = input(f"Enter the email for {name}: ").strip()
        create_local_git_config(name, email)

    git_account_dirs = create_symlinks_for_all_gitconfigs()
    create_global_gitconfig(git_account_dirs)


if __name__ == "__main__":
    main()
