import ast

import pytest

from check_raise_gen_return import main, Visitor, Call

TEST_CODE = """
from tornado import gen

@gen.coroutine
def a():
    def b():
        raise gen.Return
    if b():
        raise gen.Return((yield something({"a": "&%^/"} for x in [1, 2, 3])))
    else:
        raise Exception("boom!")
    raise gen.Return(False)
"""


@pytest.fixture
def visitor():
    return Visitor()


@pytest.mark.parametrize(
    ("expr", "calls"),
    [
        ("raise", []),
        ("raise SystemExit()", []),
        ("raise Return", [Call("raise Return", 1, 0)]),
        ("raise gen.Return", [Call("raise Return", 1, 0)]),
        ("raise Return()", [Call("raise Return", 1, 0)]),
        ("raise gen.Return()", [Call("raise Return", 1, 0)]),
        ('raise gen.Return("kaboom!")', [Call("raise Return", 1, 0)]),
        ("raise gum.Return from exc", [Call("raise Return", 1, 0)]),
        ("raise gen.Return() from exc", [Call("raise Return", 1, 0)]),
    ],
)
def test_dict_allow_kwargs_exprs(visitor, expr, calls):
    visitor.visit(ast.parse(expr))
    assert visitor.gen_return_excs == calls


def test_failing_file(tmpdir):
    f = tmpdir.join("f.py")
    f.write(TEST_CODE)
    rc = main([str(f)])
    assert rc == 1
