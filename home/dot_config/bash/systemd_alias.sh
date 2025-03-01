#!/usr/bin/env bash

alias ctl='systemctl'
alias ctl_stop='systemctl stop'
alias ctl_start='systemctl start'
alias ctl_restart='systemctl restart'
alias ctl_status='systemctl status'
alias ctl_enable='systemctl enable'
alias ctl_disable='systemctl disable'
alias ctl_daemon_reload="systemctl daemon-reload"

# Function to start a service and show its status
ctl_strt_sts() {
    if [ "$1" = "--user" ]; then
        shift
        systemctl --user start "$1" && systemctl --user status "$1"
    else
        systemctl start "$1" && systemctl status "$1"
    fi
}

# Function to restart a service and show its status
ctl_restrt_sts() {
    if [ "$1" = "--user" ]; then
        shift
        systemctl --user restart "$1" && systemctl --user status "$1"
    else
        systemctl restart "$1" && systemctl status "$1"
    fi
}

# Function to enable a service and start it, then show its status
ctl_enbl_strt_sts() {
    if [ "$1" = "--user" ]; then
        shift
        systemctl --user enable "$1" && systemctl --user start "$1" && systemctl --user status "$1"
    else
        systemctl enable "$1" && systemctl start "$1" && systemctl status "$1"
    fi
}

# Function to disable a service and stop it, then show its status
ctl_dsbld_stop_sts() {
    if [ "$1" = "--user" ]; then
        shift
        systemctl --user disable "$1" && systemctl --user stop "$1" && systemctl --user status "$1"
    else
        systemctl disable "$1" && systemctl stop "$1" && systemctl status "$1"
    fi
}
