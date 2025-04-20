from __future__ import annotations

import abc
import dataclasses
import inspect
import typing

import mistypes

import funktools.abc_.decorator as abc_decorator


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Annotation[T](abc.ABC):
    t: type[T]
    comment: str = ""

    @abc.abstractmethod
    def to_short_str(self) -> str: ...

    @abc.abstractmethod
    def to_long_str(self) -> str: ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Parameter[T](_Annotation[T], abc.ABC):
    name: str

    def __call__(self, arg: str) -> T:
        return mistypes.Convert(t=self.t)(arg)

    def to_long_str(self) -> str:
        return f'    {self.to_short_str():<30}  # {self.t}  # {self.comment}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredParameter[T](_Parameter[T], abc.ABC):

    @classmethod
    def of_parameter[T](cls: type[T], parameter: inspect.Parameter, /) -> T:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalParameter[T](_Parameter[T], abc.ABC):
    default: str

    @classmethod
    def of_parameter[T](cls: type[T], parameter: inspect.Parameter, /) -> T:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t, default=parameter.default)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment, default=parameter.default)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts], default=parameter.default)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VariadicParameter[T](_Parameter[T], abc.ABC):

    @classmethod
    def of_parameter[T](cls: type[T], parameter: inspect.Parameter, /) -> T:
        match parameter.annotation, typing.get_origin(parameter.annotation), typing.get_args(parameter.annotation):
            case t, None, ():
                return cls(name=parameter.name, t=t)
            case _, typing.Annotated, (t, *_, comment):
                return cls(name=parameter.name, t=t, comment=comment)
            case _, t, ts:
                return cls(name=parameter.name, t=t[*ts])


@dataclasses.dataclass(frozen=True, kw_only=True)
class _StackedParameter[T](_Parameter[T], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _KeywordParameter[T](_Parameter[T], abc.ABC): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredStackedParameter[T](_RequiredParameter[T], _StackedParameter[T]):

    def to_short_str(self) -> str:
        return f'<{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalStackedParameter[T](_OptionalParameter[T], _StackedParameter[T]):

    def to_short_str(self) -> str:
        return f'[<{self.name}({self.default})>]'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _RequiredKeywordParameter[T](_RequiredParameter[T], _KeywordParameter[T]):

    def to_short_str(self) -> str:
        return f'--{self.name} <{self.name}>'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _OptionalKeywordParameter[T](_OptionalParameter[T], _KeywordParameter[T]):

    def to_short_str(self) -> str:
        return f'[--{self.name}]' if self.t == bool and self.default == False else (
            f'[--{self.name} <{self.name}({self.default})>]'
        )


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VariadicStackedParameter[T](_VariadicParameter[T], _StackedParameter[T]):

    def to_short_str(self) -> str:
        return f'[<{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _VariadicKeywordParameter[T](_VariadicParameter[T], _KeywordParameter[T]):

    def to_short_str(self) -> str:
        return f'[--{self.name} <{self.name}>]...'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _ReturnAnnotation[T](_Annotation[T]):

    @staticmethod
    def of_annotation(annotation: type) -> _ReturnAnnotation:
        match annotation, typing.get_origin(annotation), typing.get_args(annotation):
            case t, None, ():
                return _ReturnAnnotation(t=t)
            case _, typing.Annotated, (t, *_, comment):
                return _ReturnAnnotation(t=t, comment=comment)
            case _, t, ts:
                return _ReturnAnnotation(t=t[*ts])
            case _:
                raise RuntimeError(f'{annotation=}. Cannot create return annotation.')

    def to_short_str(self) -> str:
        return ''

    def to_long_str(self) -> str:
        return f'    {' ':<30}  # {self.t}  # {self.comment}'


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Signature:
    return_annotation: _ReturnAnnotation
    variadic_keyword_parameter: _VariadicKeywordParameter | None
    variadic_stacked_parameter: _VariadicStackedParameter | None
    optional_keyword_parameter_by_name: dict[str, _OptionalKeywordParameter]
    required_keyword_parameter_by_name: dict[str, _RequiredKeywordParameter]
    optional_stacked_parameter_by_name: dict[str, _OptionalStackedParameter]
    required_stacked_parameter_by_name: dict[str, _RequiredStackedParameter]

    ReturnAnnotation: typing.ClassVar = _ReturnAnnotation
    VariadicKeywordParameter: typing.ClassVar = _VariadicKeywordParameter
    VariadicStackedParameter: typing.ClassVar = _VariadicStackedParameter
    OptionalKeywordParameter: typing.ClassVar = _OptionalKeywordParameter
    RequiredKeywordParameter: typing.ClassVar = _RequiredKeywordParameter
    OptionalStackedParameter: typing.ClassVar = _OptionalStackedParameter
    RequiredStackedParameter: typing.ClassVar = _RequiredStackedParameter

    @property
    def variadic_parameter_by_name(self) -> dict[str, _VariadicParameter]:
        return {
            parameter_by_name.name: parameter_by_name
            for parameter_by_name in (self.variadic_stacked_parameter, self.variadic_keyword_parameter)
            if parameter_by_name is not None
        }

    @property
    def keyword_parameter_by_name(self) -> dict[str, _KeywordParameter]:
        return self.optional_keyword_parameter_by_name | self.required_keyword_parameter_by_name

    @property
    def stacked_parameter_by_name(self) -> dict[str, _StackedParameter]:
        return self.optional_stacked_parameter_by_name | self.required_stacked_parameter_by_name

    @property
    def parameter_by_name(self) -> dict[str, _Parameter]:
        return self.variadic_parameter_by_name | self.keyword_parameter_by_name | self.stacked_parameter_by_name

    @property
    def annotations(self) -> tuple[_Annotation, ...]:
        return self.return_annotation, *self.parameter_by_name.values()

    def __call__(self, *argv: str) -> _BoundSignature:
        arg_stack = list(reversed(argv))

        stacked_parameter_by_name = dict(self.stacked_parameter_by_name)
        keyword_parameter_by_name = dict(self.keyword_parameter_by_name)

        stacked_value_by_name = dict()
        keyword_value_by_name = dict()
        variadic_stacked_values = []
        variadic_keyword_value_by_name = dict()

        while arg_stack:
            arg = arg_stack.pop()
            match arg.split('-'):
                case ('', '', name) if (
                    (parameter := keyword_parameter_by_name.pop(name, None))
                    and parameter.t == bool
                    and parameter.default == False
                ):
                    keyword_value_by_name[name] = True
                case ('', '', name) if parameter := keyword_parameter_by_name.pop(name, None):
                    keyword_value_by_name[name] = parameter(arg_stack.pop())
                case ('', '', name) if parameter := self.variadic_keyword_parameter:
                    variadic_keyword_value_by_name[name] = parameter(arg_stack.pop())
                case ('', '', _) if parameter := self.variadic_stacked_parameter:
                    variadic_stacked_values += [arg, parameter(arg_stack.pop())]
                case (arg,) if stacked_parameter_by_name:
                    name, parameter = stacked_parameter_by_name.popitem()
                    stacked_value_by_name[name] = parameter(arg)
                case (arg,) if parameter := self.variadic_stacked_parameter:
                    variadic_stacked_values.append(parameter(arg))
                case _:
                    raise RuntimeError(f'{arg=}. Expected valid variable name prefixed with "", "-", or "--".')

        return _BoundSignature(
            return_annotation=self.return_annotation,
            variadic_keyword_parameter=self.variadic_keyword_parameter,
            variadic_stacked_parameter=self.variadic_stacked_parameter,
            optional_keyword_parameter_by_name=self.optional_keyword_parameter_by_name,
            required_keyword_parameter_by_name=self.required_keyword_parameter_by_name,
            optional_stacked_parameter_by_name=self.optional_stacked_parameter_by_name,
            required_stacked_parameter_by_name=self.required_stacked_parameter_by_name,
            stacked_value_by_name=stacked_value_by_name,
            keyword_value_by_name=keyword_value_by_name,
            variadic_stacked_values=variadic_stacked_values,
            variadic_keyword_value_by_name=variadic_keyword_value_by_name,
        )

    @staticmethod
    def of_signature(signature: inspect.Signature, /) -> _Signature:
        variadic_keyword_parameter: _VariadicKeywordParameter | None = None
        variadic_stacked_parameter: _VariadicStackedParameter | None = None
        optional_keyword_parameter_by_name: dict[str, _OptionalKeywordParameter] = {}
        required_keyword_parameter_by_name: dict[str, _RequiredKeywordParameter] = {}
        optional_stacked_parameter_by_name: dict[str, _OptionalStackedParameter] = {}
        required_stacked_parameter_by_name: dict[str, _RequiredStackedParameter] = {}
        for parameter in reversed(signature.parameters.values()):
            match parameter:
                case inspect.Parameter(kind=parameter.VAR_KEYWORD):
                    variadic_keyword_parameter = _VariadicKeywordParameter.of_parameter(parameter)
                case inspect.Parameter(kind=parameter.VAR_POSITIONAL):
                    variadic_stacked_parameter = _VariadicStackedParameter.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.KEYWORD_ONLY, default=parameter.empty):
                    required_keyword_parameter_by_name[name] = _RequiredKeywordParameter.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.KEYWORD_ONLY):
                    optional_keyword_parameter_by_name[name] = _OptionalKeywordParameter.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_OR_KEYWORD, default=parameter.empty):
                    required_stacked_parameter_by_name[name] = _RequiredStackedParameter.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_OR_KEYWORD):
                    optional_keyword_parameter_by_name[name] = _OptionalKeywordParameter.of_parameter(parameter)

                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_ONLY, default=parameter.empty):
                    required_stacked_parameter_by_name[name] = _RequiredStackedParameter.of_parameter(parameter)
                case inspect.Parameter(name=name, kind=parameter.POSITIONAL_ONLY):
                    optional_stacked_parameter_by_name[name] = _OptionalStackedParameter.of_parameter(parameter)

        return _Signature(
            return_annotation=_ReturnAnnotation.of_annotation(signature.return_annotation),
            variadic_keyword_parameter=variadic_keyword_parameter,
            variadic_stacked_parameter=variadic_stacked_parameter,
            optional_keyword_parameter_by_name=optional_keyword_parameter_by_name,
            required_keyword_parameter_by_name=required_keyword_parameter_by_name,
            optional_stacked_parameter_by_name=optional_stacked_parameter_by_name,
            required_stacked_parameter_by_name=required_stacked_parameter_by_name,
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
                required_stacked_parameter_by_name=({}
                    | right_signature.required_stacked_parameter_by_name
                    | left_signature.required_stacked_parameter_by_name
                ),
                optional_stacked_parameter_by_name=({}
                    | right_signature.optional_stacked_parameter_by_name
                    | left_signature.optional_stacked_parameter_by_name
                ),
                required_keyword_parameter_by_name=({}
                    | right_signature.required_keyword_parameter_by_name
                    | left_signature.required_keyword_parameter_by_name
                ),
                optional_keyword_parameter_by_name=({}
                    | right_signature.optional_keyword_parameter_by_name
                    | left_signature.optional_keyword_parameter_by_name
                ),
                variadic_stacked_parameter=(None
                    or right_signature.variadic_stacked_parameter
                    or left_signature.variadic_stacked_parameter
                ),
                variadic_keyword_parameter=(None
                    or right_signature.variadic_keyword_parameter
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
    stacked_value_by_name: dict[str, object]
    keyword_value_by_name: dict[str, object]
    variadic_stacked_values: list[object]
    variadic_keyword_value_by_name: dict[str, object]

    def __call__(self, decorateds: typing.Iterable[Decorated]) -> typing.Iterable[typing.Callable]:
        for decorated in decorateds:
            decoratee_signature = inspect.signature(decorated.decoratee)
            yield lambda: decorated.decoratee(
                *(
                    value for name, value in self.stacked_value_by_name.items()
                    if name in decoratee_signature.parameters
                       and isinstance(self.parameter_by_name[name], _StackedParameter)
                ),
                *(
                    value for value in self.variadic_stacked_values
                    if self.variadic_stacked_parameter.name in decoratee_signature.parameters
                ),
                **{
                    name: value for name, value in self.keyword_value_by_name.items()
                    if name in decoratee_signature.parameters
                       and isinstance(self.parameter_by_name[name], _KeywordParameter)
                },
                **{
                    name: value for name, value in self.variadic_keyword_value_by_name.items()
                    if self.variadic_keyword_parameter.name in decoratee_signature.parameters
                },
            )


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
): ...


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
            case _:
                raise RuntimeError(f'{self.children=}. Expected {self.__annotations__['children']}')

    def __call__(self, *argv: str) -> typing.Iterable[typing.Callable]:
        yield from self.to_signature()(*argv)(self.decorateds)


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

    def to_long_str(self) -> str:
        return '\n\n'.join([
            self.to_signature().to_short_str(),
            self.__doc__,
            self.to_signature().to_long_str(),
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
    LogLevel = typing.Annotated[
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
