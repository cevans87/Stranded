from __future__ import annotations

import abc
import dataclasses
import enum
import inspect
import typing

from stranded import types

from stranded.abc import composer_
from stranded.builtins import exception_


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Annotation[T](abc.ABC):
    t: T
    comment: str = ""

    @abc.abstractmethod
    def to_short_str(self) -> str: ...

    @abc.abstractmethod
    def to_long_str(self) -> str: ...

    def to_type_str(self) -> str:
        if typing.get_origin(self.t) is typing.Literal:
            return f'literal: {{{', '.join(map(str, typing.get_args(self.t)))}}}'
        if isinstance(self.t, type) and issubclass(self.t, enum.Enum):
            return f'enum: {{{', '.join(self.t._member_names_)}}}'
        return f'type: {self.t.__name__}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Parameter[T](_Annotation[T], abc.ABC):
    name: str

    def __call__(self, arg: str) -> T:
        return types.Convert(t=self.t)(arg)

    def to_long_str(self) -> str:
        return '\n'.join((
            f'    {self.to_short_str()}',
            f'        {self.to_type_str()}',
            *((f'        {self.comment}',) if self.comment else ()),
        ))


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredParameter[T](_Parameter[T], abc.ABC):

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])
            case _:
                raise RuntimeError()


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalParameter[T](_Parameter[T], abc.ABC):
    default: T

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t, default=parameter.default)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment, default=parameter.default)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts], default=parameter.default)
            case _:
                raise RuntimeError()


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VariadicParameter[T](_Parameter[T], abc.ABC):

    @classmethod
    def of_parameter(cls, parameter: inspect.Parameter, /) -> typing.Self:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])
            case _:
                raise RuntimeError()


@dataclasses.dataclass(frozen=True, kw_only=True)
class _StackedParameter[T](_Parameter[T], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredPositionalParameter[T](_RequiredParameter[T], _StackedParameter[T]):

    def to_short_str(self) -> str:
        return f'<{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalPositionalParameter[T](_OptionalParameter[T], _StackedParameter[T]):

    def to_short_str(self) -> str:
        return f'[<{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VariadicPositionalParameter[T](_VariadicParameter[T], _StackedParameter[T]):

    def to_short_str(self) -> str:
        return f'[<{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _KeywordParameter[T](_Parameter[T], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredKeywordParameter[T](_RequiredParameter[T], _KeywordParameter[T]):

    def to_short_str(self) -> str:
        return f'--{self.name} <{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalKeywordParameter[T](_OptionalParameter[T], _KeywordParameter[T]):

    def to_short_str(self) -> str:
        return f'[-{self.name}]' if (self.t == bool and self.default == False) else (
            f'[--{self.name} <{self.name}({self.default})>]'
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VariadicKeywordParameter[T](_VariadicParameter[T], _KeywordParameter[T]):

    def to_short_str(self) -> str:
        return f'[--{self.name} <{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _ReturnAnnotation[T](_Annotation[T]):

    @staticmethod
    def of_annotation(annotation: type) -> _ReturnAnnotation[typing.Any]:
        match annotation, typing.get_origin(annotation), typing.get_args(annotation):
            case t, None, ():
                return _ReturnAnnotation(t=t)
            case _, typing.Annotated, (t, *_, comment):
                return _ReturnAnnotation(t=t, comment=comment)
            case _, t, ts:
                return _ReturnAnnotation(t=t[*ts])  # type: ignore[index]
            case _:
                raise RuntimeError(f'{annotation=}. Cannot create return annotation.')

    def to_short_str(self) -> str:
        return ''

    def to_long_str(self) -> str:
        return '\n'.join((
            f'    {self.t}',
            *((f'        {self.comment}',) if self.comment else ()),
        ))


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Signature:
    return_annotation: _ReturnAnnotation[typing.Any]

    # Parameters that are detected by position.
    optional_positional_parameter_by_name: dict[str, _OptionalPositionalParameter[typing.Any]]
    required_positional_parameter_by_name: dict[str, _RequiredPositionalParameter[typing.Any]]
    variadic_positional_parameter: _VariadicPositionalParameter[typing.Any] | None

    # Flags that are detected by two leading dashes.
    optional_keyword_parameter_by_name: dict[str, _OptionalKeywordParameter[typing.Any]]
    required_keyword_parameter_by_name: dict[str, _RequiredKeywordParameter[typing.Any]]
    variadic_keyword_parameter: _VariadicKeywordParameter[typing.Any] | None

    ReturnAnnotation: typing.ClassVar = _ReturnAnnotation

    RequiredPositionalParameter: typing.ClassVar = _RequiredPositionalParameter
    OptionalPositionalParameter: typing.ClassVar = _OptionalPositionalParameter
    VariadicPositionalParameter: typing.ClassVar = _VariadicPositionalParameter

    RequiredKeywordParameter: typing.ClassVar = _RequiredKeywordParameter
    OptionalKeywordParameter: typing.ClassVar = _OptionalKeywordParameter
    VariadicKeywordParameter: typing.ClassVar = _VariadicKeywordParameter

    @property
    def variadic_parameter_by_name(self) -> dict[str, _VariadicParameter[typing.Any]]:
        return {
            parameter.name: parameter
            for parameter in (self.variadic_positional_parameter, self.variadic_keyword_parameter)
            if parameter is not None
        }

    @property
    def keyword_parameter_by_name(self) -> dict[str, _KeywordParameter[typing.Any]]:
        return self.optional_keyword_parameter_by_name | self.required_keyword_parameter_by_name  # type: ignore[no-any-return, operator]

    @property
    def positional_parameter_by_name(self) -> dict[str, _StackedParameter[typing.Any]]:
        return self.optional_positional_parameter_by_name | self.required_positional_parameter_by_name  # type: ignore[no-any-return, operator]

    @property
    def parameter_by_name(self) -> dict[str, _Parameter[typing.Any]]:
        return self.variadic_parameter_by_name | self.positional_parameter_by_name | self.keyword_parameter_by_name  # type: ignore[no-any-return, operator]

    @property
    def annotations(self) -> tuple[_Annotation[typing.Any], ...]:
        return self.return_annotation, *self.parameter_by_name.values()

    def __call__(self, *argv: str) -> _BoundSignature:
        args = list(reversed(argv))

        required_positional_parameter_by_name = dict(self.required_positional_parameter_by_name)
        optional_positional_parameter_by_name = dict(self.optional_positional_parameter_by_name)

        required_keyword_parameter_by_name = dict(self.required_keyword_parameter_by_name)
        optional_keyword_parameter_by_name = dict(self.optional_keyword_parameter_by_name)

        positional_value_by_name = dict()
        variadic_positional_values = []

        keyword_value_by_name = dict()
        variadic_keyword_value_by_name = dict()

        while args:
            match args[-1].split('-'):

                case ('', '', name) if parameter := required_keyword_parameter_by_name.pop(name, None):
                    args.pop()
                    keyword_value_by_name[name] = parameter(args.pop())
                case ('', '', name) if parameter := optional_keyword_parameter_by_name.pop(name, None):  # type: ignore[assignment]
                    args.pop()
                    keyword_value_by_name[name] = parameter(args.pop())
                case ('', '', name) if parameter := self.variadic_keyword_parameter:  # type: ignore[assignment]
                    args.pop()
                    variadic_keyword_value_by_name[name] = parameter(args.pop())
                case ('', '', _) if parameter := self.variadic_positional_parameter:  # type: ignore[assignment]
                    variadic_positional_values += [args.pop(), parameter(args.pop())]

                # Special cases of keyword arguments where type is bool.
                case ('', name) if (
                    (parameter := required_keyword_parameter_by_name.pop(name, None))
                    and (parameter.t == bool)
                ):
                    args.pop()
                    keyword_value_by_name[name] = True
                case ('', name) if (
                    (parameter := optional_keyword_parameter_by_name.pop(name, None))  # type: ignore[assignment]
                    and (parameter.t == bool)
                    and (parameter.default == False)
                ):
                    args.pop()
                    keyword_value_by_name[name] = True
                case ('', name) if self.variadic_keyword_parameter and (self.variadic_keyword_parameter.t == bool):
                    args.pop()
                    variadic_keyword_value_by_name[name] = True
                case ('', _) if self.variadic_positional_parameter and (self.variadic_positional_parameter.t == bool):
                    args.pop()
                    variadic_positional_values.append(True)

                case (_arg,):
                    break

        while args:
            match args[-1]:
                case arg if required_positional_parameter_by_name:
                    name, parameter = required_positional_parameter_by_name.popitem()  # type: ignore[assignment]
                    positional_value_by_name[name] = parameter(args.pop())  # type: ignore[misc]
                case arg if optional_positional_parameter_by_name:
                    name, parameter = optional_positional_parameter_by_name.popitem()  # type: ignore[assignment]
                    positional_value_by_name[name] = parameter(args.pop())  # type: ignore[misc]
                case arg if parameter := self.variadic_positional_parameter:  # type: ignore[assignment]
                    variadic_positional_values.append(parameter(args.pop()))

                case _:
                    raise RuntimeError(f'Could not parse {arg=}.')

        return _BoundSignature(
            return_annotation=self.return_annotation,

            required_positional_parameter_by_name=self.required_positional_parameter_by_name,
            optional_positional_parameter_by_name=self.optional_positional_parameter_by_name,

            required_keyword_parameter_by_name=self.required_keyword_parameter_by_name,
            optional_keyword_parameter_by_name=self.optional_keyword_parameter_by_name,

            variadic_positional_parameter=self.variadic_positional_parameter,
            variadic_keyword_parameter=self.variadic_keyword_parameter,

            positional_value_by_name=positional_value_by_name,
            keyword_value_by_name=keyword_value_by_name,

            variadic_positional_values=variadic_positional_values,
            variadic_keyword_value_by_name=variadic_keyword_value_by_name,
        )

    @staticmethod
    def of_signature(signature: inspect.Signature, /) -> _Signature:
        variadic_keyword_parameter: _VariadicKeywordParameter[typing.Any] | None = None
        variadic_positional_parameter: _VariadicPositionalParameter[typing.Any] | None = None
        optional_keyword_parameter_by_name: dict[str, _OptionalKeywordParameter[typing.Any]] = {}
        required_keyword_parameter_by_name: dict[str, _RequiredKeywordParameter[typing.Any]] = {}
        optional_positional_parameter_by_name: dict[str, _OptionalPositionalParameter[typing.Any]] = {}
        required_positional_parameter_by_name: dict[str, _RequiredPositionalParameter[typing.Any]] = {}

        for parameter in reversed(signature.parameters.values()):  # type: ignore[call-overload]
            match parameter:
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_ONLY, default=parameter.empty):
                    required_positional_parameter_by_name[name] = _RequiredPositionalParameter.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_ONLY):
                    optional_positional_parameter_by_name[name] = _OptionalPositionalParameter.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_OR_KEYWORD, default=parameter.empty):
                    required_positional_parameter_by_name[name] = _RequiredPositionalParameter.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_OR_KEYWORD):
                    optional_keyword_parameter_by_name[name] = _OptionalKeywordParameter.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.KEYWORD_ONLY, default=parameter.empty):
                    required_keyword_parameter_by_name[name] = _RequiredKeywordParameter.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.KEYWORD_ONLY):
                    optional_keyword_parameter_by_name[name] = _OptionalKeywordParameter.of_parameter(parameter)

                case inspect.Parameter(kind=parameter.VAR_KEYWORD):
                    variadic_keyword_parameter = _VariadicKeywordParameter.of_parameter(parameter)
                case inspect.Parameter(kind=parameter.VAR_POSITIONAL):
                    variadic_positional_parameter = _VariadicPositionalParameter.of_parameter(parameter)

        return _Signature(
            return_annotation=_ReturnAnnotation[typing.Any].of_annotation(signature.return_annotation),
            optional_positional_parameter_by_name=optional_positional_parameter_by_name,
            required_positional_parameter_by_name=required_positional_parameter_by_name,
            optional_keyword_parameter_by_name=optional_keyword_parameter_by_name,
            required_keyword_parameter_by_name=required_keyword_parameter_by_name,
            variadic_keyword_parameter=variadic_keyword_parameter,
            variadic_positional_parameter=variadic_positional_parameter,
        )

    @staticmethod
    def of_signatures(left_signature: _Signature, /, *signatures: _Signature) -> _Signature:
        for right_signature in signatures:
            for name in (
                (left_parameter_by_name := left_signature.parameter_by_name).keys()
                & (right_parameter_by_name := right_signature.parameter_by_name).keys()
            ):
                assert (
                    left_parameter := left_parameter_by_name[name]
                ) == (
                    right_parameter := right_parameter_by_name[name]
                ), (
                    f'Cannot merge conflicting CLI signatures with {left_parameter=} and {right_parameter=}.'
                )

            left_signature = _Signature(
                required_positional_parameter_by_name=(
                    right_signature.required_positional_parameter_by_name
                    | left_signature.required_positional_parameter_by_name
                ),
                optional_positional_parameter_by_name=(
                    right_signature.optional_positional_parameter_by_name
                    | left_signature.optional_positional_parameter_by_name
                ),
                required_keyword_parameter_by_name=(
                    right_signature.required_keyword_parameter_by_name
                    | left_signature.required_keyword_parameter_by_name
                ),
                optional_keyword_parameter_by_name=(
                    right_signature.optional_keyword_parameter_by_name
                    | left_signature.optional_keyword_parameter_by_name
                ),
                variadic_positional_parameter=(
                    right_signature.variadic_positional_parameter
                    or left_signature.variadic_positional_parameter
                ),
                variadic_keyword_parameter=(
                    right_signature.variadic_keyword_parameter
                    or left_signature.variadic_keyword_parameter
                ),
                return_annotation=right_signature.return_annotation,
            )

        return left_signature

    def to_short_str(self) -> str:
        return ' '.join((value.to_short_str() for value in reversed(self.annotations))).rstrip()

    def to_long_str(self) -> str:
        return '\n'.join((value.to_long_str() for value in reversed(self.annotations))).rstrip()


@dataclasses.dataclass(frozen=True, kw_only=True)
class _BoundSignature(_Signature):
    positional_value_by_name: dict[str, object]
    keyword_value_by_name: dict[str, object]

    variadic_positional_values: list[object]
    variadic_keyword_value_by_name: dict[str, object]

    def __call__(self, composeds: typing.Iterable[Composed[..., typing.Any]]) -> typing.Iterable[typing.Callable[..., typing.Any]]:  # type: ignore[override]
        for composed in composeds:
            composee_signature = inspect.signature(composed.composee)
            yield lambda: composed.composee(
                *(
                    value for name, value in self.positional_value_by_name.items()
                    if name in composee_signature.parameters
                       and isinstance(self.parameter_by_name[name], _StackedParameter)
                ),
                *(
                    value for value in self.variadic_positional_values
                    if self.variadic_positional_parameter.name in composee_signature.parameters  # type: ignore[union-attr]
                ),
                **{
                    name: value for name, value in self.keyword_value_by_name.items()
                    if name in composee_signature.parameters
                       and isinstance(self.parameter_by_name[name], _KeywordParameter)
                },
                **{
                    name: value for name, value in self.variadic_keyword_value_by_name.items()
                    if self.variadic_keyword_parameter.name in composee_signature.parameters  # type: ignore[union-attr]
                },
            )


class Exception(exception_.Exception): ...  # noqa


@typing.runtime_checkable
class Composee[**ParamT, RetT](composer_.Composee[ParamT, RetT], typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**ParamT, RetT](composer_.Connect[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**ParamT, RetT](composer_.Exit[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**ParamT, RetT](composer_.Enter[ParamT, RetT], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Composed[**ParamT, RetT](composer_.Composed[ParamT, RetT], abc.ABC):
    composee: Composee[ParamT, RetT]
    children: tuple[typing.Self, typing.Self] | None = None

    @property
    def composeds(self) -> tuple[typing.Self, ...]:
        match self.children:
            case None:
                return self,
            case left, right:
                return *left.composeds, *right.composeds
            case _:
                raise RuntimeError(f'{self.children=}. Expected {self.__annotations__['children']}')

    def __call__(self, *argv: str) -> typing.Iterable[typing.Callable[..., typing.Any]]:
        yield from self.to_signature()(*argv)(self.composeds)


    def __or__[Composed2T: Composed[..., typing.Any]](self, other: Composed2T) -> Composed2T:
        return dataclasses.replace(other, children=(self, other))

    def __xor__[Composed2T: Composed[..., typing.Any]](self, other: Composed2T) -> Composed2T:  # type: ignore[empty-body]
        # TODO make this mark flags in the two CLI's as mutually exclusive.
        ...

    def __str__(self) -> str:
        return '\n'.join([
            f'{self.__doc__}',
            '',
            f'{self.__signature__}',
        ])

    def to_long_str(self) -> str:
        return '\n\n'.join([
            self.to_signature().to_short_str(),
            f'{self.__doc__}',
            self.to_signature().to_long_str(),
        ])

    def to_signature(self) -> _Signature:
        return _Signature.of_signature(inspect.signature(self.composee, eval_str=True)) if self.children is None else (
            _Signature.of_signatures(self.children[0].to_signature(), self.children[1].to_signature())
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class ArgumentParser[**ParamT, RetT](composer_.Composer[ParamT, RetT], abc.ABC):
    type HT = typing.Annotated[bool, 'Print help and exit.']
    type LogLevelT = typing.Annotated[
        typing.Literal['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'],
        'Log level to set.',
    ]

    type ComposeeT = Composee[ParamT, RetT]
    type ConnectT = Connect[ParamT, RetT]
    type ExitT = Exit[ParamT, RetT]
    type EnterT = Enter[ParamT, RetT]
    type ComposedT = Composed[ParamT, RetT]
    type ComposerT = ArgumentParser[ParamT, RetT]

    Signature: typing.ClassVar = _Signature
    Composee: typing.ClassVar[type[Composee[typing.Any, typing.Any]]]
    Connect: typing.ClassVar[type[Connect[typing.Any, typing.Any]]]
    Exit: typing.ClassVar[type[Exit[typing.Any, typing.Any]]]
    Enter: typing.ClassVar[type[Enter[typing.Any, typing.Any]]]
    Composed: typing.ClassVar[type[Composed[typing.Any, typing.Any]]]
    Composer: typing.ClassVar[type[ArgumentParser[typing.Any, typing.Any]]]

    def __call__(self, composee: ComposeeT, /) -> ComposedT:
        return self.Composed(  # type: ignore[return-value]
            __doc__=str(composee.__doc__),
            __module__=str(composee.__module__),
            __name__=str(composee.__name__),
            __qualname__=str(composee.__qualname__),
            __signature__=inspect.signature(composee).replace(
                parameters=(inspect.Parameter('argv', inspect.Parameter.VAR_POSITIONAL, annotation=str),),
            ),
            composee=composee,
            composer=self,
            stack=(self.Enter(composer=self, composee=composee),),
        )


Composer = ArgumentParser
