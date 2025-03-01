#!/usr/bin/env bash

# ===========================================================
# Script: bashenv.sh
# Purpose: Sources XDG-based configuration files to load
# environment variables, functions, aliases, and program settings
# without cluttering the .bashrc, ensuring portability via dotfiles.
# ===========================================================

. "$HOME/.config/bash/xdg_config.sh"
. "$XDG_CONFIG_HOME/bash/complete_alias.sh"
. "$XDG_CONFIG_HOME/bash/functions.sh"
. "$XDG_CONFIG_HOME/bash/aliases.sh"
. "$XDG_CONFIG_HOME/bash/program_configs.sh"
. "$XDG_CONFIG_HOME/bash/systemd_alias.sh"
