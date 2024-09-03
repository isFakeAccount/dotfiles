# github.com/isFakeAccount/dotfiles

Yoshikage Kira 's dotfiles, managed with [`chezmoi`](https://github.com/twpayne/chezmoi).

Install them with:

    chezmoi init isFakeAccount

For PC with NVIDIA GPU, run the following command
```bash
ansible-playbook "$chezmoi_dir/home/ansible_playbooks/nvidia_setup.yaml"
```