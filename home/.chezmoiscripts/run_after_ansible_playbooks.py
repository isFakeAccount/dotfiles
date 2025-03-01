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
    PLAYBOOKS: dict[str, PlaybookInfo] = {}

    for ansible_playbook in sorted(
        (CHEZMOI_DIR / "home" / "ansible_playbooks").iterdir()
    ):
        if "setup" not in ansible_playbook.name:
            continue

        playbook: PlaybookInfo = {
            "filename": ansible_playbook.name,
            "sudo": True if "become" in ansible_playbook.name else False,
        }
        PLAYBOOKS[ansible_playbook.name] = playbook

    selected = questionary.checkbox(
        "Select the playbooks to run:",
        choices=list(PLAYBOOKS.keys()),
        instruction="If flatpak is not installed on system, run the 1_flatpak_setup__become.yaml",
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
