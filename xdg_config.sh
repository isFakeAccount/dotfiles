# Setting up XDG Env Var
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"

export CARGO_HOME="$XDG_DATA_HOME"/cargo
export CUDA_CACHE_PATH="$XDG_CACHE_HOME"/nv
export DOCKER_CONFIG="$XDG_CONFIG_HOME"/docker
export GRADLE_USER_HOME="$XDG_DATA_HOME"/gradle
export HISTFILE="${XDG_STATE_HOME}"/bash/history
export LESSHISTFILE="$XDG_STATE_HOME"/less/history
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME"/npm/npmrc
export NVM_DIR="$XDG_DATA_HOME"/nvm
export PLATFORMIO_CORE_DIR="$XDG_DATA_HOME"/platformio
export PYENV_ROOT="$XDG_DATA_HOME"/pyenv
export RUSTUP_HOME="$XDG_DATA_HOME"/rustup
export XCURSOR_PATH=/usr/share/icons:$XDG_DATA_HOME/icons

alias wget=wget --hsts-file="$XDG_DATA_HOME/wget-hsts"
# nvidia-settings --config="$XDG_CONFIG_HOME"/nvidia/settings

