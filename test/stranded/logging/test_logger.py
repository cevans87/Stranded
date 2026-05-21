import logging
import sys

import pytest

from stranded.logging import Logger


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


@pytest.mark.asyncio
async def test_zero_args() -> None:

    @Logger(logger=logger)
    async def foo(bar: int) -> int:
        return 42

    await foo(777)
