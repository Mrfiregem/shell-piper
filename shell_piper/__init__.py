"""Write a temporary file and pass it to a program"""
import argparse
import logging
import subprocess
import sys
from typing import IO

from .exe import get_fullpath, replace_tmpfile_references
from .file import (close_file_and_exit, close_tmpfile, create_tmpfile,
                   open_file_in_editor)

__version__ = "0.6.0"

EPILOG = """\
Use '--' to prevent command flags to the right of it being parsed by piper.

The '--type' flag can take values 'stdin' (default), 'argument', or 'expand',
or the letters 's', 'a', or 'x', respectively. This determines how the file is
passed to your program by shellpiper.
"""

LOG_NAME = "shell_piper" if __name__ == "__main__" else __name__
root_log = logging.Logger(LOG_NAME)


def stdin_mode(cmdline: list[str], file: IO[bytes]) -> int:
    """Run 'cmdline', passing 'file' as it's stdin"""
    try:
        logging.debug("Starting command %s", cmdline)
        proc = subprocess.run(cmdline, stdin=file, check=True)
    except subprocess.CalledProcessError as exc:
        logging.error(
            "Failed to run command: %s exited with exit code %d",
            cmdline,
            exc.returncode,
        )
        close_file_and_exit(file, 2)
    logging.debug("Finished running command %s", cmdline)
    return proc.returncode


def argument_mode(cmdline: list[str], file: IO[bytes]) -> int:
    """Run 'cmdline', passing path to 'file' as final argument"""
    if r"{piper:file}" in cmdline:
        cmdline = replace_tmpfile_references(cmdline, file)
    else:
        cmdline = cmdline + [file.name]

    try:
        logging.debug("Starting command %s", cmdline)
        proc = subprocess.run(cmdline, check=True)
    except subprocess.CalledProcessError as exc:
        logging.error(
            "Failed to run command: %s exited with exit code %d",
            cmdline,
            exc.returncode,
        )
        close_file_and_exit(file, 2)
    logging.debug("Finished running command %s", cmdline)
    return proc.returncode


def expand_mode(cmdline: list[str], file: IO[bytes], keep_empty: bool) -> int:
    """Run 'cmdline', passing each line of 'file' as an argument"""
    expansion = [line.decode(encoding="utf8").strip() for line in file.readlines()]
    if not keep_empty:
        expansion = list(filter(None, expansion))
    try:
        cmdline = cmdline + expansion
        logging.debug("Starting command %s", cmdline)
        proc = subprocess.run(cmdline, check=True)
    except subprocess.CalledProcessError as exc:
        logging.error(
            "Failed to run command: %s exited with exit code %d",
            cmdline,
            exc.returncode,
        )
        close_file_and_exit(file, 2)
    logging.debug("Finished running command %s", cmdline)
    return proc.returncode


def main():
    """Entrance to cli script"""
    ap = argparse.ArgumentParser(  # pylint: disable=invalid-name
        prog="shellpiper",
        description=sys.modules[__name__].__doc__,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
    ap.add_argument(
        "-k",
        "--keep-empty",
        action="store_true",
        help="Don't remove empty lines when using '--type expand'",
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

    cmdline = [cli_args.program] + cli_args.prog_args

    # Show more output if '-V' was passed
    if cli_args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Create a temporary file and open it in user's editor
    file_obj = create_tmpfile()
    open_file_in_editor(file_obj)

    try:
        logging.debug("Attempting to find executable: %s", cli_args.program)
        executable = get_fullpath(cli_args.program)
    except FileNotFoundError:
        logging.error("Cannot find full path for %s", cli_args.program)
        close_file_and_exit(file_obj, 4)

    logging.debug("Found executable: %s", executable)

    logging.debug("Beginning mode check")
    # Run the given program on the temporary file
    if cli_args.type in ["stdin", "s"]:
        logging.debug("Starting stdin_mode()")
        stdin_mode(cmdline, file_obj)
    elif cli_args.type in ["argument", "a"]:
        logging.debug("Starting argument_mode()")
        argument_mode(cmdline, file_obj)
    elif cli_args.type in ["expand", "x"]:
        logging.debug("Starting expand_mode()")
        expand_mode(cmdline, file_obj, cli_args.keep_empty)
    else:
        logging.error("Unknown '--type' value. Something went wrong.")
        close_file_and_exit(file_obj, 3)

    # Delete the temporary file
    close_tmpfile(file_obj)
