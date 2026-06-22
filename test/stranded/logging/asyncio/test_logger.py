import logging
import sys
import typing

import pytest

from stranded.logging.asyncio import Logger


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def _return_level(caplog: pytest.LogCaptureFixture) -> str:
    (record,) = (record for record in caplog.records if '->' in record.getMessage())
    return record.levelname


@pytest.mark.asyncio
async def test_zero_args() -> None:

    @Logger()
    async def foo(bar: int) -> int:
        return 42

    await foo(777)


@pytest.mark.asyncio
async def test_optional_return_none_logs_at_none_level(caplog: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo() -> int | None:
        return None

    with caplog.at_level(logging.DEBUG):
        await foo()

    assert _return_level(caplog) == 'WARNING'


@pytest.mark.asyncio
async def test_optional_return_value_logs_at_ok_level(caplog: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo() -> int | None:
        return 42

    with caplog.at_level(logging.DEBUG):
        await foo()

    assert _return_level(caplog) == 'INFO'


@pytest.mark.asyncio
async def test_non_optional_return_none_logs_at_ok_level(caplog: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo() -> None:
        return None

    with caplog.at_level(logging.DEBUG):
        await foo()

    assert _return_level(caplog) == 'INFO'


@pytest.mark.asyncio
async def test_literal_none_return_none_logs_at_ok_level(caplog: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo() -> typing.Literal['a', None]:
        return None

    with caplog.at_level(logging.DEBUG):
        await foo()

    assert _return_level(caplog) == 'INFO'
