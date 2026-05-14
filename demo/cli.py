import logging
import sys
import typing

from stranded.argparse import ArgumentParser
from stranded.logging import Logger

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel('ERROR')


@ArgumentParser()
def help_flag(prog: str, /, *, help: bool = False) -> None:
    if help:
        cli = main
        match prog.split():
            case (_, 'bar'):
                cli = bar_subcommand
            case (_, 'baz'):
                cli = baz_subcommand

        print((help_flag | log_level_flag | cli).to_long_str())
        sys.exit(0)


@ArgumentParser()
def log_level_flag(*, log_level: Logger.Level = 'ERROR') -> None:
    logger.setLevel(log_level)


@ArgumentParser()
@Logger(logger=logger, call_level='DEBUG', ok_level='DEBUG')
def bar_subcommand(b: int) -> dict[str, int]: return locals()


@ArgumentParser()
@Logger(logger=logger, call_level='DEBUG', ok_level='DEBUG')
def baz_subcommand(c: float) -> dict[str, float]: return locals()


@ArgumentParser()
@Logger(logger=logger, call_level='DEBUG', ok_level='DEBUG')
def main(prog: str, subcommand: typing.Literal['bar', 'baz'], /, *args: str) -> None:
    """This is foo documentation."""
    match subcommand:
        case 'bar':
            return (help_flag | log_level_flag | bar_subcommand)(f'{prog} bar', *args)
        case 'baz':
            return (help_flag | log_level_flag | baz_subcommand)(f'{prog} baz', *args)


if __name__ == '__main__':
    (help_flag | log_level_flag | main)(*sys.argv)
