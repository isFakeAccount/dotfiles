#!/usr/bin/env python3

import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, StrEnum
from pathlib import Path
from platform import freedesktop_os_release
from typing import Any, Literal, Self

import questionary
import yaml
from platformdirs import user_data_path
from questionary import Choice, Style

CHEZMOI_DIR = user_data_path("chezmoi", False)


class LinuxDistroBase(Enum):
    ARCH = "arch"
    DEBIAN = "debian"
    FEDORA = "fedora"


class PackageInstallMethod(StrEnum):
    FLATPAK = "flatpak"
    PARU = "paru"
    SCRIPT = "script"
    SYSTEM_PACKAGE = "system_package"


@dataclass
class ScriptPackageMetadata:
    """Metadata required to install a package using a custom script.

    :var url: URL from which the installation script can be downloaded.
    :var environment_vars: Environment variables to be set when executing the installation script.
    :var ansible_vars: Variables exposed to Ansible when running the script-based installation.
    :var preinstall_packages: Optional list of system packages that must be installed before running the script.
    :var post_install_packages: Optional list of system packages that maybe available after running the script if the
        script adds PPA.
    :var interpreter: Interpreter used to execute the script. Supported values are ``"bash"`` and ``"python3"``.

    """

    url: str
    environment_vars: dict[str, str]
    ansible_vars: dict[str, str]
    preinstall_packages: list[str] | None
    post_install_packages: list[str] | None
    interpreter: Literal["bash", "python3"] = "bash"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            url=data["url"],
            environment_vars=data.get("environment", {}),
            ansible_vars=data.get("vars", {}),
            preinstall_packages=None,  # TODO: Add this feature later.
            post_install_packages=data.get("post_install_packages", None),
            interpreter=data.get("interpreter", "bash"),
        )


@dataclass
class LinuxPackage:
    """Class representing a linux package and how to install the package.

    :var become: Indicates if package needs elevated privileges to install.
    :var display_name: Display name for the package.
    :var executable_name: Name of the executable that will be available on the PATH after the installation of the
        package.
    :var package_name: Name of the package used by the remote repositories.
    :var method: Installation method used for this package.
    :var script_extra: If installation method is script then this will contain the necessary information to install via
        script.

    """

    become: bool
    display_name: str
    executable_name: str
    package_name: str
    method: PackageInstallMethod
    script_extra: ScriptPackageMetadata | None

    @classmethod
    def from_dict(cls, display_name: str, data: dict[str, Any]) -> Self:
        method = PackageInstallMethod(data["method"])
        package_name = data[method] if method != PackageInstallMethod.SCRIPT else data["executable_name"]
        return cls(
            display_name=display_name,
            package_name=package_name,
            executable_name=data["executable_name"],
            method=method,
            become=data.get("become", False),
            script_extra=ScriptPackageMetadata.from_dict(data["script"]) if method == PackageInstallMethod.SCRIPT else None,
        )

    @classmethod
    def to_flatpak_list(cls, package_names: Sequence[str], become: bool) -> list[Self]:
        return [
            cls(
                display_name=package_name,
                package_name=package_name,
                executable_name=package_name,
                method=PackageInstallMethod.FLATPAK,
                become=become,
                script_extra=None,
            )
            for package_name in package_names
        ]


def get_linux_distro_base() -> LinuxDistroBase:
    """Determines the base Linux distribution type.

    :returns: An instance of LinuxDistroBase representing the base distro.

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


def make_syspkg_install_task(linux_package_names: list[str], become: bool) -> dict[str, object]:
    """Create an Ansible task for installing system packages.

    :param linux_package_names: A list of Linux package names to install.
    :param become: Whether to run the task with privilege escalation. This should typically be ``True`` for system
        packages.

    :returns: A dictionary representing an Ansible task using ``ansible.builtin.package``.

    """
    return {
        "name": "Install System packages",
        "become": become,
        "ansible.builtin.package": {
            "name": linux_package_names,
            "state": "present",
        },
    }


def make_flatpak_install_task(linux_packages: list[LinuxPackage], become: bool) -> dict[str, object]:
    """Create an Ansible task for installing Flatpak packages.

    The Flatpak installation method is derived from ``become``: - ``become=True`` → system-wide installation -
    ``become=False`` → per-user installation

    :param linux_packages: A list of Flatpak LinuxPackage objects to install.
    :param become: Whether to install Flatpaks system-wide (``True``) or for the current user (``False``).

    :returns: A dictionary representing an Ansible task using ``community.general.flatpak``.

    """
    return {
        "name": f"Install {'System' if become else 'User'} Flatpak packages",
        "become": become,
        "community.general.flatpak": {
            "name": [pkg.package_name for pkg in linux_packages],
            "method": "system" if become else "user",
            "state": "present",
        },
    }


def make_script_install_task(
    linux_package: LinuxPackage,
    script_pkg: ScriptPackageMetadata,
) -> list[dict[str, Any]]:
    """Generate an Ansible task list to install a Linux package via a script, optionally followed by post-install system packages.

    :param linux_package: Linux package metadata.
    :param script_pkg: Script package metadata.

    :returns: List of Ansible task dictionaries.

    """
    temp_sh_path = tempfile.TemporaryDirectory(prefix=f"{linux_package.package_name}_installer_", delete=False)

    check_step = {
        "name": f"Check if {linux_package.package_name} is already installed",
        "ansible.builtin.shell": {
            "cmd": f"command -v {linux_package.executable_name}",
        },
        "register": f"{linux_package.package_name}_check",
        "ignore_errors": True,
        "args": {
            "executable": "/bin/bash",
        },
    }

    download_step = {
        "name": f"Download {linux_package.package_name} script installer",
        "get_url": {
            "url": script_pkg.url,
            "dest": temp_sh_path.name + "/install.sh",
            "mode": "0755",
            "force": "yes",
        },
        "when": f"{linux_package.package_name}_check.failed",
    }

    install_step = {
        "name": f"Install {linux_package.package_name} via script installer",
        "ansible.builtin.shell": {
            "cmd": temp_sh_path.name + "/install.sh",
        },
        "args": {
            "executable": f"/bin/{script_pkg.interpreter}",
        },
        "environment": script_pkg.environment_vars,
        "vars": script_pkg.ansible_vars,
        "when": f"{linux_package.package_name}_check.failed",
    }

    if script_pkg.post_install_packages is None:
        return [check_step, download_step, install_step]

    post_install_step = make_syspkg_install_task(linux_package_names=script_pkg.post_install_packages, become=True)
    post_install_step["when"] = f"{linux_package.package_name}_check.failed"
    return [check_step, download_step, install_step, post_install_step]


def package_selection_menu(
    packages_dict: dict[str, list[str | dict[str, Any]]],
) -> set[str]:
    """Generates selection menu from the packages dict and returns the user selection.

    :param packages_dict: A dict containing packages category as key and list of packages names as values.

    :returns: List of packages selected by the user.

    """

    menu_style = Style(
        [
            ("menu_header", "bold"),
            ("selected", "bold fg:green"),
        ]
    )

    flattened_choices = ["All (all packages below)"]
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

    selected_items = questionary.checkbox("Select the packages to install:", choices=flattened_choices, style=menu_style).ask()

    unique_selection = set()

    # If user selects all packages then dump all packages into selection
    if "All (all packages below)" in selected_items:
        for packages_list in packages_dict.values():
            unique_selection.update(packages_list)
        return unique_selection

    for selection in selected_items:
        # Handles if a category is selected
        if selection in packages_dict:
            unique_selection.update(packages_dict[selection])
        else:
            # Handles individual packages
            unique_selection.add(selection)

    return unique_selection


def flatpak_install_wizard(packages_dict: dict[str, list[str]], method: Literal["System", "User"]) -> list[LinuxPackage]:
    """Reads the flatpak apps config and prompts the user to select apps to install.

    :returns: A set of selected flatpak app identifiers.

    """
    selected_packages = package_selection_menu(packages_dict)
    return LinuxPackage.to_flatpak_list(package_names=selected_packages, become=method == "System")


def system_package_wizard(packages_dict: dict[str, list[str]]) -> list[LinuxPackage]:
    unique_selection = package_selection_menu(packages_dict)
    # Converts the selection list to list of LinuxPackages so it is easier
    # use them later when writing Ansible playbooks.
    distro_packages = []
    for packages_names in packages_dict.values():
        for package_display_name, package_metadata in packages_names.items():
            if package_display_name not in unique_selection:
                continue

            current_distro = get_linux_distro_base()
            installation_type = package_metadata.get(current_distro.value, package_metadata["default"])
            distro_packages.append(LinuxPackage.from_dict(display_name=package_display_name, data=installation_type))

    return distro_packages


def generate_ansible_playbook_for_packages(packages: list[LinuxPackage], playbook_path: Path) -> None:
    """Generates an Ansible playbook to install the given packages.

    :param packages: List of LinuxPackage instances to install.
    :param playbook_path: Path where the generated playbook will be saved.

    """

    flatpak_user_packages: list[LinuxPackage] = []
    flatpak_system_packages: list[LinuxPackage] = []
    system_packages: list[LinuxPackage] = []

    scripts_install_tasks: list[dict[str, Any]] = []

    for package in packages:
        if package.method == PackageInstallMethod.FLATPAK:
            if package.become:
                flatpak_system_packages.append(package)
            else:
                flatpak_user_packages.append(package)
        elif package.method == PackageInstallMethod.SYSTEM_PACKAGE:
            system_packages.append(package)
        elif package.method == PackageInstallMethod.SCRIPT:
            scripts_install_tasks.extend(make_script_install_task(package, package.script_extra))

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
                    "ansible.builtin.shell": {"cmd": "flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"},
                },
                {
                    "name": "Add Flathub remote at system level if not already added",
                    "become": True,
                    "ansible.builtin.shell": {"cmd": "flatpak remote-add --system --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo"},
                },
            ],
        },
    ]

    if flatpak_user_packages:
        playbook_content[0]["tasks"].append(make_flatpak_install_task(linux_packages=flatpak_user_packages, become=False))

    if flatpak_system_packages:
        playbook_content[0]["tasks"].append(make_flatpak_install_task(linux_packages=flatpak_system_packages, become=True))

    if system_packages:
        playbook_content[0]["tasks"].append(
            make_syspkg_install_task(
                linux_package_names=[x.package_name for x in system_packages],
                become=True,
            )
        )

    if scripts_install_tasks:
        playbook_content[0]["tasks"].extend(scripts_install_tasks)

    with playbook_path.open("w") as fp:
        yaml.safe_dump(
            playbook_content,
            fp,
            explicit_start=True,
            sort_keys=False,
            indent=4,
            width=1000,
        )


def main():
    playbooks_dir = CHEZMOI_DIR / "home" / "ansible_playbooks"

    flatpak_user_install_file = playbooks_dir / "flatpak_apps_user.yaml"
    with flatpak_user_install_file.open("r") as fp:
        file_content = yaml.safe_load(fp)
        flatpak_user_packages = flatpak_install_wizard(packages_dict=file_content, method="User")

    flatpak_sys_install_file = playbooks_dir / "flatpak_apps_system.yaml"
    with flatpak_sys_install_file.open("r") as fp:
        file_content = yaml.safe_load(fp)
        flatpak_sys_packages = flatpak_install_wizard(packages_dict=file_content, method="System")

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
        playbooks_dir / "universal_install_ansible_become_playbook.yaml",
    )


if __name__ == "__main__":
    main()
