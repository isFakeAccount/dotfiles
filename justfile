# Justfile for easily running commands related to my dotfiles managed with chezmoi.

just-fmt:
    just --fmt --unstable

# Runs the formatter for python scripts in the .chezmoiscripts directory.
fmt:
    ruff format home/.chezmoiscripts/
    docstrfmt home/.chezmoiscripts/*.py -v

checker:
    mypy home/.chezmoiscripts/

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
    chezmoi --verbose -i dirs,files,remove,symlinks,templates apply

chezmoi-apply-scripts:
    chezmoi --verbose -i always,scripts,templates apply

# Pull changes from a remote repository and apply them
chezmoi-update:
    chezmoi update

# Resets the state of the script execution state (states like before/after script execution, etc.)
reset-chezmoi-script-state:
    chezmoi state delete-bucket --bucket=scriptState

# Run the generate playbook python script
run-gen-pb:
    .venv/bin/python home/.chezmoiscripts/run_after_01_gen_ansible_playbooks.py

# Run the python script to play the generated playbooks
run-play-pb:
    .venv/bin/python home/.chezmoiscripts/run_after_02_play_ansible_playbooks.py
