from __future__ import annotations

import ast
import builtins
import dataclasses
import enum
import types
import typing


@dataclasses.dataclass(frozen=True, kw_only=True)
class Convert[T]:
    """Converts a given str argument into given type T.

        >>> assert Convert(t=dict[int, str])('{42: "foo"}') == {42: "foo"}
        >>> assert Convert(t=typing.Literal['foo', 'bar', 'baz'])('"foo"') == "foo"
        >>> assert Convert(t=int | float | str)('3.14') == 3.14  # noqa
        >>> assert Convert(t=tuple[int, ...])('(1, 2, 3, 4)') == (1, 2, 3, 4)

    This performs verification that the arg matches the given type.

        >>> assert ast.literal_eval('3.14') == 3.14
        >>> Convert(t=int)('3.14') == 3.14
        Traceback (most recent call last):
          ...
        ValueError: Could not convert arg=3.14 to t=<class 'int'>.

    Custom types may also be used. The underlying type must be trivially-costructable with the output of
    ast.literal_eval of given positional constructor arg.

        >>> class MyEnum(enum.Enum):
        ...     foo = 1
        ...     bar = 2
        ...     baz = 3
        >>> assert Convert(t=MyEnum)('foo') == MyEnum.foo

        >>> @dataclasses.dataclass(frozen=True)
        ... class Foo[T]:
        ...     v: T
        >>> assert Convert(t=Foo)('foo') == Foo('foo')
        >>> assert Convert(t=Foo[str])('foo') == Foo('foo')

    Custom type aliases may be used similarly to custom types. The type alias arguments must correspond to the types of
    given positional constructor arguements.

        >>> @dataclasses.dataclass(frozen=True)
        ... class Bar[T, U, V]:
        ...     a: T
        ...     b: U
        ...     c: V
        >>> assert Convert(t=Bar[int, float, Foo])('42, 3.14, "foo"') == Bar(42, 3.14, Foo('foo'))
        >>> assert Convert(t=Bar[str, Foo[str], Foo[MyEnum]])('"foo", "foo", "foo"') == Bar("foo", Foo("foo"), Foo(MyEnum.foo))
    """
    t: type[T]

    type _Args = bool | float | int | str | list[typing.Any] | dict[typing.Any, typing.Any] | set[typing.Any] | None
    type _Args2[*Ts] = bool | float | int | str | list[*Ts] | dict[*Ts] | set[*Ts] | None

    def _using_type(self, arg: _Args, /) -> T:
        match self.t:
            case types.NoneType | None:
                assert arg is None, f'{self} expected `None`, got `{arg}`.'
                return arg
            case builtins.bool | builtins.int | builtins.float | builtins.str:
                assert isinstance(arg, self.t), f'{self} expected `{self.t}`, got `{arg}`'
                return arg
            case t if issubclass(t, enum.Enum):
                assert isinstance(arg, str) and hasattr(t, arg), (
                    f'{self} expected `{typing.Literal[*t._member_names_]}`, got `{type(arg)}`'  # noqa
                )
                return getattr(t, arg)
            case t:
                return t(arg)

    def _using_type_alias(self, args: _Args, /) -> T:
        match typing.get_origin(self.t), typing.get_args(self.t):
            case builtins.dict, (key_t, value_t):
                assert isinstance(args, dict), (
                    f'{self} expected `dict[{key_t}, {value_t}]`, got `{args}`'
                )
                return {
                    Convert(t=key_t)._from_arg(key): Convert(t=value_t)._from_arg(value)
                    for key, value in args.items()
                }

            case builtins.frozenset, (t,):
                assert isinstance(args, (set, frozenset)), (
                    f'{self} expected `{frozenset[t]}`, got `{args}`.'
                )
                return frozenset({Convert(t=t)._from_arg(arg) for arg in args})

            case builtins.list, (t,):
                assert isinstance(args, list), (
                    f'{self} expected `{list[t]}`, got `{args}`.'
                )
                return list(Convert(t=t)._from_arg(arg) for arg in args)

            case builtins.tuple, ():
                assert args == tuple(), (
                    f'{self} expected `{tuple[()]}`, got `{args}`.'
                )
                return args
            case builtins.tuple, (t,):
                assert isinstance(args, tuple) and len(args) == 1, (
                    f'{self} expected `{tuple[t]}`, got `{args}`.'
                )
                return tuple([Convert(t=t)._from_arg(args[0])])
            case builtins.tuple, (t, builtins.Ellipsis):
                assert isinstance(args, tuple), (
                    f'{self} expected `{tuple[t, ...]}`, got `{args}`.'
                )
                return tuple([Convert(t=t)._from_arg(value) for value in args])
            case builtins.tuple, (t, *ts):
                assert isinstance(args, tuple) and len(args) > 0, (
                    f'{self} expected `{tuple[t, *ts]}`, got `{args}`.'
                )
                return Convert(t=t)._from_arg(args[0]), *Convert(t=tuple[*ts])._from_arg(args[1:])

            case builtins.set, (t,):
                assert isinstance(args, (set, frozenset)), (
                    f'{self} expected `{set[t]}`, got `{args}`.'
                )
                return set({Convert(t=t)._from_arg(arg) for arg in args})

            case(typing.Union | types.UnionType), ts:
                assert type(args) in ts, (
                    f'{self} expected `{typing.Union[*ts]}`, got `{args}`.'
                )
                return args
            case typing.Literal, vs:
                assert args in vs, (
                    f'{self} expected `{typing.Literal[*vs]}`, got `{args}`.'  # noqa
                )
                return args

            case t, (t_,):
                return t(Convert(t=t_)._from_arg(args))
            case t, ts:
                return t(*(Convert(t=t)._from_arg(arg) for t, arg in zip(ts, args)))


    def _from_arg(self, arg: _Args, /) -> T:
        return self._using_type(arg) if typing.get_origin(self.t) is None else self._using_type_alias(arg)

    def __call__(self, arg: str, /) -> T:
        """Returns a T from given arg. Raises ValueError upon failure."""

        if self.t != str:
            try:
                arg: Convert._Args = ast.literal_eval(arg)
            except (SyntaxError, ValueError,):
                pass

        try:
            value = self._from_arg(arg)
        except AssertionError as e:
            raise ValueError(f'Could not convert {arg=} to t={self.t}.') from e

        return value
