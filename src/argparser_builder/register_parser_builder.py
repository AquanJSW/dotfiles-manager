import argparse
import os
import shutil

from sqlmodel import Session

from src.model import App, Dotfile, Host, Path

from . import helper


class RegisterParserBuilder:
    def __init__(self, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(
            title='entities',
            description='''Register procedure: host -> app -> dotfile -> path''',
        )
        self._add_host(
            subparsers.add_parser('host', help='Register a new host', aliases=['h'])
        )
        self._add_app(
            subparsers.add_parser('app', help='Register a new app', aliases=['a'])
        )
        self._add_dotfile(
            subparsers.add_parser(
                'dotfile', help='Register a new dotfile', aliases=['d']
            )
        )
        self._add_path(
            subparsers.add_parser('path', help='Register a new path', aliases=['p'])
        )

    def _add_host(self, parser: argparse.ArgumentParser):
        parser.add_argument('id', help='The host ID')
        parser.add_argument('--desc', help='A description of the host')
        helper.add_verbose_argument(parser)

        def resolve(engine, args: argparse.Namespace):
            host = Host(
                id=args.id, description=args.desc, platform=helper.get_platform()
            )
            with Session(engine) as session:
                session.add(host)
                session.commit()
            helper.save_host_id(args.id)

        parser.set_defaults(func=resolve)

    def _add_app(self, parser: argparse.ArgumentParser):
        parser.add_argument('id', help='The app ID')
        parser.add_argument('--desc', help='A description of the app')
        helper.add_verbose_argument(parser)

        def resolve(engine, args: argparse.Namespace):
            app = App(id=args.id, description=args.desc)
            with Session(engine) as session:
                session.add(app)
                session.commit()

        parser.set_defaults(func=resolve)

    def _add_dotfile(self, parser: argparse.ArgumentParser):
        parser.add_argument('app', help='The app ID')
        parser.add_argument('name', help='The dotfile name')
        parser.add_argument('--desc', help='A description of the dotfile')
        helper.add_verbose_argument(parser)

        def resolve(engine, args: argparse.Namespace):
            dotfile = Dotfile(app_id=args.app, name=args.name, description=args.desc)
            with Session(engine) as session:
                session.add(dotfile)
                session.commit()

        parser.set_defaults(func=resolve)

    def _add_path(self, parser: argparse.ArgumentParser):
        parser.add_argument('app', help='The app ID')
        parser.add_argument('dotfile', help='The dotfile name')
        parser.add_argument('name', help='The path ID for the row')
        parser.add_argument('path', help='The actual path')
        parser.add_argument(
            '-p',
            '--private',
            action='store_true',
            help='Make the path private, which will be ignored in sync',
        )
        parser.add_argument('-d', '--desc', help='A description of the path')
        helper.add_verbose_argument(parser)

        def resolve(engine, args: argparse.Namespace):
            """

            Try to insert in to db first and then try to copy the file.
            This may avoid duplicated insertions.
            """

            path = Path(
                host_id=helper.get_host_id(),
                app_id=args.app,
                dotfile_name=args.dotfile,
                name=args.name,
                path=args.path,
                private=args.private,
                description=args.desc,
                datetime=helper.get_datetime(args.path),
            )
            with Session(engine) as session:
                session.add(path)
                session.commit()

            # Copy the dotfile to database
            src = args.path
            dst = helper.get_dotfile_path_in_repo(
                helper.get_host_id(), args.app, args.dotfile, args.name
            )
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)

        parser.set_defaults(func=resolve)
