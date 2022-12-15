"""Writing and reading the file"""
import logging
import subprocess
import sys
from typing import BinaryIO

from .exe import get_editor


def open_file_in_editor(file: BinaryIO) -> tuple[str, bytes]:
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
        sys.exit(exit_code)
    return file.name, file.read()
