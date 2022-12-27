"""Handles working with the foreign executable"""
import os
from shutil import which
from typing import IO


def get_editor_name() -> str:
    """Determine user's file editor based on $VISUAL or $EDITOR"""
    result: str = "vim"
    if "VISUAL" in os.environ:
        result = os.getenv("VISUAL")  # type: ignore[assignment]
    elif "EDITOR" in os.environ:
        result = os.getenv("EDITOR")  # type: ignore[assignment]
    return result


def get_fullpath(exe="") -> str:
    """Get the full path to the chosen editor"""
    prog = which(exe if exe != "" else get_editor_name())
    if prog is None:
        raise FileNotFoundError(f"Cannot determine a full path for {exe}")
    return prog


def replace_tmpfile_references(cmdline: list[str], file: IO[bytes]) -> list[str]:
    """Replace instances of '{piper:file}' in 'cmdline' with the path to 'file'"""
    return [file.name if arg == r"{piper:file}" else arg for arg in cmdline]
