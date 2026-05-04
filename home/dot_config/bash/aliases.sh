#!/usr/bin/env bash

# Run ssh agent and add ssh file
alias ssha='eval "$(ssh-agent -s)" && ssh-add'

# Clear screen alias
alias cls='clear'
alias cx='clear -x'

# Use git diff instead of diff
alias diff='git diff --no-index'

# Create a new file and make it executable
alias touchx='touch "$1" && chmod u+x "$1"'

# Extract .tar.gz, .tar.xz, .tar.bz2, and .zip files
alias extract_tar='tar -xvf'
alias extract_gz='tar -xzvf'
alias extract_bz2='tar -xjvf'
alias extract_xz='tar -xJvf'
alias extract_zip='unzip'

# Program Alias
if command -v rg &> /dev/null; then
    alias grep='rg'
fi

if command -v eza &> /dev/null; then
    # Replace ls with eza
    alias ls='eza --color=always --group-directories-first'
    alias la='eza -a --color=always --group-directories-first --header'
    alias ll='eza -lagH --color=always --group-directories-first --header'
    alias lt='eza -aT --color=always --group-directories-first --header -L'
    alias l.="eza -a | grep -e '^\.'"
fi

# Stop after sending count ECHO_REQUEST packets #
alias ping='ping -c 5'
# Do not wait interval 1 second, go fast #
alias fastping='ping -c 100 -i .2'

# List all TCP/UDP ports
alias ports='netstat -tulanp'

# rsync to copy files to removable media and fsync each file
alias rsync_to_media='rsync -av --progress --fsync'

# Print $PATH Variable
alias path='echo -e ${PATH//:/\\n}'

# Time related alias
alias now_datetime='date -u +%Y-%m-%dT%H:%M:%S%Z'
alias now_12='date +"%I:%M:%S %p"'

# uv configs
alias uvr='uv run'
