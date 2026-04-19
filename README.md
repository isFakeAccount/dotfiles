# github.com/isFakeAccount/dotfiles

Yoshikage Kira 's dotfiles, managed with [`chezmoi`](https://github.com/twpayne/chezmoi).

## Dependencies

- `chezmoi`
- `git`
- `justfile`
- `nvim`
- `python3-pip`
- `python3-venv`

## Installation

1. Install all dependencies.
2. Run the following command to set up chezmoi:

    ```sh
    chezmoi init isFakeAccount/dotfiles
    ```

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
chezmoi --verbose -i dirs,files,remove,symlinks,templates apply
```

### Pull changes from a remote repository and apply them

```sh
chezmoi update
```

### Clear the state of run_once_ scripts

```sh
chezmoi state delete-bucket --bucket=scriptState
```
