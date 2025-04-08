#!/usr/bin/env bash

[ -z "$XDG_DATA_HOME" ] && warn "XDG_DATA_HOME is not set" "$BASH_SOURCE" "$LINENO"
[ -z "$NVM_DIR" ] && warn "NVM_DIR is not set" "$BASH_SOURCE" "$LINENO"

# Cargo: Rust build system
if [ -d "$XDG_DATA_HOME/cargo" ]; then
    # shellcheck source="$XDG_DATA_HOME/cargo/env"
    . "$XDG_DATA_HOME/cargo/env"
fi

# Nvm: Node version manager
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Jetbrains Toolbox App
if [ -d "$XDG_DATA_HOME/JetBrains/Toolbox/scripts" ] && ! echo "$PATH" | grep -q "$XDG_DATA_HOME/JetBrains/Toolbox/scripts"; then
    export PATH="$PATH:$XDG_DATA_HOME/JetBrains/Toolbox/scripts"
fi

# pyenv: Python version manager
# command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
