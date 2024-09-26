# dotfiles-manager

[中文](README-zh-hans.md)

This is a simple dotfiles manager that I use to manage my dotfiles (configuration files) across multiple devices,
this idea is inspired by [agarrharr/settings](https://github.com/agarrharr/settings)

Four tables are used:

- `hosts`: Store device infos
- `apps`: Store application infos
- `dotfiles`: Store configuration infos, note that **this table doesn't store the actual paths**, as there may be multiple files for one configuration.
- `paths`: Store the actual paths of each configuration.

```plain
$ ./manage.py -h
usage: manage.py [-h] {register,r,query,q,sync,s} ...

Manage and sync dotfiles across multiple hosts

options:
  -h, --help            show this help message and exit

commands:

  {register,r,query,q,sync,s}
    register (r)        Register a new entity
    query (q)           Query all the database
    sync (s)            Sync dotfiles across hosts
```

## Usage

### Install

```bash
# WARNING: You should *fork* this repository first
# git clone --depth=1 https://github.com/AquanJSW/dotfiles-manager ~/.dotfiles
cd ~/.dotfiles
python3 -m venv .venv
pip install -r requirements.txt
. .venv/bin/activate
```

### Example

**For the very first use, a typical workflow would be:**

1. On the first device

  ```bash
  # Add host
  HOSTNAME=$(hostname)
  python3 ./manage.py register host "$HOSTNAME"
  # Add apps
  python3 ./manage.py register app wezterm
  python3 ./manage.py register app nvim
  python3 ./manage.py register app bash
  # Add dotfiles
  python3 ./manage.py register dotfile wezterm main
  python3 ./manage.py register dotfile nvim init
  python3 ./manage.py register dotfile bash rc
  # Add paths
  python3 ./manage.py register path wezterm main main ~/.wezterm.lua
  python3 ./manage.py register path nvim init main ~/.config/nvim/init.lua
  python3 ./manage.py register path bash rc main ~/.bashrc
  python3 ./manage.py register path bash rc aliases ~/.bash_aliases
  # You can check the database anytime
  python3 ./manage.py query
  # Push to your forked repository
  ```

1. Then on another device, register it too:

  ```pwsh
  # Clone your forked repository
  # Add host
  $HOSTNAME=$env:COMPUTERNAME
  python3 ./manage.py register host "$HOSTNAME"
  # Add paths
  python3 ./manage.py register path wezterm main main ~/.wezterm.lua
  python3 ./manage.py register path nvim init main $env:LOCALAPPDATA/nvim/init.lua
  # Sync with the first host
  python3 ./manage.py sync A
  ```

**For the following use, you may want to sync local to repo, simply run:**

```bash
python3 ./manage.py sync
```

> [!TIP]
> **The *update* functionalities like *update* and *delete***, due to their low
> frequency of use, **are not intended to be implemented**.
> If you want to update or delete an entity, you can do it manually by using
> other utils like `sqlite3`, `python -m sqlite3`, *DB Browser for SQLite*, etc.

> [!NOTE]
> You need to manually create an empty dotfile if you don't have the
> configuration file yet to register the path.

> [!NOTE]
> By default, the **`sync HOST`** command will **need diff tool to sync with
> confirmations**, **currently supported diff tools are `nvim` and `VSCode`**.
> You can also using `-f` to force sync without confirmations.

## Known Issues

- There may be some foreign key constraints are not working. For my use case,
  I've found that the `dotfile_name` constraint in `Path` table is not working.
  The models in `model.py` are possibly not the reason, because the
  *DB Browser for SQLite* can find the foreign key constraints and reports the
  errors.
  You may want to use other utils to modify the database if you encounter this.
