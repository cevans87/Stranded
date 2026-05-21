import pytest

from stranded.functools import Retry


@pytest.mark.asyncio
async def test_one_retry() -> None:
    call_count = 0

    @Retry(n=1)
    async def foo():
        nonlocal call_count
        call_count += 1
        raise Exception()

    try:
        await foo()
    except Exception:  # noqa
        ...

    assert call_count == 2
