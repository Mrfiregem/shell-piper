"""Handles working with the foreign executable"""
import os
from shutil import which


def get_editor_name() -> str:
    """Determine user's file editor based on $VISUAL or $EDITOR"""
    result: str = "vim"
    if "VISUAL" in os.environ:
        result = os.getenv("VISUAL")  # type: ignore[assignment]
    elif "EDITOR" in os.environ:
        result = os.getenv("EDITOR")  # type: ignore[assignment]
    return result


def get_editor(exe="") -> str:
    """Get the full path to the chosen editor"""
    editor = which(exe if exe != "" else get_editor_name())
    if editor is not None:
        return editor
    raise RuntimeError
