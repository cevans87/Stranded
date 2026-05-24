from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import apply_sender_
    from .apply_sender_ import ApplySender
    from . import as_awaitable_
    from .as_awaitable_ import AsAwaitable
    from . import bulk_
    from .bulk_ import Bulk
    from . import bulk_chunked_
    from .bulk_chunked_ import BulkChunked
    from . import bulk_unchunked_
    from .bulk_unchunked_ import BulkUnchunked
    from . import connect_
    from .connect_ import Connect
    from . import continues_on_
    from .continues_on_ import ContinuesOn
    from . import default_domain_
    from .default_domain_ import DefaultDomain
    from . import empty_env_
    from .empty_env_ import EmptyEnv
    from . import ensure_started_
    from .ensure_started_ import EnsureStarted
    from . import env_
    from .env_ import Env
    from . import forwarding_query_
    from .forwarding_query_ import ForwardingQuery
    from . import get_allocator_
    from .get_allocator_ import GetAllocator
    from . import get_completion_scheduler_
    from .get_completion_scheduler_ import GetCompletionScheduler
    from . import get_completion_signatures_
    from .get_completion_signatures_ import GetCompletionSignatures
    from . import get_delegation_scheduler_
    from .get_delegation_scheduler_ import GetDelegationScheduler
    from . import get_domain_
    from .get_domain_ import GetDomain
    from . import get_env_
    from .get_env_ import GetEnv
    from . import get_forward_progress_guarantee_
    from .get_forward_progress_guarantee_ import GetForwardProgressGuarantee
    from . import get_scheduler_
    from .get_scheduler_ import GetScheduler
    from . import get_stop_token_
    from .get_stop_token_ import GetStopToken
    from . import inline_scheduler_
    from .inline_scheduler_ import InlineScheduler
    from . import inplace_stop_callback_
    from .inplace_stop_callback_ import InplaceStopCallback
    from . import inplace_stop_source_
    from .inplace_stop_source_ import InplaceStopSource
    from . import inplace_stop_token_
    from .inplace_stop_token_ import InplaceStopToken
    from . import into_variant_
    from .into_variant_ import IntoVariant
    from . import just_
    from .just_ import Just
    from . import just_error_
    from .just_error_ import JustError
    from . import just_stopped_
    from .just_stopped_ import JustStopped
    from . import let_error_
    from .let_error_ import LetError
    from . import let_stopped_
    from .let_stopped_ import LetStopped
    from . import let_value_
    from .let_value_ import LetValue
    from . import never_stop_token_
    from .never_stop_token_ import NeverStopToken
    from . import operation_state_
    from .operation_state_ import OperationState
    from . import prop_
    from .prop_ import Prop
    from . import read_env_
    from .read_env_ import ReadEnv
    from . import receiver_
    from .receiver_ import Receiver
    from . import run_loop_
    from .run_loop_ import RunLoop
    from . import schedule_
    from .schedule_ import Schedule
    from . import schedule_from_
    from .schedule_from_ import ScheduleFrom
    from . import scheduler_
    from .scheduler_ import Scheduler
    from . import sender_
    from .sender_ import Sender
    from . import set_error_
    from .set_error_ import SetError
    from . import set_stopped_
    from .set_stopped_ import SetStopped
    from . import set_value_
    from .set_value_ import SetValue
    from . import split_
    from .split_ import Split
    from . import start_
    from .start_ import Start
    from . import start_detached_
    from .start_detached_ import StartDetached
    from . import starts_on_
    from .starts_on_ import StartsOn
    from . import static_thread_pool_
    from .static_thread_pool_ import StaticThreadPool
    from . import stop_callback_
    from .stop_callback_ import StopCallback
    from . import stop_source_
    from .stop_source_ import StopSource
    from . import stop_token_
    from .stop_token_ import StopToken
    from . import stopped_
    from .stopped_ import Stopped
    from . import stopped_as_error_
    from .stopped_as_error_ import StoppedAsError
    from . import stopped_as_optional_
    from .stopped_as_optional_ import StoppedAsOptional
    from . import sync_wait_
    from .sync_wait_ import SyncWait
    from . import sync_wait_with_variant_
    from .sync_wait_with_variant_ import SyncWaitWithVariant
    from . import system_context_
    from .system_context_ import SystemContext
    from . import then_
    from .then_ import Then
    from . import transform_env_
    from .transform_env_ import TransformEnv
    from . import transform_sender_
    from .transform_sender_ import TransformSender
    from . import upon_error_
    from .upon_error_ import UponError
    from . import upon_stopped_
    from .upon_stopped_ import UponStopped
    from . import when_all_
    from .when_all_ import WhenAll
    from . import when_all_with_variant_
    from .when_all_with_variant_ import WhenAllWithVariant
    from . import with_awaitable_senders_
    from .with_awaitable_senders_ import WithAwaitableSenders
    from . import with_query_value_
    from .with_query_value_ import WithQueryValue


def __getattr__(name: str) -> _typing.Any:
    match name:
        case 'apply_sender_': return _importlib.import_module('.apply_sender_', __name__)
        case 'ApplySender': return _importlib.import_module('.apply_sender_', __name__).ApplySender
        case 'as_awaitable_': return _importlib.import_module('.as_awaitable_', __name__)
        case 'AsAwaitable': return _importlib.import_module('.as_awaitable_', __name__).AsAwaitable
        case 'bulk_': return _importlib.import_module('.bulk_', __name__)
        case 'Bulk': return _importlib.import_module('.bulk_', __name__).Bulk
        case 'bulk_chunked_': return _importlib.import_module('.bulk_chunked_', __name__)
        case 'BulkChunked': return _importlib.import_module('.bulk_chunked_', __name__).BulkChunked
        case 'bulk_unchunked_': return _importlib.import_module('.bulk_unchunked_', __name__)
        case 'BulkUnchunked': return _importlib.import_module('.bulk_unchunked_', __name__).BulkUnchunked
        case 'connect_': return _importlib.import_module('.connect_', __name__)
        case 'Connect': return _importlib.import_module('.connect_', __name__).Connect
        case 'continues_on_': return _importlib.import_module('.continues_on_', __name__)
        case 'ContinuesOn': return _importlib.import_module('.continues_on_', __name__).ContinuesOn
        case 'default_domain_': return _importlib.import_module('.default_domain_', __name__)
        case 'DefaultDomain': return _importlib.import_module('.default_domain_', __name__).DefaultDomain
        case 'empty_env_': return _importlib.import_module('.empty_env_', __name__)
        case 'EmptyEnv': return _importlib.import_module('.empty_env_', __name__).EmptyEnv
        case 'ensure_started_': return _importlib.import_module('.ensure_started_', __name__)
        case 'EnsureStarted': return _importlib.import_module('.ensure_started_', __name__).EnsureStarted
        case 'env_': return _importlib.import_module('.env_', __name__)
        case 'Env': return _importlib.import_module('.env_', __name__).Env
        case 'forwarding_query_': return _importlib.import_module('.forwarding_query_', __name__)
        case 'ForwardingQuery': return _importlib.import_module('.forwarding_query_', __name__).ForwardingQuery
        case 'get_allocator_': return _importlib.import_module('.get_allocator_', __name__)
        case 'GetAllocator': return _importlib.import_module('.get_allocator_', __name__).GetAllocator
        case 'get_completion_scheduler_': return _importlib.import_module('.get_completion_scheduler_', __name__)
        case 'GetCompletionScheduler': return _importlib.import_module('.get_completion_scheduler_', __name__).GetCompletionScheduler
        case 'get_completion_signatures_': return _importlib.import_module('.get_completion_signatures_', __name__)
        case 'GetCompletionSignatures': return _importlib.import_module('.get_completion_signatures_', __name__).GetCompletionSignatures
        case 'get_delegation_scheduler_': return _importlib.import_module('.get_delegation_scheduler_', __name__)
        case 'GetDelegationScheduler': return _importlib.import_module('.get_delegation_scheduler_', __name__).GetDelegationScheduler
        case 'get_domain_': return _importlib.import_module('.get_domain_', __name__)
        case 'GetDomain': return _importlib.import_module('.get_domain_', __name__).GetDomain
        case 'get_env_': return _importlib.import_module('.get_env_', __name__)
        case 'GetEnv': return _importlib.import_module('.get_env_', __name__).GetEnv
        case 'get_forward_progress_guarantee_': return _importlib.import_module('.get_forward_progress_guarantee_', __name__)
        case 'GetForwardProgressGuarantee': return _importlib.import_module('.get_forward_progress_guarantee_', __name__).GetForwardProgressGuarantee
        case 'get_scheduler_': return _importlib.import_module('.get_scheduler_', __name__)
        case 'GetScheduler': return _importlib.import_module('.get_scheduler_', __name__).GetScheduler
        case 'get_stop_token_': return _importlib.import_module('.get_stop_token_', __name__)
        case 'GetStopToken': return _importlib.import_module('.get_stop_token_', __name__).GetStopToken
        case 'inline_scheduler_': return _importlib.import_module('.inline_scheduler_', __name__)
        case 'InlineScheduler': return _importlib.import_module('.inline_scheduler_', __name__).InlineScheduler
        case 'inplace_stop_callback_': return _importlib.import_module('.inplace_stop_callback_', __name__)
        case 'InplaceStopCallback': return _importlib.import_module('.inplace_stop_callback_', __name__).InplaceStopCallback
        case 'inplace_stop_source_': return _importlib.import_module('.inplace_stop_source_', __name__)
        case 'InplaceStopSource': return _importlib.import_module('.inplace_stop_source_', __name__).InplaceStopSource
        case 'inplace_stop_token_': return _importlib.import_module('.inplace_stop_token_', __name__)
        case 'InplaceStopToken': return _importlib.import_module('.inplace_stop_token_', __name__).InplaceStopToken
        case 'into_variant_': return _importlib.import_module('.into_variant_', __name__)
        case 'IntoVariant': return _importlib.import_module('.into_variant_', __name__).IntoVariant
        case 'just_': return _importlib.import_module('.just_', __name__)
        case 'Just': return _importlib.import_module('.just_', __name__).Just
        case 'just_error_': return _importlib.import_module('.just_error_', __name__)
        case 'JustError': return _importlib.import_module('.just_error_', __name__).JustError
        case 'just_stopped_': return _importlib.import_module('.just_stopped_', __name__)
        case 'JustStopped': return _importlib.import_module('.just_stopped_', __name__).JustStopped
        case 'let_error_': return _importlib.import_module('.let_error_', __name__)
        case 'LetError': return _importlib.import_module('.let_error_', __name__).LetError
        case 'let_stopped_': return _importlib.import_module('.let_stopped_', __name__)
        case 'LetStopped': return _importlib.import_module('.let_stopped_', __name__).LetStopped
        case 'let_value_': return _importlib.import_module('.let_value_', __name__)
        case 'LetValue': return _importlib.import_module('.let_value_', __name__).LetValue
        case 'never_stop_token_': return _importlib.import_module('.never_stop_token_', __name__)
        case 'NeverStopToken': return _importlib.import_module('.never_stop_token_', __name__).NeverStopToken
        case 'operation_state_': return _importlib.import_module('.operation_state_', __name__)
        case 'OperationState': return _importlib.import_module('.operation_state_', __name__).OperationState
        case 'prop_': return _importlib.import_module('.prop_', __name__)
        case 'Prop': return _importlib.import_module('.prop_', __name__).Prop
        case 'read_env_': return _importlib.import_module('.read_env_', __name__)
        case 'ReadEnv': return _importlib.import_module('.read_env_', __name__).ReadEnv
        case 'receiver_': return _importlib.import_module('.receiver_', __name__)
        case 'Receiver': return _importlib.import_module('.receiver_', __name__).Receiver
        case 'run_loop_': return _importlib.import_module('.run_loop_', __name__)
        case 'RunLoop': return _importlib.import_module('.run_loop_', __name__).RunLoop
        case 'schedule_': return _importlib.import_module('.schedule_', __name__)
        case 'Schedule': return _importlib.import_module('.schedule_', __name__).Schedule
        case 'schedule_from_': return _importlib.import_module('.schedule_from_', __name__)
        case 'ScheduleFrom': return _importlib.import_module('.schedule_from_', __name__).ScheduleFrom
        case 'scheduler_': return _importlib.import_module('.scheduler_', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler_', __name__).Scheduler
        case 'sender_': return _importlib.import_module('.sender_', __name__)
        case 'Sender': return _importlib.import_module('.sender_', __name__).Sender
        case 'set_error_': return _importlib.import_module('.set_error_', __name__)
        case 'SetError': return _importlib.import_module('.set_error_', __name__).SetError
        case 'set_stopped_': return _importlib.import_module('.set_stopped_', __name__)
        case 'SetStopped': return _importlib.import_module('.set_stopped_', __name__).SetStopped
        case 'set_value_': return _importlib.import_module('.set_value_', __name__)
        case 'SetValue': return _importlib.import_module('.set_value_', __name__).SetValue
        case 'split_': return _importlib.import_module('.split_', __name__)
        case 'Split': return _importlib.import_module('.split_', __name__).Split
        case 'start_': return _importlib.import_module('.start_', __name__)
        case 'Start': return _importlib.import_module('.start_', __name__).Start
        case 'start_detached_': return _importlib.import_module('.start_detached_', __name__)
        case 'StartDetached': return _importlib.import_module('.start_detached_', __name__).StartDetached
        case 'starts_on_': return _importlib.import_module('.starts_on_', __name__)
        case 'StartsOn': return _importlib.import_module('.starts_on_', __name__).StartsOn
        case 'static_thread_pool_': return _importlib.import_module('.static_thread_pool_', __name__)
        case 'StaticThreadPool': return _importlib.import_module('.static_thread_pool_', __name__).StaticThreadPool
        case 'stop_callback_': return _importlib.import_module('.stop_callback_', __name__)
        case 'StopCallback': return _importlib.import_module('.stop_callback_', __name__).StopCallback
        case 'stop_source_': return _importlib.import_module('.stop_source_', __name__)
        case 'StopSource': return _importlib.import_module('.stop_source_', __name__).StopSource
        case 'stop_token_': return _importlib.import_module('.stop_token_', __name__)
        case 'StopToken': return _importlib.import_module('.stop_token_', __name__).StopToken
        case 'stopped_': return _importlib.import_module('.stopped_', __name__)
        case 'Stopped': return _importlib.import_module('.stopped_', __name__).Stopped
        case 'stopped_as_error_': return _importlib.import_module('.stopped_as_error_', __name__)
        case 'StoppedAsError': return _importlib.import_module('.stopped_as_error_', __name__).StoppedAsError
        case 'stopped_as_optional_': return _importlib.import_module('.stopped_as_optional_', __name__)
        case 'StoppedAsOptional': return _importlib.import_module('.stopped_as_optional_', __name__).StoppedAsOptional
        case 'sync_wait_': return _importlib.import_module('.sync_wait_', __name__)
        case 'SyncWait': return _importlib.import_module('.sync_wait_', __name__).SyncWait
        case 'sync_wait_with_variant_': return _importlib.import_module('.sync_wait_with_variant_', __name__)
        case 'SyncWaitWithVariant': return _importlib.import_module('.sync_wait_with_variant_', __name__).SyncWaitWithVariant
        case 'system_context_': return _importlib.import_module('.system_context_', __name__)
        case 'SystemContext': return _importlib.import_module('.system_context_', __name__).SystemContext
        case 'then_': return _importlib.import_module('.then_', __name__)
        case 'Then': return _importlib.import_module('.then_', __name__).Then
        case 'transform_env_': return _importlib.import_module('.transform_env_', __name__)
        case 'TransformEnv': return _importlib.import_module('.transform_env_', __name__).TransformEnv
        case 'transform_sender_': return _importlib.import_module('.transform_sender_', __name__)
        case 'TransformSender': return _importlib.import_module('.transform_sender_', __name__).TransformSender
        case 'upon_error_': return _importlib.import_module('.upon_error_', __name__)
        case 'UponError': return _importlib.import_module('.upon_error_', __name__).UponError
        case 'upon_stopped_': return _importlib.import_module('.upon_stopped_', __name__)
        case 'UponStopped': return _importlib.import_module('.upon_stopped_', __name__).UponStopped
        case 'when_all_': return _importlib.import_module('.when_all_', __name__)
        case 'WhenAll': return _importlib.import_module('.when_all_', __name__).WhenAll
        case 'when_all_with_variant_': return _importlib.import_module('.when_all_with_variant_', __name__)
        case 'WhenAllWithVariant': return _importlib.import_module('.when_all_with_variant_', __name__).WhenAllWithVariant
        case 'with_awaitable_senders_': return _importlib.import_module('.with_awaitable_senders_', __name__)
        case 'WithAwaitableSenders': return _importlib.import_module('.with_awaitable_senders_', __name__).WithAwaitableSenders
        case 'with_query_value_': return _importlib.import_module('.with_query_value_', __name__)
        case 'WithQueryValue': return _importlib.import_module('.with_query_value_', __name__).WithQueryValue
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'apply_sender_',
    'ApplySender',
    'as_awaitable_',
    'AsAwaitable',
    'bulk_',
    'Bulk',
    'bulk_chunked_',
    'BulkChunked',
    'bulk_unchunked_',
    'BulkUnchunked',
    'connect_',
    'Connect',
    'continues_on_',
    'ContinuesOn',
    'default_domain_',
    'DefaultDomain',
    'empty_env_',
    'EmptyEnv',
    'ensure_started_',
    'EnsureStarted',
    'env_',
    'Env',
    'forwarding_query_',
    'ForwardingQuery',
    'get_allocator_',
    'GetAllocator',
    'get_completion_scheduler_',
    'GetCompletionScheduler',
    'get_completion_signatures_',
    'GetCompletionSignatures',
    'get_delegation_scheduler_',
    'GetDelegationScheduler',
    'get_domain_',
    'GetDomain',
    'get_env_',
    'GetEnv',
    'get_forward_progress_guarantee_',
    'GetForwardProgressGuarantee',
    'get_scheduler_',
    'GetScheduler',
    'get_stop_token_',
    'GetStopToken',
    'inline_scheduler_',
    'InlineScheduler',
    'inplace_stop_callback_',
    'InplaceStopCallback',
    'inplace_stop_source_',
    'InplaceStopSource',
    'inplace_stop_token_',
    'InplaceStopToken',
    'into_variant_',
    'IntoVariant',
    'just_',
    'Just',
    'just_error_',
    'JustError',
    'just_stopped_',
    'JustStopped',
    'let_error_',
    'LetError',
    'let_stopped_',
    'LetStopped',
    'let_value_',
    'LetValue',
    'never_stop_token_',
    'NeverStopToken',
    'operation_state_',
    'OperationState',
    'prop_',
    'Prop',
    'read_env_',
    'ReadEnv',
    'receiver_',
    'Receiver',
    'run_loop_',
    'RunLoop',
    'schedule_',
    'Schedule',
    'schedule_from_',
    'ScheduleFrom',
    'scheduler_',
    'Scheduler',
    'sender_',
    'Sender',
    'set_error_',
    'SetError',
    'set_stopped_',
    'SetStopped',
    'set_value_',
    'SetValue',
    'split_',
    'Split',
    'start_',
    'Start',
    'start_detached_',
    'StartDetached',
    'starts_on_',
    'StartsOn',
    'static_thread_pool_',
    'StaticThreadPool',
    'stop_callback_',
    'StopCallback',
    'stop_source_',
    'StopSource',
    'stop_token_',
    'StopToken',
    'stopped_',
    'Stopped',
    'stopped_as_error_',
    'StoppedAsError',
    'stopped_as_optional_',
    'StoppedAsOptional',
    'sync_wait_',
    'SyncWait',
    'sync_wait_with_variant_',
    'SyncWaitWithVariant',
    'system_context_',
    'SystemContext',
    'then_',
    'Then',
    'transform_env_',
    'TransformEnv',
    'transform_sender_',
    'TransformSender',
    'upon_error_',
    'UponError',
    'upon_stopped_',
    'UponStopped',
    'when_all_',
    'WhenAll',
    'when_all_with_variant_',
    'WhenAllWithVariant',
    'with_awaitable_senders_',
    'WithAwaitableSenders',
    'with_query_value_',
    'WithQueryValue',
)