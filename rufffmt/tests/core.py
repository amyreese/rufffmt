from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from unittest import TestCase

from ..core import rufffmt_file, rufffmt_text

FILE = Path("hello.py")


def t(value: str) -> str:
    return dedent(value).lstrip()


class CoreTest(TestCase):
    def test_rufffmt_text(self) -> None:
        original = t(
            """
            import sys
            import re
            print(
                "hello"   )
            """
        )
        expected = t(
            """
            import re
            import sys

            print("hello")
            """
        )

        self.assertEqual(expected, rufffmt_text(FILE, original))

    def test_rufffmt_file(self) -> None:
        original = t(
            """
            import sys
            import re
            print(
                "hello"   )
            """
        )
        expected = t(
            """
            import re
            import sys

            print("hello")
            """
        )

        with TemporaryDirectory() as td:
            tdp = Path(td).resolve()
            path = tdp / "hello.py"
            path.write_text(original)

            rufffmt_file(path)
            self.assertEqual(expected, path.read_text())
