import asyncio
import builtins
import inspect
import logging
import shlex
import sys
import textwrap
import typing

import pytest

from funktools import Cli

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


@pytest.fixture(autouse=True)
def event_loop() -> asyncio.AbstractEventLoop:
    """All async tests execute eagerly.

    Upon task creation return, we can be sure that the task has gotten to a point that it is either blocked or done.
    """

    eager_loop = asyncio.new_event_loop()
    eager_loop.set_task_factory(asyncio.eager_task_factory)
    yield eager_loop
    eager_loop.close()


def test_cli_union_preserves_order() -> None:

    @Cli()
    def foo(a: int) -> dict[str, int]: return locals()

    @Cli()
    def bar(b: int) -> dict[str, int]: return locals()

    @Cli()
    def baz(c: typing.Annotated[int, "A c to set"]) -> dict[str, int]: return locals()

    assert (foo | bar | baz).decorateds == (foo, bar, baz)


def test_cli_creates_cli_signature() -> None:

    @Cli()
    def foo(a: int) -> dict[str, int]:
        return locals()

    @Cli()
    def bar(b: int) -> dict[str, int]:
        return locals()

    baz = foo | bar

    for cli in (foo, bar, baz):
        assert inspect.signature(cli).parameters == {
            'argv': inspect.Parameter('argv', inspect.Parameter.VAR_POSITIONAL),
        }


def test_merged_cli_merges_signatures() -> None:

    @Cli()
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

    @Cli()
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

    assert (foo | bar).to_signature() == Cli.Signature(
        required_stacked_parameter_by_name={
            'a': Cli.Signature.RequiredStackedParameter(name='a', t=int),
            'f': Cli.Signature.RequiredStackedParameter(name='f', t=int),
            'g': Cli.Signature.RequiredStackedParameter(name='g', t=int),
        },
        optional_stacked_parameter_by_name={
            'b': Cli.Signature.OptionalStackedParameter(name='b', t=int, default=0),
        },
        required_keyword_parameter_by_name={
            'd': Cli.Signature.RequiredKeywordParameter(name='d', t=int),
            'i': Cli.Signature.RequiredKeywordParameter(name='i', t=int),
        },
        optional_keyword_parameter_by_name={
            'c': Cli.Signature.OptionalKeywordParameter(name='c', t=int, default=1),
            'e': Cli.Signature.OptionalKeywordParameter(name='e', t=int, default=2),
            'h': Cli.Signature.OptionalKeywordParameter(name='h', t=int, default=3),
            'j': Cli.Signature.OptionalKeywordParameter(name='j', t=int, default=4),

        },
        variadic_stacked_parameter=Cli.Signature.VariadicStackedParameter(name='args', t=int),
        variadic_keyword_parameter=Cli.Signature.VariadicKeywordParameter(name='kwargs', t=int),
        return_annotation=Cli.Signature.ReturnAnnotation(t=dict[str, int]),
    )


def test_merged_cli_requires_matching_annotations() -> None:
    @Cli()
    def foo(a: int):
        return locals()

    @Cli()
    def bar(a: float):
        return locals()

    @Cli()
    def baz(a: typing.Annotated[int, "An a to set"]):
        return locals()

    @Cli()
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

    @Cli()
    def foo(
        a: int,
        b: int = 0,
        /,
        c: int = 1,
        *,
        d: int,
        e: int = 2,
    ) -> dict[str, int]: return locals()

    @Cli()
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

    @Cli()
    def foo(
        a: typing.Annotated[int, 'Sets a.'],
        b: typing.Annotated[int, 'Sets b.'] = 0,
        /,
        c: typing.Annotated[int, 'Sets c.'] = 1,
        *,
        d: typing.Annotated[int, 'Sets d.'],
        e: typing.Annotated[int, 'Sets e.'] = 2,
    ) -> typing.Annotated[dict[str, int], 'Returns foo.']: return locals()

    @Cli()
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

    @Cli()
    def foo(a: int) -> dict[str, int]: return locals()

    assert foo(*'1'.split()) == {'a': 1}


def test_call_calls_merged_clis() -> None:

    @Cli()
    def foo(a: int) -> dict[str, int]: return locals()

    @Cli()
    def bar(b: int) -> dict[str, int]: return locals()

    assert (foo | bar)(*'1 2'.split()) == {'b': 2}


def test_call_parses_args() -> None:

    calls = []

    @Cli()
    def foo(a: int) -> None: calls.append({'a': a})

    @Cli()
    def bar(*args: str) -> None: calls.append({'args': args})

    (foo | bar)(*'1 2 --b 3.0 --c 4.0'.split())

    assert calls == [
        {'a': 1},
        {'args': ('2', '--b', '3.0', '--c', '4.0')},
    ]


def test_call_parses_kwargs() -> None:

    calls = []

    @Cli()
    def foo(a: int) -> None: calls.append({'a': a})

    @Cli()
    def bar(**kwargs: int) -> None: calls.append({'kwargs': kwargs})

    (foo | bar)(*'1 --b 2 --c 3'.split())

    assert calls == [
        {'a': 1},
        {'kwargs': {'b': 2, 'c': 3}},
    ]


def test_call_parses_args_and_kwargs() -> None:

    calls = []

    @Cli()
    def foo(a: int) -> None: calls.append({'a': a})

    @Cli()
    def bar(*args: str) -> None: calls.append({'args': args})

    @Cli()
    def baz(**kwargs: float) -> None: calls.append({'kwargs': kwargs})

    (foo | bar | baz)(*'1 2 --b 3.0 --c 4.0'.split())

    assert calls == [
        {'a': 1},
        {'args': ('2',)},
        {'kwargs': {'b': 3.0, 'c': 4.0}},
    ]


def test_args_passed_to_subcommand() -> None:

    calls = []

    @Cli()
    def foo(subcommand: typing.Literal['bar', 'baz'], *args: str) -> None:
        calls.append({'subcommand': subcommand})
        match subcommand:
            case 'bar':
                bar(*args)
            case 'baz':
                baz(*args)

    @Cli()
    def bar(*args: str) -> None: calls.append({'args': args})

    @Cli()
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

    @Cli()
    def help_flag(subcommand: typing.Literal['bar', 'baz'] = ..., /, *, help: bool = False) -> None:  # noqa
        calls.append({'subcommand': subcommand, 'help': help})
        if help:
            match subcommand:
                case builtins.Ellipsis:
                    cli = foo
                case 'bar':
                    cli = bar
                case 'baz':
                    cli = baz
                case _:
                    assert False, f'Invalid {subcommand=}'
            print((help_flag | cli).to_long_str())
            assert False, 'In a normal Cli, this should be `sys.exit(0)`.'

    @Cli()
    def foo(subcommand: typing.Literal['bar', 'baz'] = ..., /, *args: str) -> None:
        calls.append({'subcommand': subcommand})
        match subcommand:
            case  builtins.Ellipsis:
                print((help_flag | foo).to_short_str())
            case 'bar':
                (help_flag | bar)(*args)
            case 'baz':
                (help_flag | baz)(*args)

    @Cli()
    def bar(*args: str) -> None: calls.append({'args': args})

    @Cli()
    def baz(**kwargs: float) -> None: calls.append({'kwargs': kwargs})

    with pytest.raises(AssertionError):
        (help_flag | foo)(*'--help'.split())

    assert calls == [
        {'subcommand': ..., 'help': True},
    ]

    calls = []

    with pytest.raises(AssertionError):
        (help_flag | foo)(*'bar --help'.split())

    assert calls == [
        {'subcommand': 'bar', 'help': True},
    ]

    calls = []

    with pytest.raises(AssertionError):
        (help_flag | foo)(*'baz --help'.split())

    assert calls == [
        {'subcommand': 'baz', 'help': True},
    ]


@pytest.mark.asyncio
async def test_asyncio_runs_threading_cli() -> None:

    calls = []

    @Cli()
    def foo(a: int) -> None: calls.append({'a': a})

    @Cli()
    async def bar(b: int) -> None: calls.append({'b': b})

    await (foo | bar)(*'1 2'.split())

    assert calls == [
        {'a': 1},
        {'b': 2},
    ]


def test_threading_runs_asyncio_cli() -> None:

    calls = []

    @Cli()
    async def foo(a: int) -> None: calls.append({'a': a})

    @Cli()
    def bar(b: int) -> None: calls.append({'b': b})

    (foo | bar)(*'1 2'.split())

    assert calls == [
        {'a': 1},
        {'b': 2},
    ]


def test_dict_is_parsed() -> None:
    calls = []

    @Cli()
    def foo(a: dict[int, str]) -> None: calls.append({'a': a})

    foo(*shlex.split(r'''"{1: 'foo'}"'''))

    assert calls == [{'a': {1: 'foo'}}]