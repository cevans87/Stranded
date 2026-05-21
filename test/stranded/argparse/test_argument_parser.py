import builtins
import inspect
import logging
import shlex
import sys
import textwrap
import typing

import pytest

from stranded.argparse import ArgumentParser

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def test_union_preserves_order() -> None:

    @ArgumentParser()
    def foo(a: int) -> dict[str, int]: return locals()

    @ArgumentParser()
    def bar(b: int) -> dict[str, int]: return locals()

    @ArgumentParser()
    def baz(c: typing.Annotated[int, "A c to set"]) -> dict[str, int]: return locals()

    assert (foo | bar | baz).decorateds == (foo, bar, baz)


def test_creates_signature() -> None:

    @ArgumentParser()
    def foo(a: int) -> dict[str, int]:
        return locals()

    @ArgumentParser()
    def bar(b: int) -> dict[str, int]:
        return locals()

    baz = foo | bar

    for argument_parser in (foo, bar, baz):
        assert inspect.signature(argument_parser).parameters == {
            'argv': inspect.Parameter('argv', inspect.Parameter.VAR_POSITIONAL),
        }


def test_merged_merges_signatures() -> None:

    @ArgumentParser()
    def foo(
        a: int,
        b: int = 0,
        /,
        c: int = 1,
        *args: int,
        d: int,
        e: int = 2,
        **kwargs: int,
    ) -> dict[str, int]: return locals()

    @ArgumentParser()
    def bar(
        f: int,
        /,
        g: int,
        h: int = 3,
        *args: int,
        i: int,
        j: int = 4,
        **kwargs: int,
    ) -> dict[str, int]: return locals()

    assert (foo | bar).to_signature() == ArgumentParser.Signature(
        required_positional_parameter_by_name={
            'a': ArgumentParser.Signature.RequiredPositionalParameter(name='a', t=int),
            'f': ArgumentParser.Signature.RequiredPositionalParameter(name='f', t=int),
            'g': ArgumentParser.Signature.RequiredPositionalParameter(name='g', t=int),
        },
        optional_positional_parameter_by_name={
            'b': ArgumentParser.Signature.OptionalPositionalParameter(name='b', t=int, default=0),
        },
        required_keyword_parameter_by_name={
            'd': ArgumentParser.Signature.RequiredKeywordParameter(name='d', t=int),
            'i': ArgumentParser.Signature.RequiredKeywordParameter(name='i', t=int),
        },
        optional_keyword_parameter_by_name={
            'c': ArgumentParser.Signature.OptionalKeywordParameter(name='c', t=int, default=1),
            'e': ArgumentParser.Signature.OptionalKeywordParameter(name='e', t=int, default=2),
            'h': ArgumentParser.Signature.OptionalKeywordParameter(name='h', t=int, default=3),
            'j': ArgumentParser.Signature.OptionalKeywordParameter(name='j', t=int, default=4),

        },
        variadic_positional_parameter=ArgumentParser.Signature.VariadicPositionalParameter(name='args', t=int),
        variadic_keyword_parameter=ArgumentParser.Signature.VariadicKeywordParameter(name='kwargs', t=int),
        return_annotation=ArgumentParser.Signature.ReturnAnnotation(t=dict[str, int]),
    )


def test_merged_requires_matching_annotations() -> None:
    @ArgumentParser()
    def foo(a: int):
        return locals()

    @ArgumentParser()
    def bar(a: float):
        return locals()

    @ArgumentParser()
    def baz(a: typing.Annotated[int, "An a to set"]):
        return locals()

    @ArgumentParser()
    def qux(*, a: int):
        return locals()

    _ = (foo | foo).to_signature()
    _ = (bar | bar).to_signature()
    _ = (baz | baz).to_signature()
    _ = (qux | qux).to_signature()

    with pytest.raises(AssertionError):
        _ = (foo | bar).to_signature()

    with pytest.raises(AssertionError):
        _ = (foo | baz).to_signature()

    with pytest.raises(AssertionError):
        _ = (foo | qux).to_signature()

    with pytest.raises(AssertionError):
        _ = (bar | baz).to_signature()

    with pytest.raises(AssertionError):
        _ = (bar | qux).to_signature()

    with pytest.raises(AssertionError):
        _ = (baz | qux).to_signature()


def test_signature_to_short_str() -> None:

    @ArgumentParser()
    def foo(
        a: int,
        b: int = 0,
        /,
        c: int = 1,
        *,
        d: int,
        e: int = 2,
    ) -> dict[str, int]: return locals()

    @ArgumentParser()
    def bar(
        f: int,
        /,
        g: int,
        h: int = 3,
        *,
        i: int,
        j: int = 4,
    ) -> dict[str, int]: return locals()

    assert (foo | bar).to_signature().to_short_str() == (
        '<a> <f> <g> [<b(0)>] --d <d> --i <i> [--c <c(1)>] [--e <e(2)>] [--h <h(3)>] [--j <j(4)>]'
    )


def test_signature_to_long_str() -> None:

    @ArgumentParser()
    def foo(
        a: typing.Annotated[int, 'Sets a.'],
        b: typing.Annotated[int, 'Sets b.'] = 0,
        /,
        c: typing.Annotated[int, 'Sets c.'] = 1,
        *,
        d: typing.Annotated[int, 'Sets d.'],
        e: typing.Annotated[int, 'Sets e.'] = 2,
    ) -> typing.Annotated[dict[str, int], 'Returns foo.']: return locals()

    @ArgumentParser()
    def bar(
        f: typing.Annotated[int, 'Sets f.'],
        /,
        g: typing.Annotated[int, 'Sets g.'],
        h: typing.Annotated[int, 'Sets h.'] = 3,
        *,
        i: typing.Annotated[int, 'Sets i.'],
        j: typing.Annotated[int, 'Sets j.'] = 4,
    ) -> typing.Annotated[dict[str, int], 'Returns bar.']: return locals()

    assert textwrap.dedent((foo | bar).to_signature().to_long_str()).strip() == textwrap.dedent('''
        <a>                             # <class 'int'>  # Sets a.
        <f>                             # <class 'int'>  # Sets f.
        <g>                             # <class 'int'>  # Sets g.
        [<b(0)>]                        # <class 'int'>  # Sets b.
        --d <d>                         # <class 'int'>  # Sets d.
        --i <i>                         # <class 'int'>  # Sets i.
        [--c <c(1)>]                    # <class 'int'>  # Sets c.
        [--e <e(2)>]                    # <class 'int'>  # Sets e.
        [--h <h(3)>]                    # <class 'int'>  # Sets h.
        [--j <j(4)>]                    # <class 'int'>  # Sets j.
                                        # dict[str, int]  # Returns bar.
    ''').strip()


def test_call_parses_int() -> None:

    @ArgumentParser()
    def foo(a: int) -> dict[str, int]: return locals()

    assert foo(*'1'.split()) == {'a': 1}


def test_call_calls_merged_argument_parsers() -> None:

    @ArgumentParser()
    def foo(a: int) -> dict[str, int]: return locals()

    @ArgumentParser()
    def bar(b: int) -> dict[str, int]: return locals()

    assert (foo | bar)(*'1 2'.split()) == {'b': 2}


def test_call_parses_args() -> None:

    calls = []

    @ArgumentParser()
    def foo(a: int) -> None: calls.append({'a': a})

    @ArgumentParser()
    def bar(*args: str) -> None: calls.append({'args': args})

    (foo | bar)(*'1 2 --b 3.0 --c 4.0'.split())

    assert calls == [
        {'a': 1},
        {'args': ('2', '--b', '3.0', '--c', '4.0')},
    ]


def test_call_parses_kwargs() -> None:

    calls = []

    @ArgumentParser()
    def foo(a: int) -> None: calls.append({'a': a})

    @ArgumentParser()
    def bar(**kwargs: int) -> None: calls.append({'kwargs': kwargs})

    (foo | bar)(*'1 --b 2 --c 3'.split())

    assert calls == [
        {'a': 1},
        {'kwargs': {'b': 2, 'c': 3}},
    ]


def test_call_parses_args_and_kwargs() -> None:

    calls = []

    @ArgumentParser()
    def foo(a: int) -> None: calls.append({'a': a})

    @ArgumentParser()
    def bar(*args: str) -> None: calls.append({'args': args})

    @ArgumentParser()
    def baz(**kwargs: float) -> None: calls.append({'kwargs': kwargs})

    (foo | bar | baz)(*'1 2 --b 3.0 --c 4.0'.split())

    assert calls == [
        {'a': 1},
        {'args': ('2',)},
        {'kwargs': {'b': 3.0, 'c': 4.0}},
    ]


def test_args_passed_to_subcommand() -> None:

    calls = []

    @ArgumentParser()
    def foo(subcommand: typing.Literal['bar', 'baz'], *args: str) -> None:
        calls.append({'subcommand': subcommand})
        match subcommand:
            case 'bar':
                bar(*args)
            case 'baz':
                baz(*args)

    @ArgumentParser()
    def bar(*args: str) -> None: calls.append({'args': args})

    @ArgumentParser()
    def baz(**kwargs: float) -> None: calls.append({'kwargs': kwargs})

    foo(*'bar --a 3.0 --b 4.0'.split())

    assert calls == [
        {'subcommand': 'bar'},
        {'args': ('--a', '3.0', '--b', '4.0')},
    ]

    calls = []

    foo(*'baz --a 3.0 --b 4.0'.split())

    assert calls == [
        {'subcommand': 'baz'},
        {'kwargs': {'a': 3.0, 'b': 4.0}},
    ]


def test_help_goes_to_subcommand() -> None:

    calls = []

    @ArgumentParser()
    def help_flag(subcommand: typing.Literal['bar', 'baz'] = ..., /, *, help: bool = False) -> None:  # noqa
        calls.append({'subcommand': subcommand, 'help': help})
        if help:
            match subcommand:
                case builtins.Ellipsis:
                    subcommand = foo
                case 'bar':
                    subcommand = bar
                case 'baz':
                    subcommand = baz
                case _:
                    assert False, f'Invalid {subcommand=}'
            print((help_flag | subcommand).to_long_str())
            assert False, 'In a normal Cli, this should be `sys.exit(0)`.'

    @ArgumentParser()
    def foo(subcommand: typing.Literal['bar', 'baz'] = ..., /, *args: str) -> None:
        calls.append({'subcommand': subcommand})
        match subcommand:
            case  builtins.Ellipsis:
                print((help_flag | foo).to_short_str())
            case 'bar':
                (help_flag | bar)(*args)
            case 'baz':
                (help_flag | baz)(*args)

    @ArgumentParser()
    def bar(*args: str) -> None: calls.append({'args': args})

    @ArgumentParser()
    def baz(**kwargs: float) -> None: calls.append({'kwargs': kwargs})

    with pytest.raises(AssertionError):
        (help_flag | foo)(*'-help'.split())

    assert calls == [
        {'subcommand': ..., 'help': True},
    ]

    calls = []

    with pytest.raises(AssertionError):
        (help_flag | foo)(*'bar -help'.split())

    assert calls == [
        {'subcommand': 'bar', 'help': True},
    ]

    calls = []

    with pytest.raises(AssertionError):
        (help_flag | foo)(*'baz -help'.split())

    assert calls == [
        {'subcommand': 'baz', 'help': True},
    ]


@pytest.mark.asyncio
async def test_asyncio_runs_threading() -> None:

    calls = []

    @ArgumentParser()
    def foo(a: int) -> None: calls.append({'a': a})

    @ArgumentParser()
    async def bar(b: int) -> None: calls.append({'b': b})

    await (foo | bar)(*'1 2'.split())

    assert calls == [
        {'a': 1},
        {'b': 2},
    ]


def test_threading_runs_asyncio() -> None:

    calls = []

    @ArgumentParser()
    async def foo(a: int) -> None: calls.append({'a': a})

    @ArgumentParser()
    def bar(b: int) -> None: calls.append({'b': b})

    (foo | bar)(*'1 2'.split())

    assert calls == [
        {'a': 1},
        {'b': 2},
    ]


def test_dict_is_parsed() -> None:
    calls = []

    @ArgumentParser()
    def foo(a: dict[int, str]) -> None: calls.append({'a': a})

    foo(*shlex.split(r'''"{1: 'foo'}"'''))

    assert calls == [{'a': {1: 'foo'}}]


if __name__ == '__main__':
    pytest.main()
