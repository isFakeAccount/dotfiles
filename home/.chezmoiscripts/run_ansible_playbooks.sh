#!/usr/bin/env bash

main() {
    local me
    me=$(basename "$0")
    echo "Running $me"

    local chezmoi_dir="$HOME/.local/share/chezmoi"
    source "$chezmoi_dir/.venv/bin/activate"

    ansible-playbook "$chezmoi_dir/home/ansible_playbooks/flatpak_setup.yaml"
    ansible-playbook "$chezmoi_dir/home/ansible_playbooks/python_setup.yaml" --ask-become-pass
    ansible-playbook "$chezmoi_dir/home/ansible_playbooks/rust_setup.yaml"
    ansible-playbook "$chezmoi_dir/home/ansible_playbooks/system_setup.yaml" --ask-become-pass
}

main "$@"
