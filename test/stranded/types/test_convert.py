import dataclasses
import enum
import types
import typing

import pytest

from stranded.types import Convert


@pytest.mark.parametrize(
    't,arg,expect',
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
def test_convert_primitive_succeeds[T](t: type[T], arg: str, expect: T) -> None:
    assert Convert(t=t)(arg) == expect


@pytest.mark.parametrize(
    't,arg,expect',
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
def test_convert_type_alias_succeeds[T](t: type[T], arg: str, expect: T) -> None:
    assert Convert(t=t)(arg) == expect


class TestEnum(enum.Enum):
    foo = 1
    bar = 2
    baz = 3


@pytest.mark.parametrize(
    't,arg,expect',
    (
        (TestEnum, 'foo', TestEnum.foo),
        (TestEnum, 'bar', TestEnum.bar),
        (TestEnum, 'baz', TestEnum.baz),
    ),
)
def test_convert_enum_succeeds[T](t: type[T], arg: str, expect: T) -> None:
    assert Convert(t=t)(arg) == expect


@pytest.mark.parametrize(
    't,arg,expect',
    (
        (int | str | float, '42', 42),
        (int | str | float, '"foo"', 'foo'),
        (int | str | float, '3.14', 3.14),
        (typing.Union[int, str, float], '42', 42),
        (typing.Union[int, str, float], '"foo"', 'foo'),
        (typing.Union[int, str, float], '3.14', 3.14),
    ),
)
def test_convert_union_succeeds[T](t: type[T], arg: str, expect: T) -> None:
    assert Convert(t=t)(arg) == expect


@dataclasses.dataclass(frozen=True)
class CustomType[T]:
    a: T


@pytest.mark.parametrize(
    't,arg,expect',
    (
        (CustomType, '42', CustomType(42)),
        (CustomType, '"foo"', CustomType('foo')),
        (CustomType, '3.14', CustomType(3.14)),
        (CustomType[int], '42', CustomType(42)),
        (CustomType[str], '"foo"', CustomType('foo')),
        (CustomType[float], '3.14', CustomType(3.14)),
    ),
)
def test_convert_custom_type_succeeds[T](t: type[T], arg: str, expect: T) -> None:
    assert Convert(t=t)(arg) == expect


@dataclasses.dataclass(frozen=True)
class ComplexCustomType[T, U, V]:
    a: T
    b: U
    c: V


@pytest.mark.parametrize(
    't,arg,expect',
    (
        (ComplexCustomType[int, float, str], '42, 3.14, "foo"', ComplexCustomType(42, 3.14, 'foo')),
        (ComplexCustomType[str, CustomType[str] , CustomType[TestEnum]], '"foo", "foo", "foo"', ComplexCustomType("foo", CustomType("foo"), CustomType(TestEnum.foo))),
    ),
)
def test_convert_complex_custom_type_succeeds[T](t: type[T], arg: str, expect: T) -> None:
    assert Convert(t=t)(arg) == expect
