import asyncio
import inspect
import logging
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
        values=(
            Cli.Signature.RequiredStackedArg(name='a', t=int),
            Cli.Signature.RequiredStackedArg(name='f', t=int),
            Cli.Signature.RequiredStackedArg(name='g', t=int),
            Cli.Signature.OptionalStackedArg(name='b', t=int, default=0),
            Cli.Signature.RequiredKeywordArg(name='d', t=int),
            Cli.Signature.RequiredKeywordArg(name='i', t=int),
            Cli.Signature.OptionalKeywordArg(name='c', t=int, default=1),
            Cli.Signature.OptionalKeywordArg(name='e', t=int, default=2),
            Cli.Signature.OptionalKeywordArg(name='h', t=int, default=3),
            Cli.Signature.OptionalKeywordArg(name='j', t=int, default=4),
            Cli.Signature.Return(t=dict[str, int]),
        ),
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
