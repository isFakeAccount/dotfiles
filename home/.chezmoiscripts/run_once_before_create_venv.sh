#!/usr/bin/env bash

main() {
    local me
    me=$(basename "$0")
    echo "Running $me"

    local chezmoi_dir="$HOME/.local/share/chezmoi"
    local venv_dir="$chezmoi_dir/.venv"

    if [ ! -d "$venv_dir" ]; then
        python3 -m venv "$venv_dir"
    fi

    source "$venv_dir/bin/activate"
    if [ $? -ne 0 ]; then
        echo "Error: Could not activate virtual environment at $venv_dir" >&2
        exit 1
    fi

    pip install -r "$chezmoi_dir/home/requirements.txt"
}

main
