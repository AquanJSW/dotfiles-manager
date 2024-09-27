import argparse

from .query_parser_builder import QueryParserBuilder
from .register_parser_builder import RegisterParserBuilder
from .sync_parser_builder import SyncParserBuilder


class RootParserBuilder:
    def __init__(self):
        # Top-level parser
        self.parser = argparse.ArgumentParser(
            description='Manage and sync dotfiles across multiple hosts'
        )
        subparsers = self.parser.add_subparsers(title='commands', description='')
        RegisterParserBuilder(
            parser=subparsers.add_parser(
                'register', help='Register a new entity', aliases=['r']
            ),
        )
        QueryParserBuilder(
            parser=subparsers.add_parser(
                'query',
                help='Query all the database',
                aliases=['q'],
                description='Query all the database',
            ),
        )
        SyncParserBuilder(
            parser=subparsers.add_parser(
                'sync',
                help='Sync dotfiles across hosts',
                aliases=['s'],
                description='''Sync dotfiles across hosts.

Depending on whether the `host` argument (the first element of `filter`) is
provided or not, the sync operation will be completely different:

- If `host` is not provided, it will update current host's dotfiles to repo.
  We call this operation *sync-self* for later reference.
- If `host` is provided, it will update current host's dotfiles with the 
  provided host's ones (*sync-host*). Note that *sync-self* will be performed
  first before this operation. Still note that after *sync-host*, the dotfiles
  in this repo may be **outdated** than your current dotfiles.
  But if the provided host is the same as the current host, *sync-self* will
  be skipped. This operation is called *restore-self*.
                ''',
                formatter_class=argparse.RawTextHelpFormatter,
            ),
        )

    def get(self):
        return self.parser
