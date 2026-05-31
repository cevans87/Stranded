from __future__ import absolute_import

import pytest

from stranded import Composer


def test_base() -> None:
    @Composer()
    def foo() -> None:
        ...

    foo()


if __name__ == '__main__':
    pytest.main()
