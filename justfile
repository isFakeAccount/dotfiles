# Justfile for easily running commands related to my dotfiles managed with chezmoi.

just-fmt:
    just --fmt --unstable

# Creates python .venv
create-venv:
    python3 -m venv .venv

install-deps:
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt

# Apply all the changes including running any scripts that are part of the dotfiles.
chezmoi-apply-all:
    chezmoi --verbose apply    

# Apply the changes only for specified types like file changes, symlinks, and templates. So basically no scripts are run.
chezmoi-apply-files:
    chezmoi --verbose -i files,symlinks,templates apply 

# Pull changes from a remote repository and apply them
chezmoi-update:
    chezmoi update

# Resets the state of the script execution state (states like before/after script execution, etc.)
reset-chezmoi-script-state:
    chezmoi state delete-bucket --bucket=scriptState
