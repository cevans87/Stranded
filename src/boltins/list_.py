import builtins
import typing
from inspect import isasyncgenfunction, iscoroutinefunction


class List[T](builtins.list[T]):

    @typing.overload
    async def map[U](self, f: typing.Callable[[T], typing.Awaitable[T]]) -> typing.AsyncIterable[U]:
        ...

    @typing.overload
    def map[U](self, f: typing.Callable[[T], U]) -> typing.Iterable[U]:
        ...

    def map(self, f):
        if not iscoroutinefunction(f):
            return (f(v) for v in self)

        async def inner():
            return (await f(v) for v in self)

        return inner()

    def fold[U](self, f: typing.Callable[[T, U], U], initial: U) -> U:
        return ()
