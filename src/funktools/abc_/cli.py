from __future__ import annotations

import abc
import dataclasses
import inspect
import typing

import mistypes

from . import decorator as abc_decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Value(abc.ABC):
    t: type | typing.TypeAliasType
    comment: str = ""

    @abc.abstractmethod
    def to_short_str(self) -> str: ...

    @abc.abstractmethod
    def to_long_str(self) -> str: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Arg(_Value, abc.ABC):
    name: str

    def to_long_str(self) -> str:
        return f'    {self.to_short_str():<30}  # {self.t}  # {self.comment}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredArg(_Arg, abc.ABC):

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])


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
class _VarArg(_Arg, abc.ABC):

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])


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
        return f'--{self.name} <{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalKeywordArg(_OptionalArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'[--{self.name} <{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VarStackedArg(_VarArg, _StackedArg):

    def to_short_str(self) -> str:
        return f'[<{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VarKeywordArg(_VarArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'[--{self.name} <{self.name}>]...'


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
    required_stacked_arg_by_name: dict[str, _RequiredStackedArg]
    optional_stacked_arg_by_name: dict[str, _OptionalStackedArg]
    required_keyword_arg_by_name: dict[str, _RequiredKeywordArg]
    optional_keyword_arg_by_name: dict[str, _OptionalKeywordArg]
    var_stacked_arg_by_name: dict[str, _VarStackedArg]
    var_keyword_arg_by_name: dict[str, _VarKeywordArg]
    return_: _Return

    RequiredStackedArg: typing.ClassVar = _RequiredStackedArg
    OptionalStackedArg: typing.ClassVar = _OptionalStackedArg
    RequiredKeywordArg: typing.ClassVar = _RequiredKeywordArg
    OptionalKeywordArg: typing.ClassVar = _OptionalKeywordArg
    VarStackedArg: typing.ClassVar = _VarStackedArg
    VarKeywordArg: typing.ClassVar = _VarKeywordArg
    Return: typing.ClassVar = _Return

    @property
    def arg_by_name(self) -> dict[str, _Arg]:
        return self.stacked_arg_by_name | self.keyword_arg_by_name | self.var_arg_by_name

    @property
    def stacked_arg_by_name(self) -> dict[str, _StackedArg]:
        return self.required_stacked_arg_by_name | self.optional_stacked_arg_by_name

    @property
    def keyword_arg_by_name(self) -> dict[str, _KeywordArg]:
        return self.required_keyword_arg_by_name | self.optional_keyword_arg_by_name

    @property
    def var_arg_by_name(self) -> dict[str, _VarArg]:
        return self.var_stacked_arg_by_name | self.var_keyword_arg_by_name

    @property
    def values(self) -> tuple[_Value, ...]:
        return *self.arg_by_name.values(), self.return_

    @staticmethod
    def of_signature(signature: inspect.Signature, /) -> _Signature:
        required_stacked_arg_by_name: dict[str, _RequiredStackedArg] = {}
        optional_stacked_arg_by_name: dict[str, _OptionalStackedArg] = {}
        required_keyword_arg_by_name: dict[str, _RequiredKeywordArg] = {}
        optional_keyword_arg_by_name: dict[str, _OptionalKeywordArg] = {}
        var_stacked_arg_by_name: dict[str, _VarStackedArg] = {}
        var_keyword_arg_by_name: dict[str, _VarKeywordArg] = {}
        for parameter in signature.parameters.values():
            match parameter:
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_ONLY, default=parameter.empty):
                    required_stacked_arg_by_name[name] = _RequiredStackedArg.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_ONLY):
                    optional_stacked_arg_by_name[name] = _OptionalStackedArg.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_OR_KEYWORD, default=parameter.empty):
                    required_stacked_arg_by_name[name] = _RequiredStackedArg.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_OR_KEYWORD):
                    optional_keyword_arg_by_name[name] = _OptionalKeywordArg.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.KEYWORD_ONLY, default=parameter.empty):
                    required_keyword_arg_by_name[name] = _RequiredKeywordArg.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.KEYWORD_ONLY):
                    optional_keyword_arg_by_name[name] = _OptionalKeywordArg.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.VAR_POSITIONAL):
                    var_stacked_arg_by_name[name] = _VarStackedArg.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.VAR_KEYWORD):
                    var_keyword_arg_by_name[name] = _VarKeywordArg.of_parameter(parameter)

        return _Signature(
            required_stacked_arg_by_name=required_stacked_arg_by_name,
            optional_stacked_arg_by_name=optional_stacked_arg_by_name,
            required_keyword_arg_by_name=required_keyword_arg_by_name,
            optional_keyword_arg_by_name=optional_keyword_arg_by_name,
            var_stacked_arg_by_name=var_stacked_arg_by_name,
            var_keyword_arg_by_name=var_keyword_arg_by_name,
            return_=_Return.of_annotation(signature.return_annotation)
        )

    @staticmethod
    def of_signatures(left_signature: _Signature, /, *signatures: _Signature) -> _Signature:
        for right_signature in signatures:
            for name in (
                (left_arg_by_name := left_signature.arg_by_name).keys()
                & (right_arg_by_name := right_signature.arg_by_name).keys()
            ):
                assert (left_arg := left_arg_by_name[name]) == (right_arg := right_arg_by_name[name]), (
                    f'Cannot merge CLIs with conflicting arguments {left_arg=} and {right_arg=}.'
                )

            left_signature = _Signature(
                required_stacked_arg_by_name=(
                    left_signature.required_stacked_arg_by_name | right_signature.required_stacked_arg_by_name
                ),
                optional_stacked_arg_by_name=(
                    left_signature.optional_stacked_arg_by_name | right_signature.optional_stacked_arg_by_name
                ),
                required_keyword_arg_by_name=(
                    left_signature.required_keyword_arg_by_name | right_signature.required_keyword_arg_by_name
                ),
                optional_keyword_arg_by_name=(
                    left_signature.optional_keyword_arg_by_name | right_signature.optional_keyword_arg_by_name
                ),
                var_stacked_arg_by_name=(
                    right_signature.var_stacked_arg_by_name | right_signature.var_stacked_arg_by_name
                ),
                var_keyword_arg_by_name=(
                    right_signature.var_keyword_arg_by_name | right_signature.var_keyword_arg_by_name
                ),
                return_=right_signature.return_,
            )

        return left_signature

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

    @property
    def decorateds(self) -> tuple[Decorated, ...]:
        match self.children:
            case None:
                return self,
            case left, right:
                return *left.decorateds, *right.decorateds

    def __call__(self, *argv: str) -> typing.Iterable[typing.Callable]:
        raw_args = list(reversed(argv[1:]))
        signature = self.to_signature()
        stacked_arg_by_name = dict(reversed(signature.stacked_arg_by_name.items()))
        keyword_arg_by_name = signature.keyword_arg_by_name
        value_by_name = {}

        while raw_args:
            raw_arg = raw_args.pop()
            match raw_arg.split('-'):
                case (raw_value,):
                    name, arg = stacked_arg_by_name.popitem()
                case ('-', _):
                    # TODO split the single character flags apart.
                    assert False
                case ('-', '-', name):
                    raw_value = raw_args.pop()
                    arg = keyword_arg_by_name.pop(name)
                case _:
                    assert False, f'Unrecognized argument {raw_arg}.'

            value_by_name[name] = mistypes.Convert(t=arg.t)(raw_value)

        for decorated in self.decorateds:
            bound = (signature := inspect.signature(decorated.decoratee)).bind(
                **{name: value for name, value in value_by_name.items() if name in signature.parameters}
            )
            yield lambda: decorated.decoratee(*bound.args, **bound.kwargs)


    def __or__[_Decorated: Decorated](self, other: _Decorated) -> _Decorated:
        return dataclasses.replace(other, children=(self, other))

    def __xor__[_Decorated: Decorated](self, other: _Decorated) -> _Decorated:
        # TODO make this mark flags in the two CLI's as mutually exclusive.
        ...

    def __str__(self) -> str:
        return '\n'.join([
            self.__doc__,
            '',
            f'{self.__signature__}',
        ])


    def to_signature(self) -> _Signature:
        return _Signature.of_signature(inspect.signature(self.decoratee)) if self.children is None else (
            _Signature.of_signatures(self.children[0].to_signature(), self.children[1].to_signature())
        )


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
