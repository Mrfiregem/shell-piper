"""Write a temporary file and pass it to a program"""
import argparse
import logging
import sys
from .exe import get_editor

__version__ = "0.4.0"


def main():
    """Entance to cli script"""
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
