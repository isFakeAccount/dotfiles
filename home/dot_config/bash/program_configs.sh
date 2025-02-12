#!/usr/bin/env bash

# Cargo: Rust build system
source "$XDG_DATA_HOME/cargo/env"

# Nvm: Node version manager
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"                   # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion

# UV: Python version manager
export UV_PYTHON_PREFERENCE='system'
