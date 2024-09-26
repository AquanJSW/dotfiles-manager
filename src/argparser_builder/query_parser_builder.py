import argparse

import tabulate
from sqlmodel import Session, select

from src.model import App, Dotfile, Host, Path


class QueryParserBuilder:
    def __init__(self, parser: argparse.ArgumentParser):
        parser.set_defaults(func=self._resolver, verbose=False)

    def _resolver(self, engine, _):
        with Session(engine) as session:
            hosts = session.exec(select(Host)).all()
            print('Host')
            print(
                tabulate.tabulate(
                    [(host.id, host.platform, host.description) for host in hosts],
                    headers=['ID', 'Platform', 'Description'],
                    tablefmt='grid',
                )
            )
            apps = session.exec(select(App)).all()
            print('App')
            print(
                tabulate.tabulate(
                    [(app.id, app.description) for app in apps],
                    headers=['ID', 'Description'],
                    tablefmt='grid',
                )
            )
            dotfiles = session.exec(select(Dotfile)).all()
            print('Dotfile')
            print(
                tabulate.tabulate(
                    [
                        (dotfile.app_id, dotfile.name, dotfile.description)
                        for dotfile in dotfiles
                    ],
                    headers=['App', 'Name', 'Description'],
                    tablefmt='grid',
                )
            )
            paths = session.exec(select(Path)).all()
            print('Path')
            print(
                tabulate.tabulate(
                    [
                        (
                            path.host_id,
                            path.app_id,
                            path.dotfile_name,
                            path.name,
                            path.path,
                            path.private,
                            path.datetime,
                            path.description,
                        )
                        for path in paths
                    ],
                    headers=[
                        'Host',
                        'App',
                        'Dotfile',
                        'Name',
                        'Path',
                        'Private',
                        'Datetime',
                        'Description',
                    ],
                    tablefmt='grid',
                )
            )
