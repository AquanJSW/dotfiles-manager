import datetime
import os
import sys


def add_verbose_argument(parser):
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Enable verbose output'
    )


def get_platform():
    return sys.platform


def get_datetime(file):
    return datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime(
        '%Y-%m-%d %H:%M:%S'
    )


def save_host_id(host_id):
    """

    Use compact config in the future if needed, like `config.yaml`
    """
    os.makedirs(os.environ['USER_CONFIG_DIR'], exist_ok=True)
    with open(os.path.join(os.environ['USER_CONFIG_DIR'], 'host_id'), 'w') as f:
        f.write(host_id)


def get_host_id():
    with open(os.path.join(os.environ['USER_CONFIG_DIR'], 'host_id'), 'r') as f:
        return f.read().strip()


def get_dotfile_path_in_repo(*components):
    """
    :param components: [HOST_ID, [APP_ID, [DOTFILE_NAME, [PATH_NAME]]]]
    """
    return os.path.join(os.environ['DOTFILES_DIR'], *components)
