import importlib as _importlib
import types as _types
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import apply_sender
    from .apply_sender import ApplySender
    from . import as_awaitable
    from .as_awaitable import AsAwaitable
    from . import bulk
    from .bulk import Bulk
    from . import bulk_chunked
    from .bulk_chunked import BulkChunked
    from . import bulk_unchunked
    from .bulk_unchunked import BulkUnchunked
    from . import connect
    from .connect import Connect
    from . import continues_on
    from .continues_on import ContinuesOn
    from . import default_domain
    from .default_domain import DefaultDomain
    from . import empty_env
    from .empty_env import EmptyEnv
    from . import ensure_started
    from .ensure_started import EnsureStarted
    from . import env
    from .env import Env
    from . import forwarding_query
    from .forwarding_query import ForwardingQuery
    from . import get_allocator
    from .get_allocator import GetAllocator
    from . import get_completion_scheduler
    from .get_completion_scheduler import GetCompletionScheduler
    from . import get_completion_signatures
    from .get_completion_signatures import GetCompletionSignatures
    from . import get_delegation_scheduler
    from .get_delegation_scheduler import GetDelegationScheduler
    from . import get_domain
    from .get_domain import GetDomain
    from . import get_env
    from .get_env import GetEnv
    from . import get_forward_progress_guarantee
    from .get_forward_progress_guarantee import GetForwardProgressGuarantee
    from . import get_scheduler
    from .get_scheduler import GetScheduler
    from . import get_stop_token
    from .get_stop_token import GetStopToken
    from . import inline_scheduler
    from .inline_scheduler import InlineScheduler
    from . import inplace_stop_callback
    from .inplace_stop_callback import InplaceStopCallback
    from . import inplace_stop_source
    from .inplace_stop_source import InplaceStopSource
    from . import inplace_stop_token
    from .inplace_stop_token import InplaceStopToken
    from . import into_variant
    from .into_variant import IntoVariant
    from . import just
    from .just import Just
    from . import just_error
    from .just_error import JustError
    from . import just_stopped
    from .just_stopped import JustStopped
    from . import let_error
    from .let_error import LetError
    from . import let_stopped
    from .let_stopped import LetStopped
    from . import let_value
    from .let_value import LetValue
    from . import never_stop_token
    from .never_stop_token import NeverStopToken
    from . import operation_state
    from .operation_state import OperationState
    from . import prop
    from .prop import Prop
    from . import read_env
    from .read_env import ReadEnv
    from . import receiver
    from .receiver import Receiver
    from . import run_loop
    from .run_loop import RunLoop
    from . import schedule
    from .schedule import Schedule
    from . import schedule_from
    from .schedule_from import ScheduleFrom
    from . import scheduler
    from .scheduler import Scheduler
    from . import sender
    from .sender import Sender
    from . import set_error
    from .set_error import SetError
    from . import set_stopped
    from .set_stopped import SetStopped
    from . import set_value
    from .set_value import SetValue
    from . import split
    from .split import Split
    from . import start
    from .start import Start
    from . import start_detached
    from .start_detached import StartDetached
    from . import starts_on
    from .starts_on import StartsOn
    from . import static_thread_pool
    from .static_thread_pool import StaticThreadPool
    from . import stop_callback
    from .stop_callback import StopCallback
    from . import stop_source
    from .stop_source import StopSource
    from . import stop_token
    from .stop_token import StopToken
    from . import stopped
    from .stopped import Stopped
    from . import stopped_as_error
    from .stopped_as_error import StoppedAsError
    from . import stopped_as_optional
    from .stopped_as_optional import StoppedAsOptional
    from . import sync_wait
    from .sync_wait import SyncWait
    from . import sync_wait_with_variant
    from .sync_wait_with_variant import SyncWaitWithVariant
    from . import system_context
    from .system_context import SystemContext
    from . import then
    from .then import Then
    from . import transform_env
    from .transform_env import TransformEnv
    from . import transform_sender
    from .transform_sender import TransformSender
    from . import upon_error
    from .upon_error import UponError
    from . import upon_stopped
    from .upon_stopped import UponStopped
    from . import when_all
    from .when_all import WhenAll
    from . import when_all_with_variant
    from .when_all_with_variant import WhenAllWithVariant
    from . import with_awaitable_senders
    from .with_awaitable_senders import WithAwaitableSenders
    from . import with_query_value
    from .with_query_value import WithQueryValue


@_typing.overload
def __getattr__(name: _typing.Literal['apply_sender']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ApplySender']) -> type[ApplySender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['as_awaitable']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['AsAwaitable']) -> type[AsAwaitable]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Bulk']) -> type[Bulk]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_chunked']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['BulkChunked']) -> type[BulkChunked]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_unchunked']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['BulkUnchunked']) -> type[BulkUnchunked]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['connect']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Connect']) -> type[Connect]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['continues_on']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ContinuesOn']) -> type[ContinuesOn]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['default_domain']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['DefaultDomain']) -> type[DefaultDomain]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['empty_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['EmptyEnv']) -> type[EmptyEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ensure_started']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['EnsureStarted']) -> type[EnsureStarted]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Env']) -> type[Env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['forwarding_query']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ForwardingQuery']) -> type[ForwardingQuery]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_allocator']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetAllocator']) -> type[GetAllocator]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetCompletionScheduler']) -> type[GetCompletionScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_signatures']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetCompletionSignatures']) -> type[GetCompletionSignatures]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_delegation_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetDelegationScheduler']) -> type[GetDelegationScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_domain']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetDomain']) -> type[GetDomain]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetEnv']) -> type[GetEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_forward_progress_guarantee']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetForwardProgressGuarantee']) -> type[GetForwardProgressGuarantee]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetScheduler']) -> type[GetScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetStopToken']) -> type[GetStopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inline_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InlineScheduler']) -> type[InlineScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_callback']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopCallback']) -> type[InplaceStopCallback]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_source']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopSource']) -> type[InplaceStopSource]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopToken']) -> type[InplaceStopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['into_variant']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['IntoVariant']) -> type[IntoVariant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Just']) -> type[Just]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['JustError']) -> type[JustError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['JustStopped']) -> type[JustStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetError']) -> type[LetError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetStopped']) -> type[LetStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_value']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetValue']) -> type[LetValue]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['never_stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['NeverStopToken']) -> type[NeverStopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['operation_state']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['OperationState']) -> type[OperationState]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['prop']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Prop']) -> type[Prop]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['read_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ReadEnv']) -> type[ReadEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['receiver']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Receiver']) -> type[Receiver]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['run_loop']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['RunLoop']) -> type[RunLoop]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Schedule']) -> type[Schedule]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule_from']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ScheduleFrom']) -> type[ScheduleFrom]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Scheduler']) -> type[Scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sender']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Sender']) -> type[Sender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetError']) -> type[SetError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetStopped']) -> type[SetStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_value']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetValue']) -> type[SetValue]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['split']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Split']) -> type[Split]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['start']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Start']) -> type[Start]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['start_detached']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StartDetached']) -> type[StartDetached]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['starts_on']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StartsOn']) -> type[StartsOn]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['static_thread_pool']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StaticThreadPool']) -> type[StaticThreadPool]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_callback']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopCallback']) -> type[StopCallback]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_source']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopSource']) -> type[StopSource]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopToken']) -> type[StopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Stopped']) -> type[Stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StoppedAsError']) -> type[StoppedAsError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_optional']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StoppedAsOptional']) -> type[StoppedAsOptional]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SyncWait']) -> type[SyncWait]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait_with_variant']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SyncWaitWithVariant']) -> type[SyncWaitWithVariant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['system_context']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SystemContext']) -> type[SystemContext]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['then']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Then']) -> type[Then]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['TransformEnv']) -> type[TransformEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_sender']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['TransformSender']) -> type[TransformSender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponError']) -> type[UponError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponStopped']) -> type[UponStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WhenAll']) -> type[WhenAll]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all_with_variant']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WhenAllWithVariant']) -> type[WhenAllWithVariant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_awaitable_senders']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WithAwaitableSenders']) -> type[WithAwaitableSenders]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_query_value']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WithQueryValue']) -> type[WithQueryValue]: ...
def __getattr__(name):
    match name:
        case 'apply_sender': return _importlib.import_module('.apply_sender', __name__)
        case 'ApplySender': return _importlib.import_module('.apply_sender', __name__).ApplySender
        case 'as_awaitable': return _importlib.import_module('.as_awaitable', __name__)
        case 'AsAwaitable': return _importlib.import_module('.as_awaitable', __name__).AsAwaitable
        case 'bulk': return _importlib.import_module('.bulk', __name__)
        case 'Bulk': return _importlib.import_module('.bulk', __name__).Bulk
        case 'bulk_chunked': return _importlib.import_module('.bulk_chunked', __name__)
        case 'BulkChunked': return _importlib.import_module('.bulk_chunked', __name__).BulkChunked
        case 'bulk_unchunked': return _importlib.import_module('.bulk_unchunked', __name__)
        case 'BulkUnchunked': return _importlib.import_module('.bulk_unchunked', __name__).BulkUnchunked
        case 'connect': return _importlib.import_module('.connect', __name__)
        case 'Connect': return _importlib.import_module('.connect', __name__).Connect
        case 'continues_on': return _importlib.import_module('.continues_on', __name__)
        case 'ContinuesOn': return _importlib.import_module('.continues_on', __name__).ContinuesOn
        case 'default_domain': return _importlib.import_module('.default_domain', __name__)
        case 'DefaultDomain': return _importlib.import_module('.default_domain', __name__).DefaultDomain
        case 'empty_env': return _importlib.import_module('.empty_env', __name__)
        case 'EmptyEnv': return _importlib.import_module('.empty_env', __name__).EmptyEnv
        case 'ensure_started': return _importlib.import_module('.ensure_started', __name__)
        case 'EnsureStarted': return _importlib.import_module('.ensure_started', __name__).EnsureStarted
        case 'env': return _importlib.import_module('.env', __name__)
        case 'Env': return _importlib.import_module('.env', __name__).Env
        case 'forwarding_query': return _importlib.import_module('.forwarding_query', __name__)
        case 'ForwardingQuery': return _importlib.import_module('.forwarding_query', __name__).ForwardingQuery
        case 'get_allocator': return _importlib.import_module('.get_allocator', __name__)
        case 'GetAllocator': return _importlib.import_module('.get_allocator', __name__).GetAllocator
        case 'get_completion_scheduler': return _importlib.import_module('.get_completion_scheduler', __name__)
        case 'GetCompletionScheduler': return _importlib.import_module('.get_completion_scheduler', __name__).GetCompletionScheduler
        case 'get_completion_signatures': return _importlib.import_module('.get_completion_signatures', __name__)
        case 'GetCompletionSignatures': return _importlib.import_module('.get_completion_signatures', __name__).GetCompletionSignatures
        case 'get_delegation_scheduler': return _importlib.import_module('.get_delegation_scheduler', __name__)
        case 'GetDelegationScheduler': return _importlib.import_module('.get_delegation_scheduler', __name__).GetDelegationScheduler
        case 'get_domain': return _importlib.import_module('.get_domain', __name__)
        case 'GetDomain': return _importlib.import_module('.get_domain', __name__).GetDomain
        case 'get_env': return _importlib.import_module('.get_env', __name__)
        case 'GetEnv': return _importlib.import_module('.get_env', __name__).GetEnv
        case 'get_forward_progress_guarantee': return _importlib.import_module('.get_forward_progress_guarantee', __name__)
        case 'GetForwardProgressGuarantee': return _importlib.import_module('.get_forward_progress_guarantee', __name__).GetForwardProgressGuarantee
        case 'get_scheduler': return _importlib.import_module('.get_scheduler', __name__)
        case 'GetScheduler': return _importlib.import_module('.get_scheduler', __name__).GetScheduler
        case 'get_stop_token': return _importlib.import_module('.get_stop_token', __name__)
        case 'GetStopToken': return _importlib.import_module('.get_stop_token', __name__).GetStopToken
        case 'inline_scheduler': return _importlib.import_module('.inline_scheduler', __name__)
        case 'InlineScheduler': return _importlib.import_module('.inline_scheduler', __name__).InlineScheduler
        case 'inplace_stop_callback': return _importlib.import_module('.inplace_stop_callback', __name__)
        case 'InplaceStopCallback': return _importlib.import_module('.inplace_stop_callback', __name__).InplaceStopCallback
        case 'inplace_stop_source': return _importlib.import_module('.inplace_stop_source', __name__)
        case 'InplaceStopSource': return _importlib.import_module('.inplace_stop_source', __name__).InplaceStopSource
        case 'inplace_stop_token': return _importlib.import_module('.inplace_stop_token', __name__)
        case 'InplaceStopToken': return _importlib.import_module('.inplace_stop_token', __name__).InplaceStopToken
        case 'into_variant': return _importlib.import_module('.into_variant', __name__)
        case 'IntoVariant': return _importlib.import_module('.into_variant', __name__).IntoVariant
        case 'just': return _importlib.import_module('.just', __name__)
        case 'Just': return _importlib.import_module('.just', __name__).Just
        case 'just_error': return _importlib.import_module('.just_error', __name__)
        case 'JustError': return _importlib.import_module('.just_error', __name__).JustError
        case 'just_stopped': return _importlib.import_module('.just_stopped', __name__)
        case 'JustStopped': return _importlib.import_module('.just_stopped', __name__).JustStopped
        case 'let_error': return _importlib.import_module('.let_error', __name__)
        case 'LetError': return _importlib.import_module('.let_error', __name__).LetError
        case 'let_stopped': return _importlib.import_module('.let_stopped', __name__)
        case 'LetStopped': return _importlib.import_module('.let_stopped', __name__).LetStopped
        case 'let_value': return _importlib.import_module('.let_value', __name__)
        case 'LetValue': return _importlib.import_module('.let_value', __name__).LetValue
        case 'never_stop_token': return _importlib.import_module('.never_stop_token', __name__)
        case 'NeverStopToken': return _importlib.import_module('.never_stop_token', __name__).NeverStopToken
        case 'operation_state': return _importlib.import_module('.operation_state', __name__)
        case 'OperationState': return _importlib.import_module('.operation_state', __name__).OperationState
        case 'prop': return _importlib.import_module('.prop', __name__)
        case 'Prop': return _importlib.import_module('.prop', __name__).Prop
        case 'read_env': return _importlib.import_module('.read_env', __name__)
        case 'ReadEnv': return _importlib.import_module('.read_env', __name__).ReadEnv
        case 'receiver': return _importlib.import_module('.receiver', __name__)
        case 'Receiver': return _importlib.import_module('.receiver', __name__).Receiver
        case 'run_loop': return _importlib.import_module('.run_loop', __name__)
        case 'RunLoop': return _importlib.import_module('.run_loop', __name__).RunLoop
        case 'schedule': return _importlib.import_module('.schedule', __name__)
        case 'Schedule': return _importlib.import_module('.schedule', __name__).Schedule
        case 'schedule_from': return _importlib.import_module('.schedule_from', __name__)
        case 'ScheduleFrom': return _importlib.import_module('.schedule_from', __name__).ScheduleFrom
        case 'scheduler': return _importlib.import_module('.scheduler', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler', __name__).Scheduler
        case 'sender': return _importlib.import_module('.sender', __name__)
        case 'Sender': return _importlib.import_module('.sender', __name__).Sender
        case 'set_error': return _importlib.import_module('.set_error', __name__)
        case 'SetError': return _importlib.import_module('.set_error', __name__).SetError
        case 'set_stopped': return _importlib.import_module('.set_stopped', __name__)
        case 'SetStopped': return _importlib.import_module('.set_stopped', __name__).SetStopped
        case 'set_value': return _importlib.import_module('.set_value', __name__)
        case 'SetValue': return _importlib.import_module('.set_value', __name__).SetValue
        case 'split': return _importlib.import_module('.split', __name__)
        case 'Split': return _importlib.import_module('.split', __name__).Split
        case 'start': return _importlib.import_module('.start', __name__)
        case 'Start': return _importlib.import_module('.start', __name__).Start
        case 'start_detached': return _importlib.import_module('.start_detached', __name__)
        case 'StartDetached': return _importlib.import_module('.start_detached', __name__).StartDetached
        case 'starts_on': return _importlib.import_module('.starts_on', __name__)
        case 'StartsOn': return _importlib.import_module('.starts_on', __name__).StartsOn
        case 'static_thread_pool': return _importlib.import_module('.static_thread_pool', __name__)
        case 'StaticThreadPool': return _importlib.import_module('.static_thread_pool', __name__).StaticThreadPool
        case 'stop_callback': return _importlib.import_module('.stop_callback', __name__)
        case 'StopCallback': return _importlib.import_module('.stop_callback', __name__).StopCallback
        case 'stop_source': return _importlib.import_module('.stop_source', __name__)
        case 'StopSource': return _importlib.import_module('.stop_source', __name__).StopSource
        case 'stop_token': return _importlib.import_module('.stop_token', __name__)
        case 'StopToken': return _importlib.import_module('.stop_token', __name__).StopToken
        case 'stopped': return _importlib.import_module('.stopped', __name__)
        case 'Stopped': return _importlib.import_module('.stopped', __name__).Stopped
        case 'stopped_as_error': return _importlib.import_module('.stopped_as_error', __name__)
        case 'StoppedAsError': return _importlib.import_module('.stopped_as_error', __name__).StoppedAsError
        case 'stopped_as_optional': return _importlib.import_module('.stopped_as_optional', __name__)
        case 'StoppedAsOptional': return _importlib.import_module('.stopped_as_optional', __name__).StoppedAsOptional
        case 'sync_wait': return _importlib.import_module('.sync_wait', __name__)
        case 'SyncWait': return _importlib.import_module('.sync_wait', __name__).SyncWait
        case 'sync_wait_with_variant': return _importlib.import_module('.sync_wait_with_variant', __name__)
        case 'SyncWaitWithVariant': return _importlib.import_module('.sync_wait_with_variant', __name__).SyncWaitWithVariant
        case 'system_context': return _importlib.import_module('.system_context', __name__)
        case 'SystemContext': return _importlib.import_module('.system_context', __name__).SystemContext
        case 'then': return _importlib.import_module('.then', __name__)
        case 'Then': return _importlib.import_module('.then', __name__).Then
        case 'transform_env': return _importlib.import_module('.transform_env', __name__)
        case 'TransformEnv': return _importlib.import_module('.transform_env', __name__).TransformEnv
        case 'transform_sender': return _importlib.import_module('.transform_sender', __name__)
        case 'TransformSender': return _importlib.import_module('.transform_sender', __name__).TransformSender
        case 'upon_error': return _importlib.import_module('.upon_error', __name__)
        case 'UponError': return _importlib.import_module('.upon_error', __name__).UponError
        case 'upon_stopped': return _importlib.import_module('.upon_stopped', __name__)
        case 'UponStopped': return _importlib.import_module('.upon_stopped', __name__).UponStopped
        case 'when_all': return _importlib.import_module('.when_all', __name__)
        case 'WhenAll': return _importlib.import_module('.when_all', __name__).WhenAll
        case 'when_all_with_variant': return _importlib.import_module('.when_all_with_variant', __name__)
        case 'WhenAllWithVariant': return _importlib.import_module('.when_all_with_variant', __name__).WhenAllWithVariant
        case 'with_awaitable_senders': return _importlib.import_module('.with_awaitable_senders', __name__)
        case 'WithAwaitableSenders': return _importlib.import_module('.with_awaitable_senders', __name__).WithAwaitableSenders
        case 'with_query_value': return _importlib.import_module('.with_query_value', __name__)
        case 'WithQueryValue': return _importlib.import_module('.with_query_value', __name__).WithQueryValue
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'apply_sender',
    'ApplySender',
    'as_awaitable',
    'AsAwaitable',
    'bulk',
    'Bulk',
    'bulk_chunked',
    'BulkChunked',
    'bulk_unchunked',
    'BulkUnchunked',
    'connect',
    'Connect',
    'continues_on',
    'ContinuesOn',
    'default_domain',
    'DefaultDomain',
    'empty_env',
    'EmptyEnv',
    'ensure_started',
    'EnsureStarted',
    'env',
    'Env',
    'forwarding_query',
    'ForwardingQuery',
    'get_allocator',
    'GetAllocator',
    'get_completion_scheduler',
    'GetCompletionScheduler',
    'get_completion_signatures',
    'GetCompletionSignatures',
    'get_delegation_scheduler',
    'GetDelegationScheduler',
    'get_domain',
    'GetDomain',
    'get_env',
    'GetEnv',
    'get_forward_progress_guarantee',
    'GetForwardProgressGuarantee',
    'get_scheduler',
    'GetScheduler',
    'get_stop_token',
    'GetStopToken',
    'inline_scheduler',
    'InlineScheduler',
    'inplace_stop_callback',
    'InplaceStopCallback',
    'inplace_stop_source',
    'InplaceStopSource',
    'inplace_stop_token',
    'InplaceStopToken',
    'into_variant',
    'IntoVariant',
    'just',
    'Just',
    'just_error',
    'JustError',
    'just_stopped',
    'JustStopped',
    'let_error',
    'LetError',
    'let_stopped',
    'LetStopped',
    'let_value',
    'LetValue',
    'never_stop_token',
    'NeverStopToken',
    'operation_state',
    'OperationState',
    'prop',
    'Prop',
    'read_env',
    'ReadEnv',
    'receiver',
    'Receiver',
    'run_loop',
    'RunLoop',
    'schedule',
    'Schedule',
    'schedule_from',
    'ScheduleFrom',
    'scheduler',
    'Scheduler',
    'sender',
    'Sender',
    'set_error',
    'SetError',
    'set_stopped',
    'SetStopped',
    'set_value',
    'SetValue',
    'split',
    'Split',
    'start',
    'Start',
    'start_detached',
    'StartDetached',
    'starts_on',
    'StartsOn',
    'static_thread_pool',
    'StaticThreadPool',
    'stop_callback',
    'StopCallback',
    'stop_source',
    'StopSource',
    'stop_token',
    'StopToken',
    'stopped',
    'Stopped',
    'stopped_as_error',
    'StoppedAsError',
    'stopped_as_optional',
    'StoppedAsOptional',
    'sync_wait',
    'SyncWait',
    'sync_wait_with_variant',
    'SyncWaitWithVariant',
    'system_context',
    'SystemContext',
    'then',
    'Then',
    'transform_env',
    'TransformEnv',
    'transform_sender',
    'TransformSender',
    'upon_error',
    'UponError',
    'upon_stopped',
    'UponStopped',
    'when_all',
    'WhenAll',
    'when_all_with_variant',
    'WhenAllWithVariant',
    'with_awaitable_senders',
    'WithAwaitableSenders',
    'with_query_value',
    'WithQueryValue',
]
