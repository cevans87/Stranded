from __future__ import annotations

import ast
import builtins
import dataclasses
import enum
import types
import typing


@dataclasses.dataclass(frozen=True, kw_only=True)
class Convert[T]:
    type_t: type[T]

    type _Arg = bool | float | int | str | list | dict | set | None

    def _from_type(self, arg: _Arg, /) -> T:
        match self.type_t:
            case types.NoneType | None:
                assert arg is None, f'{self} expected `None`, got `{arg}`.'
                return arg
            case builtins.bool | builtins.int | builtins.float | builtins.str:
                assert isinstance(arg, self.type_t), f'{self} expected `{self.type_t}`, got `{arg}`'
                return arg
            case T_ if issubclass(T_, enum.Enum):
                assert isinstance(arg, str) and hasattr(T_, arg)
                return getattr(T_, arg)
            case T_:
                return T_(arg)

    def _from_type_alias(self, arg: _Arg, /) -> T:
        match typing.get_origin(self.type_t), typing.get_args(self.type_t):
            case builtins.dict, (Key, Value):
                assert isinstance(arg, dict)
                return {
                    Convert(type_t=Key)._parse(key): Convert(type_t=Value)._parse(value)
                    for key, value in arg.items()
                }
            case builtins.tuple, ():
                assert arg == tuple()
                return arg
            case builtins.tuple, (Value,):
                assert isinstance(arg, tuple) and len(arg) == 1
                return tuple([Convert(type_t=Value)._parse(arg[0])])
            case builtins.tuple, (Value, builtins.Ellipsis):
                assert isinstance(arg, tuple)
                return tuple([Convert(type_t=Value)._parse(value) for value in arg])
            case builtins.tuple, (Value, *Values):
                assert isinstance(arg, tuple) and len(arg) > 0
                return Convert(type_t=Value)._parse(arg[0]), *Convert(type_t=tuple[*Values])._parse(arg[1:])

            case(typing.Union | types.UnionType), Ts:
                assert type(arg) in Ts
                return arg
            case typing.Literal, Vs:
                assert arg in Vs
                return arg

            case T_, _:
                return T_(arg)


    def _parse(self, arg: _Arg, /) -> T:
        return self._from_type(arg) if typing.get_origin(self.type_t) is None else self._from_type_alias(arg)

    def __call__(self, arg: str, /) -> T:
        """Returns a T parsed from given arg or throws an _Exception upon failure."""

        if self.type_t != str:
            try:
                arg: Convert._Arg = ast.literal_eval(arg)
            except (SyntaxError, ValueError,):
                pass

        try:
            value = self._parse(arg)
        except AssertionError as e:
            raise Exception(f'Could not parse {arg=!r}. {e}.')

        return value
