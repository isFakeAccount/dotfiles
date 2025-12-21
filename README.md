# github.com/isFakeAccount/dotfiles

Yoshikage Kira 's dotfiles, managed with [`chezmoi`](https://github.com/twpayne/chezmoi).

## Installation

1. Clone this repo to ~/.local/share/chezmoi.

    ```sh
    git clone https://github.com/isFakeAccount/dotfiles.git ~/.local/share/chezmoi
    ```

2. Install `python3-venv` and `python3-pip` if necessary.
3. `cd` into the repo, create a python venv and activate it.
4. Run the ./install.sh script.

## Chezmoi Quick Commands

### Set up chezmoi from existing dotfiles of a Git repository:

```sh
chezmoi init repository_url
```

### Start tracking one or more dotfiles

```sh
chezmoi add path/to/dotfile1 path/to/dotfile2 ...
```

### Update repository with local changes

```sh
chezmoi re-add path/to/dotfile1 path/to/dotfile2 ...
```

### Edit the source state of a tracked dotfile

```sh
chezmoi edit path/to/dotfile_or_symlink
```

### See pending changes

```sh
chezmoi diff
```

### Apply the changes

```sh
chezmoi --verbose apply
```

**Apply the changes only for specified types like file changes, symlinks, and templates. So basically no scripts are run.**

```sh
chezmoi --verbose -i files,symlinks,templates apply 
```

### Pull changes from a remote repository and apply them

```sh
chezmoi update
```

### Clear the state of run_once_ scripts

```sh
chezmoi state delete-bucket --bucket=scriptState
```
