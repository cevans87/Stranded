from __future__ import annotations

import abc
import dataclasses
import typing

from ...abc import decorator


class Exception(decorator.Exception): ...  # noqa


@typing.runtime_checkable
class Decoratee[**_Param, _Ret](
    decorator.Decoratee[_Param, _Ret],
    typing.Protocol,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Connect[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Connect[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Exit[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Exit[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Enter[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Enter[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
): ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorated[**_SenderParam, _SenderRet, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorated[_SenderParam, _SenderRet, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    sender: _Sender


@dataclasses.dataclass(frozen=True, kw_only=True)
class Receiver[**_ReceiverParam, _ReceiverRet, _Receiver, _Exit, _Enter, _Decorated, **_SenderParam, _SenderRet, _Sender](
    decorator.Decorator[_SenderParam, _ReceiverRet, _Receiver, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    def __call__(self, receiver: _Receiver, /,
    ) -> Decorated[_Param, _ReceiverRet, Decoratee[_Param, _ReceiverRet], _Decorator]:
        ...

@dataclasses.dataclass(frozen=True, kw_only=True)
class Sender[**_ReceiverParam, _ReceiverRet, _Receiver, _Exit, _Enter, _Decorated, **_SenderParam, _SenderRet, _Sender](
    decorator.Decorator[_SenderParam, _ReceiverRet, _Receiver, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    def __call__(self, receiver: _Receiver, /,
    ) -> Decorated[_Param, _ReceiverRet, Decoratee[_Param, _ReceiverRet], _Decorator]:
        ...


@dataclasses.dataclass(frozen=True, kw_only=True)
class Decorator[**_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator](
    decorator.Decorator[_Param, _Ret, _Decoratee, _Connect, _Exit, _Enter, _Decorated, _Decorator],
    abc.ABC,
):
    def __call__(self, decoratee: _Decoratee, /) -> _Decorated:
        return self.decorated_t(
            __doc__=str(decoratee.__doc__),
            __module__=str(decoratee.__module__),
            __name__=str(decoratee.__name__),
            __qualname__=str(decoratee.__qualname__),
            __signature__=inspect.signature(decoratee),
            decoratee=decoratee,
            decorator=self,
        )


Connect = Decorator
