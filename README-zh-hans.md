# dotfiles-manager

这个脚本可以用来管理多个设备间的配置文件 (dotfiles)。

本项目思想受 [agarrharr/settings](https://github.com/agarrharr/settings) 启发。

一共用到了4个表, 各个表及其需要用户输入的列信息如下：

> [!NOTE]
> 非可选列的顺序与命令行参数的输入顺序相同

- `host`: 存储设备信息

  | 列 | 外键 | 主键 | 可选 | 描述 |
  |-|-|-|-|-|
  |`id`||Y||为你的设备起一个名字|
  |`description`|||Y|设备描述信息|

- `app`: 存储应用信息

  | 列 | 外键 | 主键 | 可选 | 描述 |
  |-|-|-|-|-|
  |`id`||Y||为这个应用起一个名字|
  |`description`|||Y|这个应用的描述信息|
  
- `dotfile`: 存储配置信息, 但**该表并不存储实际路径**, 因为有些配置可能包含多个文件

  | 列 | 外键 | 主键 | 可选 | 描述 |
  |-|-|-|-|-|
  |`app_id`|Y|Y||所属应用的`id`|
  |`name`||Y||配置名称|
  |`description`|||Y|描述信息|

- `path`: 存储实际配置路径

  | 列 | 外键 | 主键 | 可选 | 描述 |
  |-|-|-|-|-|
  |`app_id`|Y|||所属应用的`id`|
  |`dotfile_name`|Y|||所属配置的`name`|
  |`name`||||给这个路径起一个简短的名字|
  |`path`||||实际路径|
  |`private`|||Y|是否私有，默认`False`|
  |`description`|||Y|描述信息|

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

## 安装

```bash
# 注意: 你应该克隆你的fork
# git clone --depth=1 https://github.com/AquanJSW/dotfiles-manager ~/.dotfiles
cd ~/.dotfiles
python3 -m venv .venv
pip install -r requirements.txt
. .venv/bin/activate
```

## 使用示例

### 首次使用的标准流程

1. 在第一台设备上（Linux）

  ```bash
  # 添加设备
  HOSTNAME=$(hostname)
  python3 ./manage.py register host "$HOSTNAME"
  # 添加应用
  python3 ./manage.py register app wezterm
  python3 ./manage.py register app nvim
  python3 ./manage.py register app bash
  # 添加配置
  python3 ./manage.py register dotfile wezterm main
  python3 ./manage.py register dotfile nvim init
  python3 ./manage.py register dotfile bash rc
  # 添加路径
  python3 ./manage.py register path wezterm main main ~/.wezterm.lua
  python3 ./manage.py register path nvim init main ~/.config/nvim/init.lua
  python3 ./manage.py register path bash rc main ~/.bashrc
  python3 ./manage.py register path bash rc aliases ~/.bash_aliases
  ```

  用`python3 ./manage.py query`检查无误后，推送到git remote

2. 在第二台设备上（Windows）

  ```pwsh
  # 添加设备
  $HOSTNAME=$env:COMPUTERNAME
  python3 ./manage.py register host "$HOSTNAME"
  # 添加路径
  python3 ./manage.py register path wezterm main main ~/.wezterm.lua
  python3 ./manage.py register path nvim init main $env:LOCALAPPDATA/nvim/init.lua
  # 与第一台设备同步
  python3 ./manage.py sync $FIRST_DEVICE
  ```

### 后续使用

同步本地更改到仓库：

```bash
python3 ./manage.py sync
```

> [!TIP]
> 与*修改*相关的命令，例如`update`和`delete`, 由于使用频率较低, 目前并没有实现.
> 你可以用其它工具来修改, 例如`sqlite3`, `python -m sqlite3`, *DB Browser for SQLite*等

> [!NOTE]
> 有些应用默认并没有配置文件，需要你手动创建，这种情况下你必须手动创建该配置文件才能添加路径

> [!NOTE]
> 默认情况下，`sync HOST`命令会用*diff tool*打开每个配置文件以实现交互式同步，目前支持**nvim**
> 和**VSCode**。你可以用`-f`参数取消交互式同步。

## 已知问题

- 有些外键约束无法正常工作。例如`Path`表的`dotfile_name`。`model.py`里的模型应该是没有问题的,
  因为*DB Browser for SQLite*可以检测出约束错误。
  当出现意外的约束错误，你可以用上面提到的工具进行修改。
