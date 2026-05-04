#!/usr/bin/env bash

warn() {
    local message="$1"
    local file="$2"
    local line="$3"

    printf "Warning: %s at %s:%s\n" "$message" "$file" "$line"
}

activate_venv() {
    local folder_name
    folder_name=${1:-".venv"}

    . "$folder_name/bin/activate"
}

symlink_to_localbin() {
    if [ -z "$1" ]; then
        echo "Error: No file path provided."
        return 1
    fi

    local source_file_path
    source_file_path=$(realpath "$1")

    if [ ! -e "$source_file_path" ]; then
        echo "Error: File '$source_file_path' does not exist."
        return 1
    fi

    local target_filename
    target_filename=$(basename "$source_file_path")

    local target_dir
    target_dir="$HOME/.local/bin"
    mkdir -p "$target_dir"

    ln -s "$source_file_path" "$target_dir/$target_filename"
    echo "Symlink created: $target_dir/$target_filename -> $source_file_path"
}

uv_shell() {
    uv run --no-project "$SHELL"
}

upgrade_node() {
    nvm install node --reinstall-packages-from=node
}

clean_apt_cache() {
    if ! command -v apt &> /dev/null; then
        warn "apt command not found. This function is intended for Debian-based systems." "${BASH_SOURCE[0]}" "${BASH_LINENO[0]}"
        return 1
    fi

    sudo apt clean
    sudo rm -r /var/lib/apt/lists/*
    sudo apt update
    sudo dpkg --configure -a
    sudo apt install -f
    sudo apt full-upgrade
    sudo apt autoremove --purge
}
