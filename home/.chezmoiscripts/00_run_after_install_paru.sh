#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f /etc/os-release ]]; then
    echo "Cannot determine OS (missing /etc/os-release). Exiting."
    exit 1
fi

source /etc/os-release

if [[ "${ID:-}" != "arch" ]]; then
    echo "Not Arch Linux (ID=${ID:-unknown}). Exiting."
    exit 0
fi

if command -v paru &> /dev/null; then
    echo "paru is already installed. Exiting."
    exit 0
fi

echo "Installing paru AUR helper..."

sudo pacman -S --needed base-devel git

temp_dir="$(mktemp -d)"
trap 'rm -rf "$temp_dir"' EXIT

git clone https://aur.archlinux.org/paru.git "$temp_dir/paru"
cd "$temp_dir/paru"
makepkg -si
