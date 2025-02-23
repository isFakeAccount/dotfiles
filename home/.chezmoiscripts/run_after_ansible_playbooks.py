#!/usr/bin/env python
import subprocess
from tempfile import TemporaryDirectory
from typing import Any, TypedDict

import ansible_runner
import questionary
from platformdirs import user_data_path

CHEZMOI_DIR = user_data_path("chezmoi", False)


class PlaybookInfo(TypedDict):
    filename: str
    sudo: bool


PLAYBOOKS: dict[str, PlaybookInfo] = {
    "System Setup": {"filename": "system_setup.yaml", "sudo": True},
    "Flatpak Setup": {"filename": "flatpak_setup.yaml", "sudo": True},
    "Python Setup": {"filename": "python_setup.yaml", "sudo": False},
    "Rust Setup": {"filename": "rust_setup.yaml", "sudo": False},
    "Software Dev Setup": {"filename": "dev_setup.yaml", "sudo": True},
    "NVIDIA Setup": {"filename": "nvidia_setup.yaml", "sudo": True},
}


def load_env() -> dict[str, str]:
    import os

    return dict(os.environ)


cached_become_pass = None


def get_become_pass() -> questionary.Question:
    global cached_become_pass

    if cached_become_pass:
        return cached_become_pass

    password_confirmed = False

    while not password_confirmed:
        become_pass = questionary.password("Enter sudo password for ansible:").ask()

        result = subprocess.run(
            ["sudo", "-S", "whoami"],
            input=become_pass + "\n",
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            cached_become_pass = become_pass
            password_confirmed = True
        else:
            print("Incorrect password. Please try again.")

    return become_pass


def run_playbook(
    playbook_name: str, playbook_info: PlaybookInfo, private_data_dir: str
) -> None:
    global cached_become_pass

    playbook_path = (
        CHEZMOI_DIR / "home" / "ansible_playbooks" / playbook_info["filename"]
    )

    runner_args: dict[str, Any] = {
        "private_data_dir": private_data_dir,
        "playbook": str(playbook_path),
        "suppress_env_files": True,
        "verbosity": 2,
        "envvars": load_env(),
    }

    if playbook_info["sudo"]:
        become_pass = become_pass = get_become_pass()
        runner_args["extravars"] = {"ansible_become_pass": str(become_pass)}

    runner = ansible_runner.run(**runner_args)

    if runner.status == "failed":
        print(f"Playbook {playbook_name} failed.")
    else:
        print(f"Playbook {playbook_name} completed successfully.")


def main():
    selected = questionary.checkbox(
        "Select the playbooks to run:", choices=list(PLAYBOOKS.keys())
    ).ask()

    if not selected:
        print("No playbooks selected. Exiting.")
        return

    with TemporaryDirectory() as temp_dir:
        for playbook_name in selected:
            run_playbook(
                playbook_name=playbook_name,
                playbook_info=PLAYBOOKS[playbook_name],
                private_data_dir=temp_dir,
            )


if __name__ == "__main__":
    main()
