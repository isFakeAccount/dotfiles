#!/usr/bin/env bash

export XDG_CACHE_HOME="$HOME/.cache"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"

export _JAVA_OPTIONS="-Djava.util.prefs.userRoot=$XDG_CONFIG_HOME/java"
export ANDROID_HOME="$XDG_DATA_HOME/android/Sdk"
export ANDROID_USER_HOME="$XDG_DATA_HOME/android"
export ANSIBLE_HOME="$XDG_DATA_HOME/ansible"
export CARGO_HOME="$XDG_DATA_HOME/cargo"
export CUDA_CACHE_PATH="$XDG_CACHE_HOME/nv"
export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"
export DOTNET_CLI_HOME="$XDG_CACHE_HOME/dotnet"
export GNUPGHOME="$XDG_DATA_HOME/gnupg"
export GOPATH="$XDG_DATA_HOME"/go
export GRADLE_USER_HOME="$XDG_DATA_HOME/gradle"
export HISTFILE="$XDG_STATE_HOME/bash/history"
export LESSHISTFILE="$XDG_STATE_HOME/less/history"
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"
export NVM_DIR="$XDG_DATA_HOME/nvm"
export PLATFORMIO_CORE_DIR="$XDG_DATA_HOME/platformio"
export PYENV_ROOT="$XDG_DATA_HOME/pyenv"
export PYTHONSTARTUP="$XDG_CONFIG_HOME/python/pythonrc"
export RUSTUP_HOME="$XDG_DATA_HOME/rustup"
export XCURSOR_PATH="/usr/share/icons:$XDG_DATA_HOME/icons"
export ZVM_PATH="$XDG_DATA_HOME/zvm"

alias wget=wget --hsts-file="$XDG_DATA_HOME/wget-hsts"
# nvidia-settings --config="$XDG_CONFIG_HOME/nvidia/settings" this doesn't work for some reason :(
