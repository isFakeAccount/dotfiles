#!/usr/bin/env bash

activate_venv() {
    local folder_name
    folder_name=${1:-".venv"}
    
    source "$folder_name/bin/activate"
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
