from __future__ import annotations

import abc
import dataclasses
import inspect
import typing

from . import decorator as abc_decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Value(abc.ABC):
    t: type | typing.TypeAliasType
    comment: str = ""

    @abc.abstractmethod
    def to_short_str(self) -> str: ...

    @abc.abstractmethod
    def to_long_str(self) -> str: ...

    @staticmethod
    def of_parameter(parameter: inspect.Parameter, /) -> _Value:
        match parameter:
            case inspect.Parameter(kind=parameter.POSITIONAL_ONLY, default=parameter.empty):
                return _RequiredStackedArg.of_parameter(parameter)
            case inspect.Parameter(kind=parameter.POSITIONAL_ONLY):
                return _OptionalStackedArg.of_parameter(parameter)

            case inspect.Parameter(kind=parameter.POSITIONAL_OR_KEYWORD, default=parameter.empty):
                return _RequiredStackedArg.of_parameter(parameter)
            case inspect.Parameter(kind=parameter.POSITIONAL_OR_KEYWORD):
                return _OptionalKeywordArg.of_parameter(parameter)

            case inspect.Parameter(kind=parameter.KEYWORD_ONLY, default=parameter.empty):
                return _RequiredKeywordArg.of_parameter(parameter)
            case inspect.Parameter(kind=parameter.KEYWORD_ONLY):
                return _OptionalKeywordArg.of_parameter(parameter)

            case inspect.Parameter(kind=parameter.VAR_POSITIONAL):
                return _VarStackedArg.of_parameter(parameter)
            case inspect.Parameter(kind=parameter.VAR_KEYWORD):
                return _VarKeywordArg.of_parameter(parameter)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Arg(_Value, abc.ABC):
    name: str

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])

    def to_long_str(self) -> str:
        return f'    {self.to_short_str():<30}  # {self.t}  # {self.comment}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredArg(_Arg, abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalArg(_Arg, abc.ABC):
    default: str

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t, default=parameter.default)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment, default=parameter.default)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts], default=parameter.default)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VarArg(_Arg, abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _StackedArg(_Arg, abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _KeywordArg(_Arg, abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredStackedArg(_RequiredArg, _StackedArg):

    def to_short_str(self) -> str:
        return f'<{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalStackedArg(_OptionalArg, _StackedArg):

    def to_short_str(self) -> str:
        return f'[<{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredKeywordArg(_RequiredArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'--{self.name.replace('_', '-')} <{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalKeywordArg(_OptionalArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'[--{self.name.replace('_', '-')} <{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VarStackedArg(_VarArg, _StackedArg):

    def to_short_str(self) -> str:
        return f'[<{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VarKeywordArg(_VarArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'[--{self.name.replace('_', '-')} <{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Return(_Value):

    @staticmethod
    def of_annotation(annotation: type) -> _Return:
        match annotation, typing.get_origin(annotation), typing.get_args(annotation):
            case t, None, ():
                return _Return(t=t)
            case _, typing.Annotated, (t, *_, comment):
                return _Return(t=t, comment=comment)
            case _, t, ts:
                return _Return(t=t[*ts])

    def to_short_str(self) -> str:
        return ''

    def to_long_str(self) -> str:
        return f'    {' ':<30}  # {self.t}  # {self.comment}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Signature:
    values: tuple[_Value, ...]

    RequiredStackedArg: typing.ClassVar = _RequiredStackedArg
    OptionalStackedArg: typing.ClassVar = _OptionalStackedArg
    RequiredKeywordArg: typing.ClassVar = _RequiredKeywordArg
    OptionalKeywordArg: typing.ClassVar = _OptionalKeywordArg
    VarStackedArg: typing.ClassVar = _VarStackedArg
    VarKeywordArg: typing.ClassVar = _VarKeywordArg
    Return: typing.ClassVar = _Return

    @staticmethod
    def of_signature(signature: inspect.Signature, /) -> _Signature:
        values: list[_Value] = []
        for parameter in signature.parameters.values():
            values.append(_Value.of_parameter(parameter))
        values.append(_Return.of_annotation(signature.return_annotation))

        return _Signature(values=tuple(values))

    @staticmethod
    def of_signatures(*signatures: _Signature) -> _Signature:
        values = []
        for value_t in (
            _RequiredStackedArg,
            _OptionalStackedArg,
            _RequiredKeywordArg,
            _OptionalKeywordArg,
            _VarStackedArg,
            _VarKeywordArg,
        ):
            for signature in signatures:
                values += filter(lambda value: isinstance(value, value_t), signature.values)

        values += filter(lambda value: isinstance(value, _Return), signatures[-1].values)

        return _Signature(values=tuple(values))

    def to_short_str(self) -> str:
        return ' '.join((value.to_short_str() for value in self.values)).rstrip()

    def to_long_str(self) -> str:
        return '\n'.join((value.to_long_str() for value in self.values)).rstrip()


class Exception(abc_decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret, _Decoratee: typing.Self, _Exit, _Enter, _Decorated, _Decorator](
    abc_decorator.Decoratee[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Exit: typing.Self, _Enter, _Decorated, _Decorator](
    abc_decorator.Exit[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    @abc.abstractmethod
    def __call__(self, result: abc_decorator.Raise | _Ret) -> ():
        return tuple()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[** _Param, _Ret, _Decoratee, _Exit, _Enter: typing.Self, _Decorated, _Decorator](
    abc_decorator.Enter[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated: typing.Self, _Decorator](
    abc_decorator.Decorated[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    children: tuple[Decorated, Decorated] | None = None

    def to_signature(self) -> _Signature:
        return _Signature.of_signature(inspect.signature(self.decoratee)) if self.children is None else (
            _Signature.of_signatures(*(decorated.to_signature() for decorated in self.children))
        )

    def __or__[_Decorated: Decorated](self, other: _Decorated) -> _Decorated:
        return dataclasses.replace(
            other,
            children=(self, other)
        )

    def __xor__[_Decorated: Decorated](self, other: _Decorated) -> _Decorated:
        # TODO make this mark flags in the two CLI's as mutually exclusive.
        ...


    def __str__(self) -> str:
        return '\n'.join([
            self.__doc__,
            '',
            f'{self.__signature__}',
        ])


    @property
    def decorateds(self) -> tuple[Decorated, ...]:
        match self.children:
            case None:
                return self,
            case left, right:
                return *left.decorateds, *right.decorateds


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator: typing.Self](
    abc_decorator.Decorator[_Param, _Ret, _Decoratee, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    type LogLevel = typing.Annotated[
        typing.Literal['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'],
        'Log level to set.'
    ]

    Signature: typing.ClassVar = _Signature

    def __call__(self, decoratee: _Decoratee, /) -> _Decorated:
        return self.decorated_t(
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),
            __qualname__=str(decoratee.__qualname__),
            __signature__=inspect.signature(decoratee).replace(
                parameters=(
                    inspect.Parameter('argv', inspect.Parameter.VAR_POSITIONAL),
                ),
            ),
            decoratee=decoratee,
            decorator=self,
        )
