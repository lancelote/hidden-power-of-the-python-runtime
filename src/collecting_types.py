import inspect
from types import CodeType
from typing import List


def args_names(co: CodeType) -> List[str]:
    nargs = co.co_argcount
    names = co.co_varnames

    print(f"{nargs=}")
    print(f"{names=}")

    return list(names[:nargs])


def main(param: str):
    print(f"{param=}")

    frame = inspect.currentframe()
    code = frame.f_code
    names = args_names(code)
    local_vars = frame.f_locals
    objects = [local_vars[name] for name in names]

    print(f"{objects=}")


if __name__ == '__main__':
    main("foo")
