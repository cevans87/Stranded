from __future__ import annotations

import abc
import collections
import dataclasses
import inspect
import typing
from _ast import arg

from . import decorator as abc_decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Value(abc.ABC):
    t: type | typing.TypeAliasType
    comment: str | None


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Arg(_Value, abc.ABC):
    name: str

    @abc.abstractmethod
    def to_short_str(self) -> str: ...

    def to_long_str(self) -> str:
        help_text_lines = []
        if self.help_text:
            i, j, k = 0, 0, 0
            while k < len(self.help_text):
                k += 1
                if 72 <= k - i:
                    help_text_lines.append(self.help_text[i:j])
                    i = j
                    j += 1
                elif help_text_lines[k] == ' ':
                    j = k

            if i != k:
                help_text_lines.append(self.help_text[i:k])
        return f'    {self.to_short_str()}# {self.t}# {self.help_text}'



@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredArg(_Arg, abc.ABC):

    @staticmethod
    def _t_of_t(self, t: type) -> type:
        match typing.get_origin(t):
            case typing.Annotated:


    @staticmethod
    def _comment_of_t(t: type) -> str | None:
        match annotation:

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case None, typing.Annotated, (t, *_, comment):
                return cls(t=t, comment=comment)
            case t, None, ():
                return cls(t=t, comment=None)



        return cls(name=parameter.name, t=cls._t_of_parameter(parameter), comment=cls._comment_of_parameter(parameter))


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalArg(_Arg, abc.ABC):
    default: str

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter) -> typing.Self:
        return cls(name=parameter.name, t=parameter.annotation, default=parameter.default)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _StackedArg(_Arg, abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _KeywordArg(_Arg, abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class RequiredStackedArg(_RequiredArg, _StackedArg):

    def to_short_str(self) -> str:
        return f'<{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class OptionalStackedArg(_OptionalArg, _StackedArg):

    def to_short_str(self) -> str:
        return f'[<{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class RequiredKeywordArg(_RequiredArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'--{self.name.replace('_', '-')} <{self.name}>'

@dataclasses.dataclass(frozen=True, kw_only=True)
class OptionalKeywordArg(_OptionalArg, _KeywordArg):

    def to_short_str(self) -> str:
        return f'[--{self.name.replace('_', '-')} <{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class Return(_Value):

    @staticmethod
    def of_annotation(annotation: type) -> Return:
        match annotation, typing.get_origin(annotation), typing.get_args(annotation):
            case None, typing.Annotated, (t, *_, comment):
                return Return(t=t, comment=comment)
            case t, None, ():


    def to_short_str(self) -> str:
        return f'{self.t}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class Signature:

    required_stacked_arg_by_name: dict[str, RequiredStackedArg]
    optional_stacked_arg_by_name: dict[str, OptionalStackedArg]

    required_keyword_arg_by_name: dict[str, RequiredKeywordArg]
    optional_keyword_arg_by_name: dict[str, OptionalKeywordArg]

    return_: Return

    RequiredStackedArg: typing.ClassVar = RequiredStackedArg
    OptionalStackedArg: typing.ClassVar = OptionalStackedArg
    RequiredKeywordArg: typing.ClassVar = RequiredKeywordArg
    OptionalKeywordArg: typing.ClassVar = OptionalKeywordArg
    Return: typing.ClassVar = Return

    def to_short_str(self) -> str:
        return ' '.join(map(lambda arg: arg.to_short_str(), [
            *self.required_stacked_arg_by_name.values(),
            *self.optional_stacked_arg_by_name.values(),
            *self.required_keyword_arg_by_name.values(),
            *self.optional_keyword_arg_by_name.values(),
        ]))

    def to_long_str(self) -> str:
        return ' '.join(map(lambda arg: arg.to_long_str(), [
            *self.required_stacked_arg_by_name.values(),
            *self.optional_stacked_arg_by_name.values(),
            *self.required_keyword_arg_by_name.values(),
            *self.optional_keyword_arg_by_name.values(),
        ]))


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

    self.get_comment()

    def to_signature(self) -> Signature:
        if self.children is None:
            return inspect.signature(self.decoratee)

        required_stacked_args_by_name: dict[str, RequiredStackedArg] = {}
        optional_stacked_args_by_name: dict[str, OptionalStackedArg] = {}
        required_keyword_args_by_name: dict[str, RequiredKeywordArg] = {}
        optional_keyword_args_by_name: dict[str, OptionalKeywordArg] = {}

        args: typing.Mapping[str, _Arg] = collections.ChainMap(
            required_stacked_args_by_name,
            optional_stacked_args_by_name,  # noqa
            required_keyword_args_by_name,  # noqa
            optional_keyword_args_by_name,  # noqa
        )

        for signature in (inspect.signature(decorated.decoratee) for decorated in self.decorateds):
        for signature in map(lambda decorated: inspect.signature(decorated.decoratee), self.decorateds):
            for parameter in signature.parameters.values():
                if arg := args.get(parameter.name, None):
                    t = self.get_t(parameter)
                    comment = self.get_comment(parameter)

                    assert parameter.annotation == arg.t, (
                        'Duplicate parameters in underlying CLIs must have same type.'
                    )

                match parameter.kind, parameter.default:
                    case inspect.Parameter.POSITIONAL_ONLY , parameter.empty:
                        required_stacked_args_by_name[parameter.name] = RequiredStackedArg.of_parameter(parameter)


                        required_stacked_args_by_name[parameter.name] = RequiredStackedArg(
                            name=parameter.name, t=parameter.annotation,
                        )
                    case inspect.Parameter.POSITIONAL_ONLY, _:
                        optional_stacked_args_by_name[parameter.name] = OptionalStackedArg(
                            name=parameter.name, t=parameter.annotation, default=parameter.default,
                        )

                    case inspect.Parameter.POSITIONAL_OR_KEYWORD, parameter.empty:
                        required_stacked_args_by_name[parameter.name] =RequiredStackedArg(
                            name=parameter.name, t=parameter.annotation,
                        )
                    case inspect.Parameter.POSITIONAL_OR_KEYWORD, _:
                        optional_keyword_args_by_name[parameter.name] = OptionalKeywordArg(
                            name=parameter.name, t=parameter.annotation, default=parameter.default,
                        )

                    case inspect.Parameter.KEYWORD_ONLY, parameter.empty:
                        required_keyword_args_by_name[parameter.name] = RequiredKeywordArg(
                            name=parameter.name, t=parameter.annotation,
                        )
                    case inspect.Parameter.KEYWORD_ONLY, _:
                        optional_keyword_args_by_name[parameter.name] = OptionalKeywordArg(
                            name=parameter.name, t=parameter.annotation, default=parameter.default,
                        )

        return Signature(
            required_stacked_arg_by_name=required_stacked_args_by_name,
            optional_stacked_arg_by_name=optional_stacked_args_by_name,
            required_keyword_arg_by_name=required_keyword_args_by_name,
            optional_keyword_arg_by_name=optional_keyword_args_by_name,
            return_=self.__signature__.return_annotation,
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
    type Flag[T, D] = typing.Annotated[T, D]
    type LogLevel = Decorator.Flag[
        typing.Literal['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'],
        'Log level to set.'
    ]

    Signature: typing.ClassVar = Signature

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
