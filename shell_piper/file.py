"""Writing and reading the file"""
import logging
import subprocess
import sys
import tempfile
from typing import IO, Union

from .exe import get_editor


def create_tmpfile(suffix=".shell-piper.tmp") -> IO[bytes]:
    """Return a randomly generated file name"""
    return tempfile.NamedTemporaryFile("w+b", suffix=suffix)


def close_tmpfile(tmpfile: Union[IO[bytes], IO[str]]) -> None:
    """Close tmpfile (and delete it)"""
    try:
        tmpfile.close()
    except Exception as exc:
        raise RuntimeWarning from exc


def open_file_in_editor(file: IO[bytes]) -> None:
    """Write to temporary file with editor"""
    file.flush()
    try:
        editor_path = get_editor()
    except RuntimeError:
        logging.error("Cannot find path to editor")
        sys.exit(1)
    edit_cmd: list[str] = [editor_path, file.name]
    exit_code = subprocess.call(edit_cmd)
    if exit_code != 0:
        logging.error("Editor exited with non-zero exit code")
        close_tmpfile(file)
        sys.exit(exit_code)
