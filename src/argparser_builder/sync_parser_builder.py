import argparse
import os
import shutil

from sqlmodel import Session, select

from src.model import Path

from . import helper


class SyncParserBuilder:
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            'filter', nargs='*', help='The source filter: [HOST [APP [DOTFILE [NAME]]]]'
        )
        parser.add_argument('-f', '--force', action='store_true', help='Skip diffing')
        parser.set_defaults(func=self._resolve, verbose=False)

    def _resolve(self, engine, args: argparse.Namespace):
        with Session(engine) as session:
            if not args.filter:
                sync_self(session)
                return
            sync_host(session, args.filter, args.force)


def sync_self(session: Session):
    print(f'Sync self: {helper.get_host_id()} -> repo/{helper.get_host_id()}')
    path_instances = session.exec(
        select(Path).where(Path.host_id == helper.get_host_id())
    ).all()
    for path_instance in path_instances:
        src_path = path_instance.path
        if helper.get_datetime(src_path) <= path_instance.datetime:
            continue
        dst_path = helper.get_dotfile_path_in_repo(
            helper.get_host_id(),
            path_instance.app_id,
            path_instance.dotfile_name,
            path_instance.name,
        )
        # Update file
        shutil.copyfile(src_path, dst_path)
        print(f'  {src_path} -> {dst_path}')
        # Update datetime
        path_instance.datetime = helper.get_datetime(src_path)
        session.add(path_instance)
        session.commit()
        session.refresh(path_instance)


def sync_host(session: Session, filter: list[str], force: bool):
    host_id = filter[0]
    if host_id != helper.get_host_id():
        sync_self(session)

    print(f'Sync host: repo/{host_id} -> {helper.get_host_id()}')

    match len(filter):
        case 1:
            wheres = [Path.host_id == host_id]
        case 2:
            wheres = [Path.host_id == host_id, Path.app_id == filter[1]]
        case 3:
            wheres = [
                Path.host_id == host_id,
                Path.app_id == filter[1],
                Path.dotfile_name == filter[2],
            ]
        case 4:
            wheres = [
                Path.host_id == host_id,
                Path.app_id == filter[1],
                Path.dotfile_name == filter[2],
                Path.name == filter[3],
            ]
    path_instances_host = session.exec(select(Path).where(*wheres)).all()

    def get_dst_path(app_id, dotfile_name, path_name):
        try:
            path_instance = session.exec(
                select(Path).where(
                    Path.host_id == helper.get_host_id(),
                    Path.app_id == app_id,
                    Path.dotfile_name == dotfile_name,
                    Path.name == path_name,
                )
            ).one()
            return path_instance.path
        except Exception as e:
            return ''

    for path_instance in path_instances_host:
        if path_instance.private:
            continue
        dst_path = get_dst_path(
            path_instance.app_id, path_instance.dotfile_name, path_instance.name
        )
        if not dst_path:
            continue
        src_path = helper.get_dotfile_path_in_repo(
            host_id,
            path_instance.app_id,
            path_instance.dotfile_name,
            path_instance.name,
        )
        # Update file
        shutil.copyfile(src_path, dst_path)
        if not force:
            diff_edit(
                helper.get_dotfile_path_in_repo(
                    helper.get_host_id(),
                    path_instance.app_id,
                    path_instance.dotfile_name,
                    path_instance.name,
                ),
                dst_path,
            )
        print(f'  {src_path} -> {dst_path}')


def diff_edit(file1, file2):
    if os.getenv('TERM_PROGRAM') == 'vscode':
        os.system(f'code -w --diff {file1} {file2}')
    else:
        # neovim
        os.system(f'vim -d {file1} {file2}')
