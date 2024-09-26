#!/usr/bin/env python3
from sqlmodel import (
    CheckConstraint,
    Field,
    ForeignKeyConstraint,
    Relationship,
    SQLModel,
    UniqueConstraint,
)


class Host(SQLModel, table=True):
    id: str = Field(primary_key=True)
    platform: str = Field(
        sa_column_args=[CheckConstraint("platform IN ('win32', 'linux', 'darwin')")]
    )
    description: str | None = None

    paths: list["Path"] = Relationship(back_populates="host", cascade_delete=True)


class App(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str | None = None

    dotfiles: list["Dotfile"] = Relationship(back_populates="app", cascade_delete=True)


class Dotfile(SQLModel, table=True):
    app_id: str = Field(foreign_key="app.id", primary_key=True, ondelete="CASCADE")
    name: str = Field(primary_key=True)
    description: str | None = None

    app: App = Relationship(back_populates="dotfiles")
    paths: list["Path"] = Relationship(back_populates="dotfile", cascade_delete=True)


class Path(SQLModel, table=True):
    id: int = Field(primary_key=True)
    host_id: str = Field(foreign_key="host.id", ondelete="CASCADE")
    app_id: str
    dotfile_name: str
    name: str
    path: str
    private: bool = False
    datetime: str
    description: str | None = None

    __table_args__ = (
        ForeignKeyConstraint(
            ["app_id", "dotfile_name"],
            ["dotfile.app_id", "dotfile.name"],
            ondelete="CASCADE",
        ),
        UniqueConstraint('host_id', 'name', 'path', name='uq_host_id_name_path'),
    )

    dotfile: Dotfile = Relationship(back_populates="paths")
    host: Host = Relationship(back_populates="paths")


# For testing
if __name__ == '__main__':
    from sqlmodel import create_engine

    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
