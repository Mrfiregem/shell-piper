# shell-piper

Shell-piper is a commandline program made to write to a temporary file with your editor and pass that file's contents to an external program through various methods.

## Installation

The recommended way to install shell-piper is through [pipx](https://github.com/pypa/pipx): `pipx install 'git+https://github.com/Mrfiregem/shell-piper.git'`

You can also clone this repository and build shell-piper manually.

## Quickstart

### Stdin Mode

Copy and paste text into your editor and modify it with `awk`:

```bash
shellpiper -- awk -F $'\t' '{ print $2 }'
```

### Argument Mode

Convert pasted html into markdown with `pandoc`:

```bash
shellpiper --type argument -- pandoc '{piper:file}' --from html -o converted.md
```

The argument `{piper:file}` will be expanded by shellpiper to the full path of the temporary file. If this argument is not present, the file path will be appended as the last argument.

### Expand Mode

Pass a list of urls to download with `youtube-dl`, with each line as an argument:

```bash
shellpiper -t x youtube-dl
```

## Usage

```
usage: shell_piper [-h] [-v] [-V] [-t TYPE] [-k] program [args ...]

Write a temporary file and pass it to a program

positional arguments:
  program               The program to pass your file to
  args                  Arguments to pass to the program

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -V, --verbose         Show debug messages
  -t TYPE, --type TYPE  How the file will be given to the program
  -k, --keep-empty      Don't remove empty lines when using '--type expand'

Use '--' to prevent command flags to the right of it being parsed by piper.

The '--type' flag can take values 'stdin' (default), 'argument', or 'expand',
or the letters 's', 'a', or 'x', respectively.
This determines how the file is passed to your program by shellpiper.

```