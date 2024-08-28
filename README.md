# github.com/isFakeAccount/dotfiles

Yoshikage Kira 's dotfiles, managed with [`chezmoi`](https://github.com/twpayne/chezmoi).

Install them with:

    chezmoi init isFakeAccount

Add the following to .bashrc

```bash
source "$HOME/.config/bash/xdg_config.sh"

source "$XDG_CONFIG_HOME/bash/aliases.sh"
source "$XDG_CONFIG_HOME/bash/program_configs.sh"
source "$XDG_CONFIG_HOME/bash/functions.sh"
```

For PC with NVIDIA GPU, run the following command
```bash
ansible-playbook "$chezmoi_dir/home/ansible_playbooks/nvidia_setup.yaml"
```