import enum
import types
import typing

import pytest

from mistypes import Convert


@pytest.mark.parametrize(
    'type_t,arg,expect',
    (
        (None, 'None', None),
        (types.NoneType, 'None', None),
        (bool, 'False', False),
        (bool, 'True', True),
        (int, '1', 1),
        (int, '-1', -1),
        (float, '0.0', 0.0),
        (float, '3.14', 3.14),
        (str, 'foo', 'foo'),
    ),
)
def test_convert_primitive_succeeds[T](type_t: type[T], arg: str, expect: T) -> None:
    assert Convert(type_t=type_t)(arg) == expect


@pytest.mark.parametrize(
    'type_t,arg,expect',
    (
        (dict[str, int], '{"foo": 1}', {"foo": 1}),
        (dict[str, dict[int, bool]], '{"foo": {42: False}}', {"foo": {42: False}}),
        (frozenset[str], '{"foo", "bar", "baz"}', frozenset({'foo', 'bar', 'baz'})),
        (list[str], '["foo", "bar", "baz"]', ["foo", "bar", "baz"]),
        (set[str], '{"foo", "bar", "baz"}', {"foo", "bar", "baz"}),
        (tuple[()], '()', ()),
        (tuple[int], '(42,)', (42,)),
        (tuple[int, float, str], '(42, 3.14, "foobar")', (42, 3.14, "foobar")),
        (tuple[int, ...], '()', ()),
        (tuple[int, ...], '(1, 2, 3, 4)', (1, 2, 3, 4)),
    ),
)
def test_convert_type_alias_succeeds[T](type_t: type[T], arg: str, expect: T) -> None:
    assert Convert(type_t=type_t)(arg) == expect


class TestEnum(enum.Enum):
    foo = 1
    bar = 2
    baz = 3


@pytest.mark.parametrize(
    'type_t,arg,expect',
    (
        (TestEnum, 'foo', TestEnum.foo),
        (TestEnum, 'bar', TestEnum.bar),
        (TestEnum, 'baz', TestEnum.baz),
    ),
)
def test_convert_enum_succeeds[T](type_t: type[T], arg: str, expect: T) -> None:
    assert Convert(type_t=type_t)(arg) == expect


@pytest.mark.parametrize(
    'type_t,arg,expect',
    (
        (int | str | float, '42', 42),
        (int | str | float, '"foo"', 'foo'),
        (int | str | float, '3.14', 3.14),
        (typing.Union[int, str, float], '42', 42),
        (typing.Union[int, str, float], '"foo"', 'foo'),
        (typing.Union[int, str, float], '3.14', 3.14),
    ),
)
def test_convert_union_succeeds[T](type_t: type[T], arg: str, expect: T) -> None:
    assert Convert(type_t=type_t)(arg) == expect
