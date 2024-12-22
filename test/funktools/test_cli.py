import asyncio
import inspect
import logging
import sys
import textwrap

import pytest

from funktools import Cli


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

type Flag[T, D] = Cli.Flag[T, D]


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
    def baz(c: Flag[int, "A _c to set"]) -> dict[str, int]: return locals()

    assert (foo | bar | baz).leaves == (foo, bar, baz)


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

    assert (foo | bar).to_signature() == Cli.Signature(
        required_stacked_arg_by_name={
            'a': Cli.Signature.RequiredStackedArg(name='a', t=int),
            'f': Cli.Signature.RequiredStackedArg(name='f', t=int),
            'g': Cli.Signature.RequiredStackedArg(name='g', t=int),
        },
        optional_stacked_arg_by_name={
            'b': Cli.Signature.OptionalStackedArg(name='b', t=int, default=0),
        },
        required_keyword_arg_by_name={
            'd': Cli.Signature.RequiredKeywordArg(name='d', t=int),
            'i': Cli.Signature.RequiredKeywordArg(name='i', t=int),
        },
        optional_keyword_arg_by_name={
            'c': Cli.Signature.OptionalKeywordArg(name='c', t=int, default=1),
            'e': Cli.Signature.OptionalKeywordArg(name='e', t=int, default=2),
            'h': Cli.Signature.OptionalKeywordArg(name='h', t=int, default=3),
            'j': Cli.Signature.OptionalKeywordArg(name='j', t=int, default=4),
        },
        return_=dict[str, int],
    )


def test_merged_cli_requires_matching_annotations() -> None:
    @Cli()
    def foo(a: int):
        return locals()

    @Cli()
    def bar(a: float):
        return locals()

    @Cli()
    def baz(a: Cli.Flag[int, "An a to set"]):
        return locals()

    _ = (foo | foo).to_signature()
    _ = (bar | bar).to_signature()
    _ = (baz | baz).to_signature()

    with pytest.raises(AssertionError):
        _ = (foo | bar).to_signature()

    with pytest.raises(AssertionError):
        _ = (foo | baz).to_signature()

    with pytest.raises(AssertionError):
        _ = (bar | baz).to_signature()


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
        a: Cli.Flag[int, 'Sets a.'],
        b: Cli.Flag[int, 'Sets b.'] = 0,
        /,
        c: Cli.Flag[int, 'Sets c'] = 1,
        *,
        d: Cli.Flag[int, 'Sets d'],
        e: Cli.Flag[int, 'Sets e'] = 2,
    ) -> dict[str, int]: return locals()

    @Cli()
    def bar(
        f: Cli.Flag[int, 'Sets f'],
        /,
        g: Cli.Flag[int, 'Sets g'],
        h: Cli.Flag[int, 'sets h'] = 3,
        *,
        i: Cli.Flag[int, 'Sets i'],
        j: Cli.Flag[int, 'Sets j'] = 4,
    ) -> dict[str, int]: return locals()

    assert textwrap.dedent((foo | bar).to_signature().to_long_str()).strip() == textwrap.dedent('''
        <a>             # int                   # Sets a.
        <f>             # int                   # Sets f.
        <g>             # int                   # Sets g.
        [<b(0)>]        # int                   # Sets b.
        --d <d>         # int                   # Sets d.
        --i <i>         # int                   # Sets i.
        [--c <c(1)>]    # int                   # Sets c.
        [--e <e(2)>]    # int                   # Sets e.
        [--h <h(3)>]    # int                   # Sets h.
        [--j <j(4)>]    # int                   # Sets j.
    ''').strip()
