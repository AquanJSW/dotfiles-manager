import os

import appdirs
from sqlmodel import SQLModel, create_engine

from src.argparser_builder import RootParserBuilder

DOTFILES_DIR = '.dotfiles'
DB_FILE = os.path.join(DOTFILES_DIR, 'sqlite.db')
APP_NAME = 'dotfile-manager'
APP_AUTHOR = 'aquanjsw'

# As module level variables
os.environ['APP_NAME'] = APP_NAME
os.environ['APP_AUTHOR'] = APP_AUTHOR
os.environ['USER_CONFIG_DIR'] = appdirs.user_config_dir(APP_NAME, APP_AUTHOR)
os.environ['DOTFILES_DIR'] = DOTFILES_DIR


def main():
    parser = RootParserBuilder().get()
    args = parser.parse_args()
    engine = create_engine(f"sqlite:///{DB_FILE}", echo=True if args.verbose else False)
    SQLModel.metadata.create_all(engine)
    args.func(engine, args)
