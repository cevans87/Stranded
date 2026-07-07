import dataclasses
import logging

import pytest

from stranded.logging.asyncio import Logger


@pytest.mark.asyncio
async def test_zero_args(log_capture_fixture: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo(bar: int) -> int:
        return 42

    with log_capture_fixture.at_level(logging.DEBUG, logger=__name__):
        await foo(777)

    call_record, return_record = log_capture_fixture.records
    assert call_record.levelname == 'DEBUG'
    assert return_record.levelname == 'INFO'


@pytest.mark.asyncio
async def test_return_none_logs_at_none_level(log_capture_fixture: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo() -> int | None:
        return None

    with log_capture_fixture.at_level(logging.DEBUG, logger=__name__):
        await foo()

    call_record, return_record = log_capture_fixture.records
    assert call_record.levelname == 'DEBUG'
    assert return_record.levelname == 'WARNING'


@pytest.mark.asyncio
async def test_return_value_logs_at_return_level(log_capture_fixture: pytest.LogCaptureFixture) -> None:

    @Logger()
    async def foo() -> int | None:
        return 42

    with log_capture_fixture.at_level(logging.DEBUG, logger=__name__):
        await foo()

    call_record, return_record = log_capture_fixture.records
    assert call_record.levelname == 'DEBUG'
    assert return_record.levelname == 'INFO'


@pytest.mark.asyncio
async def test_self_referential_return_none_logs_at_none_level(log_capture_fixture: pytest.LogCaptureFixture) -> None:

    @dataclasses.dataclass
    class Foo:
        @Logger()
        async def foo(self) -> Foo | None:
            return None

    with log_capture_fixture.at_level(logging.DEBUG, logger=__name__):
        await Foo().foo()  # type: ignore[call-arg]

    call_record, return_record = log_capture_fixture.records
    assert call_record.levelname == 'DEBUG'
    assert return_record.levelname == 'WARNING'


@pytest.mark.asyncio
async def test_self_referential_return_none_logs_at_none_level_classmethod(
    log_capture_fixture: pytest.LogCaptureFixture,
) -> None:

    @dataclasses.dataclass
    class Foo:
        @classmethod
        @Logger()
        async def foo(cls) -> Foo | None:
            return None

    with log_capture_fixture.at_level(logging.DEBUG, logger=__name__):
        await Foo.foo()  # type: ignore[call-arg]

    call_record, return_record = log_capture_fixture.records
    assert call_record.levelname == 'DEBUG'
    assert return_record.levelname == 'WARNING'
