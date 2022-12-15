"""Writing and reading the file"""
import tempfile
from typing import IO


def write_file_contents() -> IO[bytes]:
    """Write to temporary file with editor"""
    with tempfile.NamedTemporaryFile("w+b", suffix=".shell-piper.tmp") as tmp:
        return tmp
