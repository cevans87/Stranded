import logging
import sys
import typing

import funktools

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel('ERROR')


@funktools.Cli()
def help_flag(prog: str, /, *, help: bool = False) -> None:
    if help:
        match prog.split():
            case (_, 'bar'):
                cli = bar_subcommand
            case (_, 'baz'):
                cli = baz_subcommand
            case _:
                cli = main

        print((help_flag | log_level_flag | cli).to_long_str())
        sys.exit(0)


@funktools.Cli()
def log_level_flag(*, log_level: funktools.Cli.LogLevel = 'ERROR') -> None:
    logger.setLevel(log_level)


@funktools.Cli()
@funktools.Log(logger=logger, call_level='DEBUG', ok_level='DEBUG')
def bar_subcommand(b: int) -> dict[str, int]: return locals()


@funktools.Cli()
@funktools.Log(logger=logger, call_level='DEBUG', ok_level='DEBUG')
def baz_subcommand(c: float) -> dict[str, float]: return locals()


@funktools.Cli()
@funktools.Log(logger=logger, call_level='DEBUG', ok_level='DEBUG')
def main(prog: str, subcommand: typing.Literal['bar', 'baz'], /, *args: str) -> None:
    """This is foo documentation."""
    match subcommand:
        case 'bar':
            return (help_flag | log_level_flag | bar_subcommand)(f'{prog} bar', *args)
        case 'baz':
            return (help_flag | log_level_flag | baz_subcommand)(f'{prog} baz', *args)


if __name__ == '__main__':
    (help_flag | log_level_flag | main)(*sys.argv)
