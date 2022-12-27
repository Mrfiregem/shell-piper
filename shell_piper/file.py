"""Writing and reading the file"""
import logging
import subprocess
import sys
import tempfile
from typing import IO, Union

from .exe import get_fullpath


def create_tmpfile(suffix=".shell-piper.tmp") -> IO[bytes]:
    """Return a randomly generated file name"""
    # pylint: disable=consider-using-with
    tmpfile = tempfile.NamedTemporaryFile("w+b", suffix=suffix)
    logging.debug("Created temporary file: %s", tmpfile.name)
    return tmpfile


def close_tmpfile(tmpfile: Union[IO[bytes], IO[str]]):
    """Close tmpfile (and delete it)"""
    logging.debug("Deleting temporary file: %s", tmpfile.name)
    try:
        tmpfile.close()
    except Exception as exc:
        raise OSError(f"Could not close {tmpfile.name}") from exc


def open_file_in_editor(file: IO[bytes]):
    """Write to temporary file with editor"""
    file.flush()
    try:
        editor_path = get_fullpath()
    except FileNotFoundError:
        logging.error("Cannot find path to editor")
        close_file_and_exit(file, 1)

    edit_cmd: list[str] = [editor_path, file.name]
    logging.debug("Opening %s with command %s", file.name, edit_cmd)

    exit_code = subprocess.call(edit_cmd)
    if exit_code != 0:
        logging.error("Editor exited with non-zero exit code")
        close_file_and_exit(file, exit_code)


def close_file_and_exit(file: IO[bytes], exit_code=0):
    """Wrapper to close a file or raise"""
    logging.debug("Running close_file_and_exit()")
    try:
        close_tmpfile(file)
    except OSError:
        logging.warning("Unable to close %s", file.name)
    sys.exit(exit_code)
