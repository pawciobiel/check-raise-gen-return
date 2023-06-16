from __future__ import annotations

import argparse
import ast
import logging
import sys
from collections.abc import Sequence
from typing import NamedTuple

log = logging.getLogger(__name__)


class Call(NamedTuple):
    name: str
    line: int
    column: int


class Visitor(ast.NodeVisitor):
    def __init__(
        self,
    ) -> None:
        self.gen_return_excs: list[Call] = []

    def visit_Raise(self, node: ast.Call) -> None:
        attrs = (
            [
                "id",
            ],
            ["func", "id"],
            [
                "attr",
            ],
            ["func", "attr"],
        )
        for attr_list in attrs:
            parent = node.exc
            for attr in attr_list:
                try:
                    # if node.exc.func.value.id == "gen" and
                    parent = getattr(parent, attr)
                except AttributeError:
                    break
            if parent == "Return":
                self.gen_return_excs.append(
                    Call("raise Return", node.lineno, node.col_offset),
                )


def check_file(
    filename: str,
) -> list[Call]:
    with open(filename, "rb") as f:
        tree = ast.parse(f.read(), filename=filename)
    visitor = Visitor()
    visitor.visit(tree)
    return visitor.gen_return_excs


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")

    args = parser.parse_args(argv)

    rc = 0
    for filename in args.filenames:
        calls = check_file(filename)
        if calls:
            rc = 1
        for call in calls:
            print(
                f"{filename}:{call.line}:{call.column}: "
                f"replace `{call.name}` with `return`",
            )
    return rc


if __name__ == "__main__":
    if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
        log.critical("This is not intended to be run on python <3.3!")
    raise SystemExit(main())
