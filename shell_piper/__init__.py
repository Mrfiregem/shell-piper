"""Write a temporary file and pass it to a program"""
import argparse
import logging
import subprocess
import sys

from .exe import get_fullpath
from .file import (
    close_file_and_exit,
    close_tmpfile,
    create_tmpfile,
    open_file_in_editor,
)

__version__ = "0.4.0"

LOG_NAME = "shell_piper" if __name__ == "__main__" else __name__
root_log = logging.Logger(LOG_NAME)


def main():
    """Entrance to cli script"""
    ap = argparse.ArgumentParser(  # pylint: disable=invalid-name
        prog="shell_piper",
        description=sys.modules[__name__].__doc__,
        epilog="Use '--' to prevent program flags to the right of it being parsed by piper.",
    )
    ap.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    ap.add_argument("-V", "--verbose", action="store_true", help="Show debug messages")
    ap.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["stdin", "s", "argument", "a", "expand", "x"],
        metavar="TYPE",
        default="stdin",
        help="How the file will be given to the program",
    )
    ap.add_argument("program", help="The program to pass your file to")
    ap.add_argument(
        "prog_args",
        metavar="args",
        nargs="*",
        default=[],
        help="Arguments to pass to the program",
    )

    cli_args = ap.parse_args()

    # Show more output if '-V' was passed
    if cli_args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Create a temporary file and open it in user's editor
    file_obj = create_tmpfile()
    open_file_in_editor(file_obj)

    executable = get_fullpath(cli_args.program)
    logging.debug(f"Found executable: {executable}")

    # Run the given program on the temporary file
    try:
        subprocess.run([executable, file_obj.name], check=True)
    except ChildProcessError as e:
        logging.error(
            f"Failed to run command: {cli_args.program} exited with exit code {e.returncode}"
        )
        close_file_and_exit(file_obj, 2)

    # Delete the temporary file
    close_tmpfile(file_obj)
