from __future__ import annotations

import abc
import annotated_types
import argparse
import ast
import builtins
import dataclasses
import enum
import inspect
import logging
import pprint
import types
import typing

from . import decorator


class Exception(decorator.Exception): ...  # noqa


@dataclasses.dataclass(frozen=True, kw_only=True)
class ParseOne[T]:
    t: type[T]

    type _Arg = bool | float | int | str | list | dict | set | None

    def _parse_arg(self, arg: _Arg, /) -> T:
        match self.t if (origin := typing.get_origin(self.t)) is None else (origin, typing.get_args(self.t)):
            case types.NoneType | None:
                assert arg is None, f'{self} expected `None`, got `{arg}`.'
            case builtins.bool | builtins.int | builtins.float | builtins.str:
                assert isinstance(arg, self.t), f'{self} expected `{self.t}`, got `{arg}`'
            case (builtins.frozenset | builtins.list | builtins.set), (Value,):
                assert isinstance(arg, (list, set))
                arg = origin([ParseOne(t=Value)._parse_arg(value) for value in arg])
            case builtins.dict, (Key, Value):
                assert isinstance(arg, dict)
                arg = {
                    ParseOne(t=Key)._parse_arg(key): ParseOne(t=Value)._parse_arg(value) for key, value in arg.items()
                }

            case builtins.tuple, ():
                assert arg == tuple()
            case builtins.tuple, (Value,):
                assert isinstance(arg, tuple) and len(arg) == 1
                arg = tuple([ParseOne(t=Value)._parse_arg(arg[0])])
            case builtins.tuple, (Value, builtins.Ellipsis):
                assert isinstance(arg, tuple)
                arg = tuple([ParseOne(t=Value)._parse_arg(value) for value in arg])
            case builtins.tuple, (Value, *Values):
                assert isinstance(arg, tuple) and len(arg) > 0
                arg = (ParseOne(t=Value)._parse_arg(arg[0]), *ParseOne(t=tuple[*Values])._parse_arg(arg[1:]))

            case (typing.Union | types.UnionType), Values:
                assert type(arg) in Values
            case typing.Literal, Values:
                assert arg in Values

            case (Value, _) | Value if issubclass(Value, enum.Enum):
                assert isinstance(arg, str) and hasattr(Value, arg)
                arg = getattr(Value, arg)

            case (Value, _) | Value:
                arg = Value(arg)

        return arg

    def parse_arg(self, arg: str, /) -> T:
        """Returns a T parsed from given arg or throws an _Exception upon failure."""

        if self.t != str:
            try:
                arg: ParseOne._Arg = ast.literal_eval(arg)
            except (SyntaxError, ValueError,):
                pass

        try:
            value = self._parse_arg(arg)
        except AssertionError as e:
            raise Exception(f'Could not parse {arg=!r}. {e}.')

        return value


@dataclasses.dataclass(frozen=True, kw_only=True)
class _AddArgument[T]:
    """Generates and collects sane argument defaults intended for argparse.ArgumentParser.add_argument(...).

    Any _Annotation fields that are not `Ellipses` should be passed to <parser instance>.add_argument(...) to add a
    flag.
    """
    name_or_flags: list[str] = ...
    action: typing.Type[argparse.Action] | typing.Literal[
        'store',
        'store_const',
        'store_true',
        'store_false',
        'append',
        'append_const',
        'count',
        'help',
        'version',
    ] = ...
    choices: typing.Iterable[T] = ...
    const: T = ...
    default: T = ...
    dest: str = ...
    help: str = ...
    metavar: str | None = ...
    nargs: typing.Annotated[int, annotated_types.Ge(0) | typing.Literal[
        '?',
        '*',
        '+'
    ]] = ...
    required: bool = ...
    type: typing.Callable[[str], T] = ...

    @staticmethod
    def of_parameter(parameter: inspect.Parameter, /) -> _AddArgument[T]:
        """Returns an _Annotation converted from given `parameter`.

        `parameter.annotation` may be of `typing.Annotated[T, <annotations>...]`. If an _Annotation instance is included
        in the annotations, non-Ellipses fields will override anything this method would normally generate. This is
        useful if special argparse behavior for the argument is desired.

        ref. https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument
        """

        # TODO: Can I evaluate this annotation the same way I do somewhere else in this file?
        assert not isinstance(parameter.annotation, str), (
            f'{parameter.annotation=!r} is not evaluated. You may need to manually evaluate this annotation.'
            f' See https://peps.python.org/pep-0563/#resolving-type-hints-at-runtime.'
        )

        add_argument = _AddArgument()
        t = parameter.annotation

        help_lines = []
        if typing.get_origin(t) is typing.Annotated:
            t, *args = typing.get_args(t)
            help_lines += [*filter(lambda arg: isinstance(arg, str), args)]
            for override_add_arguments in filter(lambda arg: isinstance(arg, _AddArgument), args):
                add_argument = dataclasses.replace(
                    add_argument,
                    **dict(filter(
                        lambda item: item[1] is not ...,
                        dataclasses.asdict(override_add_arguments).items(),
                    )),
                )

        if add_argument.name_or_flags is ...:
            match parameter.kind, parameter.default == parameter.empty:
                case (
                (parameter.POSITIONAL_ONLY, _)
                | ((parameter.VAR_POSITIONAL | parameter.POSITIONAL_OR_KEYWORD), True)
                ):
                    add_argument = dataclasses.replace(add_argument, name_or_flags=[parameter.name])
                case (parameter.KEYWORD_ONLY, _) | (parameter.POSITIONAL_OR_KEYWORD, False):
                    add_argument = dataclasses.replace(
                        add_argument, name_or_flags=[f'--{parameter.name.replace('_', '-')}']
                    )

        if add_argument.action is ...:
            match parameter.kind:
                case inspect.Parameter.VAR_POSITIONAL:
                    add_argument = dataclasses.replace(add_argument, action='append')

        if add_argument.choices is ...:
            match typing.get_origin(t) or type(t):
                case typing.Literal:
                    add_argument = dataclasses.replace(add_argument, choices=typing.get_args(t))
                case enum.EnumType:
                    add_argument = dataclasses.replace(add_argument, choices=tuple(t))

        # No automatic actions needed for 'const'.

        if add_argument.default is ...:
            if parameter.default != parameter.empty:
                add_argument = dataclasses.replace(add_argument, default=parameter.default)

        if add_argument.help is ...:
            if add_argument.default is not ...:
                help_lines.append(f'default: {add_argument.default!r}')
            if add_argument.choices is not ...:
                match typing.get_origin(t) or type(t):
                    case enum.EnumType:
                        choice_names = tuple(map(lambda value: value.name, t))
                    case _:
                        choice_names = tuple(map(str, add_argument.choices))
                show_choice_names = tuple(filter(lambda choice_name: not choice_name.startswith('_'), choice_names))
                help_lines.append(
                    f'choices: {pprint.pformat(show_choice_names, compact=True, width=60)}'
                )
            help_lines.append(f'type: {typing.Literal if typing.get_origin(t) is typing.Literal else t!r}')
            add_argument = dataclasses.replace(add_argument, help='\n'.join(help_lines))

        if add_argument.metavar is ...:
            if add_argument.choices is not ...:
                add_argument = dataclasses.replace(add_argument, metavar=f'{{{parameter.name}}}')

        if add_argument.nargs is ...:
            match add_argument.action, parameter.kind, parameter.default == parameter.empty:
                case builtins.Ellipsis, (parameter.POSITIONAL_ONLY | parameter.POSITIONAL_OR_KEYWORD), False:
                    add_argument = dataclasses.replace(add_argument, nargs='?')
                case 'append', (parameter.VAR_POSITIONAL | parameter.VAR_KEYWORD), True:
                    add_argument = dataclasses.replace(add_argument, nargs='*')

        if add_argument.required is ...:
            if (parameter.kind == parameter.KEYWORD_ONLY) and (parameter.default == parameter.empty):
                add_argument = dataclasses.replace(add_argument, required=True)

        if add_argument.type is ...:
            if add_argument.action not in {'count', 'store_false', 'store_true'}:
                add_argument = dataclasses.replace(add_argument, type=lambda arg: ParseOne(t=t).parse_arg(arg))

        return add_argument


# Override __init__ so that we can make `_side_effect` positional-only while instantiating.
@dataclasses.dataclass(frozen=True, init=False)
class _SideEffect[T]:
    _side_effect: typing.Callable[[T], T]

    def __init__(self, _side_effect: typing.Callable[[T], T], /) -> None:
        object.__setattr__(self, '_side_effect', _side_effect)


_Help = typing.Annotated[bool, 'Show this help text and exit.']
_LogLevelInt = typing.Annotated[int, annotated_types.Interval(ge=10, le=60)]
_LogLevelStr = typing.Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
_LogLevel = _LogLevelInt | _LogLevelStr
_SubCommand = typing.Literal

@dataclasses.dataclass(frozen=True, kw_only=True)
class _Flag:
    ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Annotated:

    Help: typing.ClassVar[type[_Help]] = _Help
    LogLevelStr: typing.ClassVar[type[_LogLevelStr]] = _LogLevelStr
    LogLevelInt: typing.ClassVar[type[_LogLevelInt]] = _LogLevelInt
    LogLevel: typing.ClassVar[type[_LogLevel]] = _LogLevel

    @staticmethod
    def help() -> type[_Help]:

        class HelpAction(argparse.Action):

            def __init__(
                self,
                option_strings,
                dest=argparse.SUPPRESS,
                default=argparse.SUPPRESS,
                deprecated=False,
                help=None,
                type=None,
            ) -> None:
                super().__init__(
                    option_strings=option_strings,
                    dest=dest,
                    default=default,
                    deprecated=deprecated,
                    help=help,
                    nargs=0,
                    type=type,
                )

            def __call__(
                self,
                parser: argparse.ArgumentParser,
                namespace: argparse.Namespace,
                values: list[object],
                option_string=None,
            ) -> None:
                parser.print_help()
                parser.exit()

        return typing.Annotated[
            _Help,
            _AddArgument[_Help](name_or_flags=['-h', '--help'], action=HelpAction),
        ]

    @staticmethod
    def log_level(logger_or_name: logging.Logger | str, /) -> type[_LogLevel]:
        logger = logger_or_name if isinstance(logger_or_name, logging.Logger) else logging.getLogger(logger_or_name)

        return typing.Annotated[
            _LogLevelStr,
            _AddArgument[_LogLevelStr](name_or_flags=['-l', '--log-level']),
            _SideEffect[_LogLevelStr](lambda log_level: logger.setLevel(log_level))
        ]

    @staticmethod
    def quiet(logger_or_name: logging.Logger | str, /) -> type[_LogLevelInt]:
        logger = logger_or_name if isinstance(logger_or_name, logging.Logger) else logging.getLogger(logger_or_name)

        class QuietAction(argparse.Action):
            def __call__(
                self,
                parser: argparse.ArgumentParser,
                namespace: argparse.Namespace,
                values: list[object],
                option_string=None,
            ) -> None:
                logger.setLevel(level := min(getattr(namespace, self.dest) + 10, logging.CRITICAL + 10))
                setattr(namespace, self.dest, level)

        return typing.Annotated[
            _LogLevelInt,
            _AddArgument[_LogLevelInt](name_or_flags=['-q', '--quiet'], action=QuietAction, nargs=0),
            _SideEffect[_LogLevelInt](lambda verbose: logger.setLevel(verbose))
        ]

    @staticmethod
    def verbose(logger_or_name: logging.Logger | str, /) -> type[_LogLevelInt]:
        logger = logger_or_name if isinstance(logger_or_name, logging.Logger) else logging.getLogger(logger_or_name)

        class VerboseAction(argparse.Action):
            def __call__(
                self,
                parser: argparse.ArgumentParser,
                namespace: argparse.Namespace,
                values: list[object],
                option_string=None,
            ) -> None:
                logger.setLevel(level := max(getattr(namespace, self.dest) - 10, logging.DEBUG))
                setattr(namespace, self.dest, level)

        return typing.Annotated[
            _LogLevelInt,
            _AddArgument[_LogLevelInt](name_or_flags=['-v', '--verbose'], action=VerboseAction, nargs=0),
            _SideEffect[_LogLevelInt](lambda verbose: logger.setLevel(verbose))
        ]


@dataclasses.dataclass(frozen=True, kw_only=True)
class _Persist[** Params, Return]:
    ...
    # TODO: Make a sticky flag that memoizes a flag.


class ArgumentParser[** Params, Return](argparse.ArgumentParser):
    ...


@typing.runtime_checkable
class Decoratee(decorator.Decoratee, typing.Protocol): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[_Enter, _Ret](decorator.Exit[_Enter], abc.ABC):

    @abc.abstractmethod
    def __call__(self, result: decorator.Raise | _Ret) -> ():
        return tuple()


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[_Decoratee, _Exit, _Decorated, **_Param](
    decorator.Enter[_Decoratee, _Exit, _Decorated, _Param],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[_Decoratee, _Exit, _Enter, _Decorator, **_Param, _Ret](
    decorator.Decorated[_Decoratee, _Exit, _Enter, _Decorator],
    abc.ABC,
):
    def __call__(self, *args: str) -> _Ret:
        subcommand_by_name = {subcommand.__name__: subcommand for subcommand in self.decorator.subcommands}
        if args and (subcommand := subcommand_by_name.get(args[0])):
                return subcommand(args[1:])


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[_Decoratee, _Exit, _Enter, _Decorated](
    decorator.Decorator[_Decoratee, _Exit, _Enter, _Decorated],
    abc.ABC,
):
    add_help: bool = True
    subcommands: tuple[_Decoratee, ...]
