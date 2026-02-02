#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum, StrEnum
from pathlib import Path
from platform import freedesktop_os_release
from typing import Literal

import questionary
import yaml
from platformdirs import user_data_path
from questionary import Choice, Style

CHEZMOI_DIR = user_data_path("chezmoi", False)


class LinuxDistroBase(Enum):
    DEBIAN = "debian"
    FEDORA = "fedora"
    ARCH = "arch"


class PackageInstallMethod(StrEnum):
    SYSTEM_PACKAGE = "system_package"
    FLATPAK = "flatpak"
    SCRIPT = "script"
    PPA = "ppa"


@dataclass
class ScriptPackage:
    name: str
    url: str
    environment_vars: dict[str, str] | None = None
    ansible_vars: dict[str, str] | None = None
    interpreter: Literal["bash", "python3"] = "bash"


@dataclass
class LinuxPackage:
    name: str
    method: PackageInstallMethod
    root: bool = True
    script_extra: ScriptPackage = None


def get_linux_distro_base() -> LinuxDistroBase:
    """Determines the base Linux distribution type.

    :return: An instance of LinuxDistroBase representing the base distro.
    """
    os_release = freedesktop_os_release()
    distro_id = os_release.get("ID_LIKE") or os_release.get("ID") or ""

    if "debian" in distro_id.lower():
        return LinuxDistroBase.DEBIAN
    elif "fedora" in distro_id.lower() or "rhel" in distro_id.lower():
        return LinuxDistroBase.FEDORA
    elif "arch" in distro_id.lower():
        return LinuxDistroBase.ARCH
    else:
        raise ValueError("Unsupported or unrecognized Linux distribution.")


def flatpak_install_wizard(
    packages_dict: dict[str, list[str]], method: Literal["System", "User"]
) -> list[LinuxPackage]:
    """Reads the flatpak apps config and prompts the user to select apps to install.

    :return: A set of selected flatpak app identifiers.
    """
    menu_style = Style(
        [
            ("menu_header", "bold"),
            ("selected", "bold fg:green"),
        ]
    )

    flattened_choices = []

    for packages_category, packages_list in packages_dict.items():
        flattened_choices.append(
            Choice(
                title=[
                    ("class:menu_header", packages_category.capitalize()),
                ],
                value=packages_category,
            )
        )
        for item in packages_list:
            flattened_choices.append(Choice(title=f"   {item}", value=item))

    selected_items = questionary.checkbox(
        "Select the packages to install:", choices=flattened_choices, style=menu_style
    ).ask()

    unique_selection = set()
    for selection in selected_items:
        if selection in packages_dict:
            unique_selection.update(packages_dict[selection])
        else:
            unique_selection.add(selection)

    return [
        LinuxPackage(
            name=package_name,
            method=PackageInstallMethod.FLATPAK,
            root=False if method == "User" else True,
            script_extra=None,
        )
        for package_name in unique_selection
    ]


def system_package_wizard(packages_dict: dict[str, list[str]]) -> list[LinuxPackage]:
    menu_style = Style(
        [
            ("menu_header", "bold"),
            ("selected", "bold fg:green"),
        ]
    )

    flattened_choices = []

    for package_category, packages_names in packages_dict.items():
        flattened_choices.append(
            Choice(
                title=[
                    ("class:menu_header", package_category.capitalize()),
                ],
                value=package_category,
            )
        )
        for package_name in packages_names.keys():
            flattened_choices.append(
                Choice(title=f"   {package_name}", value=package_name)
            )

    selected_items = questionary.checkbox(
        "Select the packages to install:", choices=flattened_choices, style=menu_style
    ).ask()

    unique_selection = set()
    for selection in selected_items:
        if selection in packages_dict:
            unique_selection.update(packages_dict[selection])
        else:
            unique_selection.add(selection)

    # Converts the selection list to list of LinuxPackages so it is easier
    # use them later when writing Ansible playbooks.
    distro_packages = []
    for package_category, packages_names in packages_dict.items():
        for package_name, package_metadata in packages_names.items():
            if package_name not in unique_selection:
                continue

            current_distro = get_linux_distro_base()
            installation_type = package_metadata.get(
                current_distro.value, package_metadata["default"]
            )
            if installation_type["method"] == PackageInstallMethod.SCRIPT:
                # The script method is
                distro_packages.append(
                    LinuxPackage(
                        name=package_name,
                        method=PackageInstallMethod.SCRIPT,
                        root=False,
                        script_extra=installation_type["script"],
                    )
                )

            else:
                distro_packages.append(
                    LinuxPackage(
                        name=installation_type[installation_type["method"]],
                        method=PackageInstallMethod(installation_type["method"]),
                        root=True,
                        script_extra=None,
                    )
                )
    return distro_packages


def generate_ansible_playbook_for_packages(
    packages: list[LinuxPackage], playbook_path: Path
):
    """Generates an Ansible playbook to install the given packages.

    :param packages: List of LinuxPackage instances to install.
    :param playbook_path: Path where the generated playbook will be saved.
    """

    flatpak_install_user_task = {
        "name": "Install User Flatpak packages",
        "become": False,
        "community.general.flatpak": {
            "name": [],
            "method": "user",
            "state": "present",
        },
    }

    flatpak_install_system_task = {
        "name": "Install System Flatpak packages",
        "become": True,
        "community.general.flatpak": {
            "name": [],
            "method": "system",
            "state": "present",
        },
    }

    syspkg_install_task = {
        "name": "Install System packages",
        "become": True,
        "ansible.builtin.package": {
            "name": [],
            "state": "present",
        },
    }

    for package in packages:
        if package.method == PackageInstallMethod.FLATPAK:
            if package.root:
                flatpak_install_system_task["community.general.flatpak"]["name"].append(
                    package.name
                )
            else:
                flatpak_install_user_task["community.general.flatpak"]["name"].append(
                    package.name
                )
        elif package.method == PackageInstallMethod.SYSTEM_PACKAGE:
            syspkg_install_task["ansible.builtin.package"]["name"].append(package.name)

    playbook_content = [
        {
            "name": "Install selected packages",
            "hosts": "localhost",
            "connection": "local",
            "gather_facts": True,
            "tasks": [
                {
                    "name": "Add Flathub remote at user level if not already added",
                    "become": False,
                    "ansible.builtin.command": {
                        "cmd": "flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"
                    },
                },
                {
                    "name": "Add Flathub remote at system level if not already added",
                    "become": True,
                    "ansible.builtin.command": {
                        "cmd": "flatpak remote-add --system --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"
                    },
                },
            ],
        },
    ]

    if flatpak_install_user_task["community.general.flatpak"]["name"]:
        playbook_content[0]["tasks"].append(flatpak_install_user_task)

    if flatpak_install_system_task["community.general.flatpak"]["name"]:
        playbook_content[0]["tasks"].append(flatpak_install_system_task)

    if syspkg_install_task["ansible.builtin.package"]["name"]:
        playbook_content[0]["tasks"].append(syspkg_install_task)

    with playbook_path.open("w") as fp:
        yaml.safe_dump(
            playbook_content,
            fp,
            explicit_start=True,
            sort_keys=False,
        )


def main():
    playbooks_dir = CHEZMOI_DIR / "home" / "ansible_playbooks"

    flatpak_user_install_file = playbooks_dir / "flatpak_apps_user.yaml"
    with flatpak_user_install_file.open("r") as fp:
        file_content = yaml.safe_load(fp)
        flatpak_user_packages = flatpak_install_wizard(
            packages_dict=file_content, method="User"
        )

    flatpak_sys_install_file = playbooks_dir / "flatpak_apps_system.yaml"
    with flatpak_sys_install_file.open("r") as fp:
        file_content = yaml.safe_load(fp)
        flatpak_sys_packages = flatpak_install_wizard(
            packages_dict=file_content, method="System"
        )

    system_install_file = playbooks_dir / "system_apps.yaml"
    with system_install_file.open("r") as fp:
        file_content = yaml.safe_load(fp)
        system_packages = system_package_wizard(packages_dict=file_content)

    combined_packages = [
        *flatpak_user_packages,
        *flatpak_sys_packages,
        *system_packages,
    ]

    generate_ansible_playbook_for_packages(
        combined_packages,
        playbooks_dir / "flatpak_system_packages_become_playbook.yaml",
    )


if __name__ == "__main__":
    main()
