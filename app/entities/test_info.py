from dataclasses import dataclass

from .file_path import FilePath
from .make_command import MakeCommand


@dataclass
class TestInfo:

    file_path: FilePath
    make_command: MakeCommand
