# Copyright Amethyst Reese
# Licensed under the MIT license

import logging
import shlex
import subprocess
from functools import cache
from pathlib import Path

log = logging.getLogger(__name__)


@cache
def which() -> Path:
    """
    Find the appropriate ruff binary.
    """
    from ruff.__main__ import find_ruff_bin

    path = Path(find_ruff_bin())
    assert path.is_file()

    return path


def ruff(*args: str | Path, stdin: str | None) -> subprocess.CompletedProcess:
    """
    Run the ruff binary with the given args and optional stdin.
    """
    cmd = [str(a) for a in (which(), *args)]
    log.debug("running ruff: $ %s", shlex.join(cmd))
    proc = subprocess.run(cmd, input=stdin, check=True, text=True, capture_output=True)
    return proc


def rufffmt_text(path: Path, content: str) -> str:
    """
    Sort and format file contents in memory.
    """
    # sort imports
    proc = ruff(
        "check",
        "--fix",
        "--select",
        "I",
        "--stdin-filename",
        path,
        "-",
        stdin=content,
    )
    content = proc.stdout

    # format code
    proc = ruff(
        "format",
        "--stdin-filename",
        path,
        "-",
        stdin=content,
    )
    content = proc.stdout

    return content


def rufffmt_file(path: Path) -> None:
    """
    Sort and format file contents on disk.
    """
    content = path.read_text()
    content = rufffmt_text(path, content)
    path.write_text(content)
