import ast
import inspect
from _ast import Assert, Name


def get_assert_at_line(node, line):
    for child in ast.walk(node):
        if isinstance(child, Assert) and child.lineno == line:
            return child


def get_vars_names(source, line):
    node = ast.parse(source)
    assert_node = get_assert_at_line(node, line)
    comparison = next(ast.iter_child_nodes(assert_node))

    for expr in ast.walk(comparison):
        if isinstance(expr, Name):  # variable nodes inside the comparison node
            yield expr.id


def vars_in_assert(exception):
    tb = exception.__traceback__
    frame = tb.tb_frame
    code = frame.f_code
    source = inspect.getsource(code)
    line = tb.tb_lineno - code.co_firstlineno + 1

    print(f"{tb.tb_lineno=}")         # line in traceback
    print(f"{code.co_firstlineno=}")  # line start of the frame
    print(f"{line=}")                 # relative assert position in the frame
    print("\nvars:")

    for name in get_vars_names(source, line):
        if name in frame.f_locals:
            var = frame.f_locals[name]
            print(f"  {name} = {var}")


def main():
    a = 1
    b = 2

    try:
        assert a + b < 1
    except AssertionError as error:
        vars_in_assert(error)


if __name__ == '__main__':
    main()
