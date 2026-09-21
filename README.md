# Stranded

Composable decorators for caching, retrying, throttling, logging, and building
command-line interfaces. Every decorator works on both plain and `async def`
functions, picking the threading or asyncio implementation from the function it
wraps.

Stranded is alpha software. The API changes between releases.

## Install

```bash
pip install stranded
```

Python 3.13 or newer is required. There are no runtime dependencies.

## Usage

Each decorator is a frozen dataclass. Configure it with keyword arguments and
apply it to a function. The same decorator works for sync and async code.

```python
import asyncio

from stranded.functools import LruCache, Retry, Throttle


@LruCache(size=128)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)


@Retry(n=3)
@Throttle(max_running=4)
async def fetch(url: str) -> str:
    await asyncio.sleep(0)
    return url


print(fib(40))
print(asyncio.run(fetch('https://example.com')))
```

### functools

- `LruCache(size=...)` memoizes by argument, sharing one in-flight result
  between concurrent callers.
- `Herd()` collapses concurrent calls with the same arguments into one call,
  without memoizing the result.
- `Retry(n=...)` re-invokes the function when it raises, up to `n` times.
- `Throttle(max_running=..., max_waiting=...)` bounds concurrency. The running
  cap grows additively while calls succeed and halves when a call raises.

Each also has an instance with default settings, spelled in lowercase:
`lru_cache`, `herd`, `retry`, `throttle`.

### logging

`Logger` logs a function's call, return value, and exceptions at configurable
levels.

```python
import logging

from stranded.logging import Logger

logging.basicConfig(level=logging.DEBUG)


@Logger(call_level='DEBUG', return_level='INFO', exception_level='ERROR')
def add(a: int, b: int) -> int:
    return a + b


add(1, 2)
```

### sqlite3

`Db` memoizes a function's results to a SQLite database on disk, so results
survive across processes.

```python
import pathlib
import tempfile

from stranded.sqlite3 import Db

with tempfile.TemporaryDirectory() as tmp:

    @Db(path=pathlib.Path(tmp) / 'db')
    def expensive(key: str) -> str:
        print('computing', key)
        return key.upper()

    print(expensive('a'))
    print(expensive('a'))
```

### argparse

`ArgumentParser` builds a command-line parser from a function's signature and
type hints. Flags come before positionals, a boolean flag is spelled with one
dash, and a valued flag with two. Parsers compose with `|`, so flags shared
across subcommands can be written once.

```python
from stranded.argparse import ArgumentParser


@ArgumentParser()
def verbose_flag(*, verbose: bool = False) -> None:
    if verbose:
        print('verbose on')


@ArgumentParser()
def main(name: str, /, *, count: int = 1) -> None:
    for _ in range(count):
        print(f'hello, {name}')


(verbose_flag | main)('-verbose', '--count', '2', 'world')
```

### Explicit sync and async variants

The top-level decorators dispatch on whether the wrapped function is a
coroutine function. To pin one, import from the `asyncio` or `threading`
subpackage instead, for example `stranded.functools.asyncio.LruCache`.

## Development

```bash
pip install -e '.[test]'
pytest
```

## License

MIT. See `LICENSE`.
