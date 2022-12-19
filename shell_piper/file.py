"""Writing and reading the file"""
import logging
import subprocess
import sys
import tempfile
from typing import IO, Union

from .exe import get_fullpath


def create_tmpfile(suffix=".shell-piper.tmp") -> IO[bytes]:
    """Return a randomly generated file name"""
    tmpfile = tempfile.NamedTemporaryFile("w+b", suffix=suffix)
    logging.debug(f"Created temporary file: {tmpfile.name}")
    return tmpfile


def close_tmpfile(tmpfile: Union[IO[bytes], IO[str]]) -> None:
    """Close tmpfile (and delete it)"""
    logging.debug(f"Deleting temporary file: {tmpfile.name}")
    try:
        tmpfile.close()
    except:
        raise RuntimeWarning(f"Could not close {tmpfile.name}")


def open_file_in_editor(file: IO[bytes]) -> None:
    """Write to temporary file with editor"""
    file.flush()
    try:
        editor_path = get_fullpath()
    except RuntimeError:
        logging.error("Cannot find path to editor")
        sys.exit(1)

    edit_cmd: list[str] = [editor_path, file.name]
    logging.debug(f"Opening {file.name} with command {edit_cmd}")

    exit_code = subprocess.call(edit_cmd)
    if exit_code != 0:
        logging.error("Editor exited with non-zero exit code")
        close_file_and_exit(file, exit_code)


def close_file_and_exit(file: IO[bytes], exit_code=0) -> None:
    logging.debug("")
    try:
        close_tmpfile(file)
    except RuntimeWarning:
        logging.warning(f"Unable to close {file.name}")
    sys.exit(exit_code)
