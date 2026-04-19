#!/usr/bin/env bash
set -euox pipefail

if [[ ! -f /etc/os-release ]]; then
    echo "Cannot determine OS (missing /etc/os-release). Exiting."
    exit 1
fi

source /etc/os-release

if [[ "${ID:-}" != "arch" && "${ID_LIKE:-}" != "arch" ]]; then
    echo "Not Arch Linux (ID=${ID:-unknown}). Exiting."
    exit 0
fi

if command -v paru &> /dev/null; then
    echo "paru is already installed. Exiting."
    exit 0
fi

read -p "paru AUR helper is not installed. Do you want to install it? (Y/N) " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Skipping paru installation."
    exit 0
fi

echo "Installing paru AUR helper..."

sudo pacman -S --needed base-devel git

temp_dir="$(mktemp -d)"
trap 'rm -rf "$temp_dir"' EXIT

git clone https://aur.archlinux.org/paru.git "$temp_dir/paru"
cd "$temp_dir/paru"
makepkg -si

sudo pacman -Rns $(pacman -Qdtq)
