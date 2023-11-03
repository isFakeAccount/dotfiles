alias ssha='eval "$(ssh-agent -s)" && ssh-add'
alias cx='clear -x'

tmux_nvim() {
    local session_name=$(basename "$(pwd)")
    if tmux has-session -t "$session_name" 2>/dev/null; then
        tmux attach-session -t "$session_name"
    else
        tmux new-session -s "$session_name" -n nvim -d
        tmux send-keys -t "$session_name" "nvim ." C-m
        tmux attach-session -t "$session_name"
    fi
}

activate_venv() {
    folder_name=${1:-"venv"}
    source "$folder_name"/bin/activate
}
