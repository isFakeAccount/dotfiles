#!/usr/bin/env bash

main() {
    local chezmoi_dir="$HOME/.local/share/chezmoi"
    local python_script="$chezmoi_dir/home/python_scripts/xdg_setup.py"
    local python_executable="$chezmoi_dir/.venv/bin/python"

    echo "Executing: $python_executable $python_script"
    "$python_executable" "$python_script"
}

main
