from __future__ import annotations

import importlib as _importlib
import typing as _typing

if _typing.TYPE_CHECKING:
    from . import apply_sender_
    from .apply_sender_ import ApplySender
    from .apply_sender_ import apply_sender
    from . import as_awaitable_
    from .as_awaitable_ import AsAwaitable
    from .as_awaitable_ import as_awaitable
    from . import bulk_
    from .bulk_ import Bulk
    from .bulk_ import bulk
    from . import bulk_chunked_
    from .bulk_chunked_ import BulkChunked
    from .bulk_chunked_ import bulk_chunked
    from . import bulk_unchunked_
    from .bulk_unchunked_ import BulkUnchunked
    from .bulk_unchunked_ import bulk_unchunked
    from . import connect_
    from .connect_ import Connect
    from .connect_ import connect
    from . import continues_on_
    from .continues_on_ import ContinuesOn
    from .continues_on_ import continues_on
    from . import default_domain_
    from .default_domain_ import DefaultDomain
    from .default_domain_ import default_domain
    from . import empty_env_
    from .empty_env_ import EmptyEnv
    from .empty_env_ import empty_env
    from . import ensure_started_
    from .ensure_started_ import EnsureStarted
    from .ensure_started_ import ensure_started
    from . import env_
    from .env_ import Env
    from .env_ import env
    from . import forwarding_query_
    from .forwarding_query_ import ForwardingQuery
    from .forwarding_query_ import forwarding_query
    from . import get_allocator_
    from .get_allocator_ import GetAllocator
    from .get_allocator_ import get_allocator
    from . import get_completion_scheduler_
    from .get_completion_scheduler_ import GetCompletionScheduler
    from .get_completion_scheduler_ import get_completion_scheduler
    from . import get_completion_signatures_
    from .get_completion_signatures_ import GetCompletionSignatures
    from .get_completion_signatures_ import get_completion_signatures
    from . import get_delegation_scheduler_
    from .get_delegation_scheduler_ import GetDelegationScheduler
    from .get_delegation_scheduler_ import get_delegation_scheduler
    from . import get_domain_
    from .get_domain_ import GetDomain
    from .get_domain_ import get_domain
    from . import get_env_
    from .get_env_ import GetEnv
    from .get_env_ import get_env
    from . import get_forward_progress_guarantee_
    from .get_forward_progress_guarantee_ import GetForwardProgressGuarantee
    from .get_forward_progress_guarantee_ import get_forward_progress_guarantee
    from . import get_scheduler_
    from .get_scheduler_ import GetScheduler
    from .get_scheduler_ import get_scheduler
    from . import get_stop_token_
    from .get_stop_token_ import GetStopToken
    from .get_stop_token_ import get_stop_token
    from . import inline_scheduler_
    from .inline_scheduler_ import InlineScheduler
    from .inline_scheduler_ import inline_scheduler
    from . import inplace_stop_callback_
    from .inplace_stop_callback_ import InplaceStopCallback
    from .inplace_stop_callback_ import inplace_stop_callback
    from . import inplace_stop_source_
    from .inplace_stop_source_ import InplaceStopSource
    from .inplace_stop_source_ import inplace_stop_source
    from . import inplace_stop_token_
    from .inplace_stop_token_ import InplaceStopToken
    from .inplace_stop_token_ import inplace_stop_token
    from . import into_variant_
    from .into_variant_ import IntoVariant
    from .into_variant_ import into_variant
    from . import just_
    from .just_ import Just
    from .just_ import just
    from . import just_error_
    from .just_error_ import JustError
    from .just_error_ import just_error
    from . import just_stopped_
    from .just_stopped_ import JustStopped
    from .just_stopped_ import just_stopped
    from . import let_error_
    from .let_error_ import LetError
    from .let_error_ import let_error
    from . import let_stopped_
    from .let_stopped_ import LetStopped
    from .let_stopped_ import let_stopped
    from . import let_value_
    from .let_value_ import LetValue
    from .let_value_ import let_value
    from . import never_stop_token_
    from .never_stop_token_ import NeverStopToken
    from .never_stop_token_ import never_stop_token
    from . import operation_state_
    from .operation_state_ import OperationState
    from .operation_state_ import operation_state
    from . import prop_
    from .prop_ import Prop
    from .prop_ import prop
    from . import read_env_
    from .read_env_ import ReadEnv
    from .read_env_ import read_env
    from . import receiver_
    from .receiver_ import Receiver
    from .receiver_ import receiver
    from . import run_loop_
    from .run_loop_ import RunLoop
    from .run_loop_ import run_loop
    from . import schedule_
    from .schedule_ import Schedule
    from .schedule_ import schedule
    from . import schedule_from_
    from .schedule_from_ import ScheduleFrom
    from .schedule_from_ import schedule_from
    from . import scheduler_
    from .scheduler_ import Scheduler
    from .scheduler_ import scheduler
    from . import sender_
    from .sender_ import Sender
    from .sender_ import sender
    from . import set_error_
    from .set_error_ import SetError
    from .set_error_ import set_error
    from . import set_stopped_
    from .set_stopped_ import SetStopped
    from .set_stopped_ import set_stopped
    from . import set_value_
    from .set_value_ import SetValue
    from .set_value_ import set_value
    from . import split_
    from .split_ import Split
    from .split_ import split
    from . import start_
    from .start_ import Start
    from .start_ import start
    from . import start_detached_
    from .start_detached_ import StartDetached
    from .start_detached_ import start_detached
    from . import starts_on_
    from .starts_on_ import StartsOn
    from .starts_on_ import starts_on
    from . import static_thread_pool_
    from .static_thread_pool_ import StaticThreadPool
    from .static_thread_pool_ import static_thread_pool
    from . import stop_callback_
    from .stop_callback_ import StopCallback
    from .stop_callback_ import stop_callback
    from . import stop_source_
    from .stop_source_ import StopSource
    from .stop_source_ import stop_source
    from . import stop_token_
    from .stop_token_ import StopToken
    from .stop_token_ import stop_token
    from . import stopped_
    from .stopped_ import Stopped
    from .stopped_ import stopped
    from . import stopped_as_error_
    from .stopped_as_error_ import StoppedAsError
    from .stopped_as_error_ import stopped_as_error
    from . import stopped_as_optional_
    from .stopped_as_optional_ import StoppedAsOptional
    from .stopped_as_optional_ import stopped_as_optional
    from . import sync_wait_
    from .sync_wait_ import SyncWait
    from .sync_wait_ import sync_wait
    from . import sync_wait_with_variant_
    from .sync_wait_with_variant_ import SyncWaitWithVariant
    from .sync_wait_with_variant_ import sync_wait_with_variant
    from . import system_context_
    from .system_context_ import SystemContext
    from .system_context_ import system_context
    from . import then_
    from .then_ import Then
    from .then_ import then
    from . import transform_env_
    from .transform_env_ import TransformEnv
    from .transform_env_ import transform_env
    from . import transform_sender_
    from .transform_sender_ import TransformSender
    from .transform_sender_ import transform_sender
    from . import upon_error_
    from .upon_error_ import UponError
    from .upon_error_ import upon_error
    from . import upon_stopped_
    from .upon_stopped_ import UponStopped
    from .upon_stopped_ import upon_stopped
    from . import when_all_
    from .when_all_ import WhenAll
    from .when_all_ import when_all
    from . import when_all_with_variant_
    from .when_all_with_variant_ import WhenAllWithVariant
    from .when_all_with_variant_ import when_all_with_variant
    from . import with_awaitable_senders_
    from .with_awaitable_senders_ import WithAwaitableSenders
    from .with_awaitable_senders_ import with_awaitable_senders
    from . import with_query_value_
    from .with_query_value_ import WithQueryValue
    from .with_query_value_ import with_query_value


@_typing.overload
def __getattr__(name: _typing.Literal['apply_sender_']) -> type[apply_sender_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ApplySender']) -> type[ApplySender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['apply_sender']) -> type[apply_sender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['as_awaitable_']) -> type[as_awaitable_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['AsAwaitable']) -> type[AsAwaitable]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['as_awaitable']) -> type[as_awaitable]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_']) -> type[bulk_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Bulk']) -> type[Bulk]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk']) -> type[bulk]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_chunked_']) -> type[bulk_chunked_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['BulkChunked']) -> type[BulkChunked]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_chunked']) -> type[bulk_chunked]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_unchunked_']) -> type[bulk_unchunked_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['BulkUnchunked']) -> type[BulkUnchunked]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_unchunked']) -> type[bulk_unchunked]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['connect_']) -> type[connect_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Connect']) -> type[Connect]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['connect']) -> type[connect]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['continues_on_']) -> type[continues_on_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ContinuesOn']) -> type[ContinuesOn]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['continues_on']) -> type[continues_on]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['default_domain_']) -> type[default_domain_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['DefaultDomain']) -> type[DefaultDomain]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['default_domain']) -> type[default_domain]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['empty_env_']) -> type[empty_env_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['EmptyEnv']) -> type[EmptyEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['empty_env']) -> type[empty_env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ensure_started_']) -> type[ensure_started_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['EnsureStarted']) -> type[EnsureStarted]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ensure_started']) -> type[ensure_started]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['env_']) -> type[env_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Env']) -> type[Env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['env']) -> type[env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['forwarding_query_']) -> type[forwarding_query_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ForwardingQuery']) -> type[ForwardingQuery]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['forwarding_query']) -> type[forwarding_query]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_allocator_']) -> type[get_allocator_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetAllocator']) -> type[GetAllocator]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_allocator']) -> type[get_allocator]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_scheduler_']) -> type[get_completion_scheduler_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetCompletionScheduler']) -> type[GetCompletionScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_scheduler']) -> type[get_completion_scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_signatures_']) -> type[get_completion_signatures_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetCompletionSignatures']) -> type[GetCompletionSignatures]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_signatures']) -> type[get_completion_signatures]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_delegation_scheduler_']) -> type[get_delegation_scheduler_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetDelegationScheduler']) -> type[GetDelegationScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_delegation_scheduler']) -> type[get_delegation_scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_domain_']) -> type[get_domain_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetDomain']) -> type[GetDomain]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_domain']) -> type[get_domain]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_env_']) -> type[get_env_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetEnv']) -> type[GetEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_env']) -> type[get_env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_forward_progress_guarantee_']) -> type[get_forward_progress_guarantee_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetForwardProgressGuarantee']) -> type[GetForwardProgressGuarantee]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_forward_progress_guarantee']) -> type[get_forward_progress_guarantee]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_scheduler_']) -> type[get_scheduler_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetScheduler']) -> type[GetScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_scheduler']) -> type[get_scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_stop_token_']) -> type[get_stop_token_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetStopToken']) -> type[GetStopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_stop_token']) -> type[get_stop_token]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inline_scheduler_']) -> type[inline_scheduler_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InlineScheduler']) -> type[InlineScheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inline_scheduler']) -> type[inline_scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_callback_']) -> type[inplace_stop_callback_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopCallback']) -> type[InplaceStopCallback]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_callback']) -> type[inplace_stop_callback]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_source_']) -> type[inplace_stop_source_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopSource']) -> type[InplaceStopSource]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_source']) -> type[inplace_stop_source]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_token_']) -> type[inplace_stop_token_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopToken']) -> type[InplaceStopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_token']) -> type[inplace_stop_token]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['into_variant_']) -> type[into_variant_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['IntoVariant']) -> type[IntoVariant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['into_variant']) -> type[into_variant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_']) -> type[just_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Just']) -> type[Just]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just']) -> type[just]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_error_']) -> type[just_error_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['JustError']) -> type[JustError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_error']) -> type[just_error]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_stopped_']) -> type[just_stopped_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['JustStopped']) -> type[JustStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_stopped']) -> type[just_stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_error_']) -> type[let_error_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetError']) -> type[LetError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_error']) -> type[let_error]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_stopped_']) -> type[let_stopped_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetStopped']) -> type[LetStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_stopped']) -> type[let_stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_value_']) -> type[let_value_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetValue']) -> type[LetValue]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_value']) -> type[let_value]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['never_stop_token_']) -> type[never_stop_token_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['NeverStopToken']) -> type[NeverStopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['never_stop_token']) -> type[never_stop_token]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['operation_state_']) -> type[operation_state_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['OperationState']) -> type[OperationState]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['operation_state']) -> type[operation_state]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['prop_']) -> type[prop_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Prop']) -> type[Prop]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['prop']) -> type[prop]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['read_env_']) -> type[read_env_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ReadEnv']) -> type[ReadEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['read_env']) -> type[read_env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['receiver_']) -> type[receiver_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Receiver']) -> type[Receiver]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['receiver']) -> type[receiver]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['run_loop_']) -> type[run_loop_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['RunLoop']) -> type[RunLoop]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['run_loop']) -> type[run_loop]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule_']) -> type[schedule_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Schedule']) -> type[Schedule]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule']) -> type[schedule]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule_from_']) -> type[schedule_from_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ScheduleFrom']) -> type[ScheduleFrom]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule_from']) -> type[schedule_from]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['scheduler_']) -> type[scheduler_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Scheduler']) -> type[Scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['scheduler']) -> type[scheduler]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sender_']) -> type[sender_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Sender']) -> type[Sender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sender']) -> type[sender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_error_']) -> type[set_error_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetError']) -> type[SetError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_error']) -> type[set_error]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_stopped_']) -> type[set_stopped_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetStopped']) -> type[SetStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_stopped']) -> type[set_stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_value_']) -> type[set_value_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetValue']) -> type[SetValue]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_value']) -> type[set_value]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['split_']) -> type[split_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Split']) -> type[Split]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['split']) -> type[split]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['start_']) -> type[start_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Start']) -> type[Start]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['start']) -> type[start]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['start_detached_']) -> type[start_detached_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StartDetached']) -> type[StartDetached]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['start_detached']) -> type[start_detached]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['starts_on_']) -> type[starts_on_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StartsOn']) -> type[StartsOn]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['starts_on']) -> type[starts_on]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['static_thread_pool_']) -> type[static_thread_pool_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StaticThreadPool']) -> type[StaticThreadPool]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['static_thread_pool']) -> type[static_thread_pool]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_callback_']) -> type[stop_callback_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopCallback']) -> type[StopCallback]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_callback']) -> type[stop_callback]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_source_']) -> type[stop_source_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopSource']) -> type[StopSource]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_source']) -> type[stop_source]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_token_']) -> type[stop_token_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopToken']) -> type[StopToken]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_token']) -> type[stop_token]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_']) -> type[stopped_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Stopped']) -> type[Stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped']) -> type[stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_error_']) -> type[stopped_as_error_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StoppedAsError']) -> type[StoppedAsError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_error']) -> type[stopped_as_error]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_optional_']) -> type[stopped_as_optional_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StoppedAsOptional']) -> type[StoppedAsOptional]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_optional']) -> type[stopped_as_optional]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait_']) -> type[sync_wait_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SyncWait']) -> type[SyncWait]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait']) -> type[sync_wait]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait_with_variant_']) -> type[sync_wait_with_variant_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SyncWaitWithVariant']) -> type[SyncWaitWithVariant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait_with_variant']) -> type[sync_wait_with_variant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['system_context_']) -> type[system_context_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SystemContext']) -> type[SystemContext]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['system_context']) -> type[system_context]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['then_']) -> type[then_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Then']) -> type[Then]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['then']) -> type[then]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_env_']) -> type[transform_env_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['TransformEnv']) -> type[TransformEnv]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_env']) -> type[transform_env]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_sender_']) -> type[transform_sender_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['TransformSender']) -> type[TransformSender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_sender']) -> type[transform_sender]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_error_']) -> type[upon_error_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponError']) -> type[UponError]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_error']) -> type[upon_error]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_stopped_']) -> type[upon_stopped_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponStopped']) -> type[UponStopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_stopped']) -> type[upon_stopped]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all_']) -> type[when_all_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WhenAll']) -> type[WhenAll]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all']) -> type[when_all]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all_with_variant_']) -> type[when_all_with_variant_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WhenAllWithVariant']) -> type[WhenAllWithVariant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all_with_variant']) -> type[when_all_with_variant]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_awaitable_senders_']) -> type[with_awaitable_senders_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WithAwaitableSenders']) -> type[WithAwaitableSenders]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_awaitable_senders']) -> type[with_awaitable_senders]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_query_value_']) -> type[with_query_value_]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WithQueryValue']) -> type[WithQueryValue]: ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_query_value']) -> type[with_query_value]: ...
def __getattr__(name):
    match name:
        case 'apply_sender_': return _importlib.import_module('.apply_sender_', __name__)
        case 'ApplySender': return _importlib.import_module('.apply_sender_', __name__).ApplySender
        case 'apply_sender': return _importlib.import_module('.apply_sender_', __name__).apply_sender
        case 'as_awaitable_': return _importlib.import_module('.as_awaitable_', __name__)
        case 'AsAwaitable': return _importlib.import_module('.as_awaitable_', __name__).AsAwaitable
        case 'as_awaitable': return _importlib.import_module('.as_awaitable_', __name__).as_awaitable
        case 'bulk_': return _importlib.import_module('.bulk_', __name__)
        case 'Bulk': return _importlib.import_module('.bulk_', __name__).Bulk
        case 'bulk': return _importlib.import_module('.bulk_', __name__).bulk
        case 'bulk_chunked_': return _importlib.import_module('.bulk_chunked_', __name__)
        case 'BulkChunked': return _importlib.import_module('.bulk_chunked_', __name__).BulkChunked
        case 'bulk_chunked': return _importlib.import_module('.bulk_chunked_', __name__).bulk_chunked
        case 'bulk_unchunked_': return _importlib.import_module('.bulk_unchunked_', __name__)
        case 'BulkUnchunked': return _importlib.import_module('.bulk_unchunked_', __name__).BulkUnchunked
        case 'bulk_unchunked': return _importlib.import_module('.bulk_unchunked_', __name__).bulk_unchunked
        case 'connect_': return _importlib.import_module('.connect_', __name__)
        case 'Connect': return _importlib.import_module('.connect_', __name__).Connect
        case 'connect': return _importlib.import_module('.connect_', __name__).connect
        case 'continues_on_': return _importlib.import_module('.continues_on_', __name__)
        case 'ContinuesOn': return _importlib.import_module('.continues_on_', __name__).ContinuesOn
        case 'continues_on': return _importlib.import_module('.continues_on_', __name__).continues_on
        case 'default_domain_': return _importlib.import_module('.default_domain_', __name__)
        case 'DefaultDomain': return _importlib.import_module('.default_domain_', __name__).DefaultDomain
        case 'default_domain': return _importlib.import_module('.default_domain_', __name__).default_domain
        case 'empty_env_': return _importlib.import_module('.empty_env_', __name__)
        case 'EmptyEnv': return _importlib.import_module('.empty_env_', __name__).EmptyEnv
        case 'empty_env': return _importlib.import_module('.empty_env_', __name__).empty_env
        case 'ensure_started_': return _importlib.import_module('.ensure_started_', __name__)
        case 'EnsureStarted': return _importlib.import_module('.ensure_started_', __name__).EnsureStarted
        case 'ensure_started': return _importlib.import_module('.ensure_started_', __name__).ensure_started
        case 'env_': return _importlib.import_module('.env_', __name__)
        case 'Env': return _importlib.import_module('.env_', __name__).Env
        case 'env': return _importlib.import_module('.env_', __name__).env
        case 'forwarding_query_': return _importlib.import_module('.forwarding_query_', __name__)
        case 'ForwardingQuery': return _importlib.import_module('.forwarding_query_', __name__).ForwardingQuery
        case 'forwarding_query': return _importlib.import_module('.forwarding_query_', __name__).forwarding_query
        case 'get_allocator_': return _importlib.import_module('.get_allocator_', __name__)
        case 'GetAllocator': return _importlib.import_module('.get_allocator_', __name__).GetAllocator
        case 'get_allocator': return _importlib.import_module('.get_allocator_', __name__).get_allocator
        case 'get_completion_scheduler_': return _importlib.import_module('.get_completion_scheduler_', __name__)
        case 'GetCompletionScheduler': return _importlib.import_module('.get_completion_scheduler_', __name__).GetCompletionScheduler
        case 'get_completion_scheduler': return _importlib.import_module('.get_completion_scheduler_', __name__).get_completion_scheduler
        case 'get_completion_signatures_': return _importlib.import_module('.get_completion_signatures_', __name__)
        case 'GetCompletionSignatures': return _importlib.import_module('.get_completion_signatures_', __name__).GetCompletionSignatures
        case 'get_completion_signatures': return _importlib.import_module('.get_completion_signatures_', __name__).get_completion_signatures
        case 'get_delegation_scheduler_': return _importlib.import_module('.get_delegation_scheduler_', __name__)
        case 'GetDelegationScheduler': return _importlib.import_module('.get_delegation_scheduler_', __name__).GetDelegationScheduler
        case 'get_delegation_scheduler': return _importlib.import_module('.get_delegation_scheduler_', __name__).get_delegation_scheduler
        case 'get_domain_': return _importlib.import_module('.get_domain_', __name__)
        case 'GetDomain': return _importlib.import_module('.get_domain_', __name__).GetDomain
        case 'get_domain': return _importlib.import_module('.get_domain_', __name__).get_domain
        case 'get_env_': return _importlib.import_module('.get_env_', __name__)
        case 'GetEnv': return _importlib.import_module('.get_env_', __name__).GetEnv
        case 'get_env': return _importlib.import_module('.get_env_', __name__).get_env
        case 'get_forward_progress_guarantee_': return _importlib.import_module('.get_forward_progress_guarantee_', __name__)
        case 'GetForwardProgressGuarantee': return _importlib.import_module('.get_forward_progress_guarantee_', __name__).GetForwardProgressGuarantee
        case 'get_forward_progress_guarantee': return _importlib.import_module('.get_forward_progress_guarantee_', __name__).get_forward_progress_guarantee
        case 'get_scheduler_': return _importlib.import_module('.get_scheduler_', __name__)
        case 'GetScheduler': return _importlib.import_module('.get_scheduler_', __name__).GetScheduler
        case 'get_scheduler': return _importlib.import_module('.get_scheduler_', __name__).get_scheduler
        case 'get_stop_token_': return _importlib.import_module('.get_stop_token_', __name__)
        case 'GetStopToken': return _importlib.import_module('.get_stop_token_', __name__).GetStopToken
        case 'get_stop_token': return _importlib.import_module('.get_stop_token_', __name__).get_stop_token
        case 'inline_scheduler_': return _importlib.import_module('.inline_scheduler_', __name__)
        case 'InlineScheduler': return _importlib.import_module('.inline_scheduler_', __name__).InlineScheduler
        case 'inline_scheduler': return _importlib.import_module('.inline_scheduler_', __name__).inline_scheduler
        case 'inplace_stop_callback_': return _importlib.import_module('.inplace_stop_callback_', __name__)
        case 'InplaceStopCallback': return _importlib.import_module('.inplace_stop_callback_', __name__).InplaceStopCallback
        case 'inplace_stop_callback': return _importlib.import_module('.inplace_stop_callback_', __name__).inplace_stop_callback
        case 'inplace_stop_source_': return _importlib.import_module('.inplace_stop_source_', __name__)
        case 'InplaceStopSource': return _importlib.import_module('.inplace_stop_source_', __name__).InplaceStopSource
        case 'inplace_stop_source': return _importlib.import_module('.inplace_stop_source_', __name__).inplace_stop_source
        case 'inplace_stop_token_': return _importlib.import_module('.inplace_stop_token_', __name__)
        case 'InplaceStopToken': return _importlib.import_module('.inplace_stop_token_', __name__).InplaceStopToken
        case 'inplace_stop_token': return _importlib.import_module('.inplace_stop_token_', __name__).inplace_stop_token
        case 'into_variant_': return _importlib.import_module('.into_variant_', __name__)
        case 'IntoVariant': return _importlib.import_module('.into_variant_', __name__).IntoVariant
        case 'into_variant': return _importlib.import_module('.into_variant_', __name__).into_variant
        case 'just_': return _importlib.import_module('.just_', __name__)
        case 'Just': return _importlib.import_module('.just_', __name__).Just
        case 'just': return _importlib.import_module('.just_', __name__).just
        case 'just_error_': return _importlib.import_module('.just_error_', __name__)
        case 'JustError': return _importlib.import_module('.just_error_', __name__).JustError
        case 'just_error': return _importlib.import_module('.just_error_', __name__).just_error
        case 'just_stopped_': return _importlib.import_module('.just_stopped_', __name__)
        case 'JustStopped': return _importlib.import_module('.just_stopped_', __name__).JustStopped
        case 'just_stopped': return _importlib.import_module('.just_stopped_', __name__).just_stopped
        case 'let_error_': return _importlib.import_module('.let_error_', __name__)
        case 'LetError': return _importlib.import_module('.let_error_', __name__).LetError
        case 'let_error': return _importlib.import_module('.let_error_', __name__).let_error
        case 'let_stopped_': return _importlib.import_module('.let_stopped_', __name__)
        case 'LetStopped': return _importlib.import_module('.let_stopped_', __name__).LetStopped
        case 'let_stopped': return _importlib.import_module('.let_stopped_', __name__).let_stopped
        case 'let_value_': return _importlib.import_module('.let_value_', __name__)
        case 'LetValue': return _importlib.import_module('.let_value_', __name__).LetValue
        case 'let_value': return _importlib.import_module('.let_value_', __name__).let_value
        case 'never_stop_token_': return _importlib.import_module('.never_stop_token_', __name__)
        case 'NeverStopToken': return _importlib.import_module('.never_stop_token_', __name__).NeverStopToken
        case 'never_stop_token': return _importlib.import_module('.never_stop_token_', __name__).never_stop_token
        case 'operation_state_': return _importlib.import_module('.operation_state_', __name__)
        case 'OperationState': return _importlib.import_module('.operation_state_', __name__).OperationState
        case 'operation_state': return _importlib.import_module('.operation_state_', __name__).operation_state
        case 'prop_': return _importlib.import_module('.prop_', __name__)
        case 'Prop': return _importlib.import_module('.prop_', __name__).Prop
        case 'prop': return _importlib.import_module('.prop_', __name__).prop
        case 'read_env_': return _importlib.import_module('.read_env_', __name__)
        case 'ReadEnv': return _importlib.import_module('.read_env_', __name__).ReadEnv
        case 'read_env': return _importlib.import_module('.read_env_', __name__).read_env
        case 'receiver_': return _importlib.import_module('.receiver_', __name__)
        case 'Receiver': return _importlib.import_module('.receiver_', __name__).Receiver
        case 'receiver': return _importlib.import_module('.receiver_', __name__).receiver
        case 'run_loop_': return _importlib.import_module('.run_loop_', __name__)
        case 'RunLoop': return _importlib.import_module('.run_loop_', __name__).RunLoop
        case 'run_loop': return _importlib.import_module('.run_loop_', __name__).run_loop
        case 'schedule_': return _importlib.import_module('.schedule_', __name__)
        case 'Schedule': return _importlib.import_module('.schedule_', __name__).Schedule
        case 'schedule': return _importlib.import_module('.schedule_', __name__).schedule
        case 'schedule_from_': return _importlib.import_module('.schedule_from_', __name__)
        case 'ScheduleFrom': return _importlib.import_module('.schedule_from_', __name__).ScheduleFrom
        case 'schedule_from': return _importlib.import_module('.schedule_from_', __name__).schedule_from
        case 'scheduler_': return _importlib.import_module('.scheduler_', __name__)
        case 'Scheduler': return _importlib.import_module('.scheduler_', __name__).Scheduler
        case 'scheduler': return _importlib.import_module('.scheduler_', __name__).scheduler
        case 'sender_': return _importlib.import_module('.sender_', __name__)
        case 'Sender': return _importlib.import_module('.sender_', __name__).Sender
        case 'sender': return _importlib.import_module('.sender_', __name__).sender
        case 'set_error_': return _importlib.import_module('.set_error_', __name__)
        case 'SetError': return _importlib.import_module('.set_error_', __name__).SetError
        case 'set_error': return _importlib.import_module('.set_error_', __name__).set_error
        case 'set_stopped_': return _importlib.import_module('.set_stopped_', __name__)
        case 'SetStopped': return _importlib.import_module('.set_stopped_', __name__).SetStopped
        case 'set_stopped': return _importlib.import_module('.set_stopped_', __name__).set_stopped
        case 'set_value_': return _importlib.import_module('.set_value_', __name__)
        case 'SetValue': return _importlib.import_module('.set_value_', __name__).SetValue
        case 'set_value': return _importlib.import_module('.set_value_', __name__).set_value
        case 'split_': return _importlib.import_module('.split_', __name__)
        case 'Split': return _importlib.import_module('.split_', __name__).Split
        case 'split': return _importlib.import_module('.split_', __name__).split
        case 'start_': return _importlib.import_module('.start_', __name__)
        case 'Start': return _importlib.import_module('.start_', __name__).Start
        case 'start': return _importlib.import_module('.start_', __name__).start
        case 'start_detached_': return _importlib.import_module('.start_detached_', __name__)
        case 'StartDetached': return _importlib.import_module('.start_detached_', __name__).StartDetached
        case 'start_detached': return _importlib.import_module('.start_detached_', __name__).start_detached
        case 'starts_on_': return _importlib.import_module('.starts_on_', __name__)
        case 'StartsOn': return _importlib.import_module('.starts_on_', __name__).StartsOn
        case 'starts_on': return _importlib.import_module('.starts_on_', __name__).starts_on
        case 'static_thread_pool_': return _importlib.import_module('.static_thread_pool_', __name__)
        case 'StaticThreadPool': return _importlib.import_module('.static_thread_pool_', __name__).StaticThreadPool
        case 'static_thread_pool': return _importlib.import_module('.static_thread_pool_', __name__).static_thread_pool
        case 'stop_callback_': return _importlib.import_module('.stop_callback_', __name__)
        case 'StopCallback': return _importlib.import_module('.stop_callback_', __name__).StopCallback
        case 'stop_callback': return _importlib.import_module('.stop_callback_', __name__).stop_callback
        case 'stop_source_': return _importlib.import_module('.stop_source_', __name__)
        case 'StopSource': return _importlib.import_module('.stop_source_', __name__).StopSource
        case 'stop_source': return _importlib.import_module('.stop_source_', __name__).stop_source
        case 'stop_token_': return _importlib.import_module('.stop_token_', __name__)
        case 'StopToken': return _importlib.import_module('.stop_token_', __name__).StopToken
        case 'stop_token': return _importlib.import_module('.stop_token_', __name__).stop_token
        case 'stopped_': return _importlib.import_module('.stopped_', __name__)
        case 'Stopped': return _importlib.import_module('.stopped_', __name__).Stopped
        case 'stopped': return _importlib.import_module('.stopped_', __name__).stopped
        case 'stopped_as_error_': return _importlib.import_module('.stopped_as_error_', __name__)
        case 'StoppedAsError': return _importlib.import_module('.stopped_as_error_', __name__).StoppedAsError
        case 'stopped_as_error': return _importlib.import_module('.stopped_as_error_', __name__).stopped_as_error
        case 'stopped_as_optional_': return _importlib.import_module('.stopped_as_optional_', __name__)
        case 'StoppedAsOptional': return _importlib.import_module('.stopped_as_optional_', __name__).StoppedAsOptional
        case 'stopped_as_optional': return _importlib.import_module('.stopped_as_optional_', __name__).stopped_as_optional
        case 'sync_wait_': return _importlib.import_module('.sync_wait_', __name__)
        case 'SyncWait': return _importlib.import_module('.sync_wait_', __name__).SyncWait
        case 'sync_wait': return _importlib.import_module('.sync_wait_', __name__).sync_wait
        case 'sync_wait_with_variant_': return _importlib.import_module('.sync_wait_with_variant_', __name__)
        case 'SyncWaitWithVariant': return _importlib.import_module('.sync_wait_with_variant_', __name__).SyncWaitWithVariant
        case 'sync_wait_with_variant': return _importlib.import_module('.sync_wait_with_variant_', __name__).sync_wait_with_variant
        case 'system_context_': return _importlib.import_module('.system_context_', __name__)
        case 'SystemContext': return _importlib.import_module('.system_context_', __name__).SystemContext
        case 'system_context': return _importlib.import_module('.system_context_', __name__).system_context
        case 'then_': return _importlib.import_module('.then_', __name__)
        case 'Then': return _importlib.import_module('.then_', __name__).Then
        case 'then': return _importlib.import_module('.then_', __name__).then
        case 'transform_env_': return _importlib.import_module('.transform_env_', __name__)
        case 'TransformEnv': return _importlib.import_module('.transform_env_', __name__).TransformEnv
        case 'transform_env': return _importlib.import_module('.transform_env_', __name__).transform_env
        case 'transform_sender_': return _importlib.import_module('.transform_sender_', __name__)
        case 'TransformSender': return _importlib.import_module('.transform_sender_', __name__).TransformSender
        case 'transform_sender': return _importlib.import_module('.transform_sender_', __name__).transform_sender
        case 'upon_error_': return _importlib.import_module('.upon_error_', __name__)
        case 'UponError': return _importlib.import_module('.upon_error_', __name__).UponError
        case 'upon_error': return _importlib.import_module('.upon_error_', __name__).upon_error
        case 'upon_stopped_': return _importlib.import_module('.upon_stopped_', __name__)
        case 'UponStopped': return _importlib.import_module('.upon_stopped_', __name__).UponStopped
        case 'upon_stopped': return _importlib.import_module('.upon_stopped_', __name__).upon_stopped
        case 'when_all_': return _importlib.import_module('.when_all_', __name__)
        case 'WhenAll': return _importlib.import_module('.when_all_', __name__).WhenAll
        case 'when_all': return _importlib.import_module('.when_all_', __name__).when_all
        case 'when_all_with_variant_': return _importlib.import_module('.when_all_with_variant_', __name__)
        case 'WhenAllWithVariant': return _importlib.import_module('.when_all_with_variant_', __name__).WhenAllWithVariant
        case 'when_all_with_variant': return _importlib.import_module('.when_all_with_variant_', __name__).when_all_with_variant
        case 'with_awaitable_senders_': return _importlib.import_module('.with_awaitable_senders_', __name__)
        case 'WithAwaitableSenders': return _importlib.import_module('.with_awaitable_senders_', __name__).WithAwaitableSenders
        case 'with_awaitable_senders': return _importlib.import_module('.with_awaitable_senders_', __name__).with_awaitable_senders
        case 'with_query_value_': return _importlib.import_module('.with_query_value_', __name__)
        case 'WithQueryValue': return _importlib.import_module('.with_query_value_', __name__).WithQueryValue
        case 'with_query_value': return _importlib.import_module('.with_query_value_', __name__).with_query_value
        case _: raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = (
    'apply_sender_',
    'ApplySender',
    'apply_sender',
    'as_awaitable_',
    'AsAwaitable',
    'as_awaitable',
    'bulk_',
    'Bulk',
    'bulk',
    'bulk_chunked_',
    'BulkChunked',
    'bulk_chunked',
    'bulk_unchunked_',
    'BulkUnchunked',
    'bulk_unchunked',
    'connect_',
    'Connect',
    'connect',
    'continues_on_',
    'ContinuesOn',
    'continues_on',
    'default_domain_',
    'DefaultDomain',
    'default_domain',
    'empty_env_',
    'EmptyEnv',
    'empty_env',
    'ensure_started_',
    'EnsureStarted',
    'ensure_started',
    'env_',
    'Env',
    'env',
    'forwarding_query_',
    'ForwardingQuery',
    'forwarding_query',
    'get_allocator_',
    'GetAllocator',
    'get_allocator',
    'get_completion_scheduler_',
    'GetCompletionScheduler',
    'get_completion_scheduler',
    'get_completion_signatures_',
    'GetCompletionSignatures',
    'get_completion_signatures',
    'get_delegation_scheduler_',
    'GetDelegationScheduler',
    'get_delegation_scheduler',
    'get_domain_',
    'GetDomain',
    'get_domain',
    'get_env_',
    'GetEnv',
    'get_env',
    'get_forward_progress_guarantee_',
    'GetForwardProgressGuarantee',
    'get_forward_progress_guarantee',
    'get_scheduler_',
    'GetScheduler',
    'get_scheduler',
    'get_stop_token_',
    'GetStopToken',
    'get_stop_token',
    'inline_scheduler_',
    'InlineScheduler',
    'inline_scheduler',
    'inplace_stop_callback_',
    'InplaceStopCallback',
    'inplace_stop_callback',
    'inplace_stop_source_',
    'InplaceStopSource',
    'inplace_stop_source',
    'inplace_stop_token_',
    'InplaceStopToken',
    'inplace_stop_token',
    'into_variant_',
    'IntoVariant',
    'into_variant',
    'just_',
    'Just',
    'just',
    'just_error_',
    'JustError',
    'just_error',
    'just_stopped_',
    'JustStopped',
    'just_stopped',
    'let_error_',
    'LetError',
    'let_error',
    'let_stopped_',
    'LetStopped',
    'let_stopped',
    'let_value_',
    'LetValue',
    'let_value',
    'never_stop_token_',
    'NeverStopToken',
    'never_stop_token',
    'operation_state_',
    'OperationState',
    'operation_state',
    'prop_',
    'Prop',
    'prop',
    'read_env_',
    'ReadEnv',
    'read_env',
    'receiver_',
    'Receiver',
    'receiver',
    'run_loop_',
    'RunLoop',
    'run_loop',
    'schedule_',
    'Schedule',
    'schedule',
    'schedule_from_',
    'ScheduleFrom',
    'schedule_from',
    'scheduler_',
    'Scheduler',
    'scheduler',
    'sender_',
    'Sender',
    'sender',
    'set_error_',
    'SetError',
    'set_error',
    'set_stopped_',
    'SetStopped',
    'set_stopped',
    'set_value_',
    'SetValue',
    'set_value',
    'split_',
    'Split',
    'split',
    'start_',
    'Start',
    'start',
    'start_detached_',
    'StartDetached',
    'start_detached',
    'starts_on_',
    'StartsOn',
    'starts_on',
    'static_thread_pool_',
    'StaticThreadPool',
    'static_thread_pool',
    'stop_callback_',
    'StopCallback',
    'stop_callback',
    'stop_source_',
    'StopSource',
    'stop_source',
    'stop_token_',
    'StopToken',
    'stop_token',
    'stopped_',
    'Stopped',
    'stopped',
    'stopped_as_error_',
    'StoppedAsError',
    'stopped_as_error',
    'stopped_as_optional_',
    'StoppedAsOptional',
    'stopped_as_optional',
    'sync_wait_',
    'SyncWait',
    'sync_wait',
    'sync_wait_with_variant_',
    'SyncWaitWithVariant',
    'sync_wait_with_variant',
    'system_context_',
    'SystemContext',
    'system_context',
    'then_',
    'Then',
    'then',
    'transform_env_',
    'TransformEnv',
    'transform_env',
    'transform_sender_',
    'TransformSender',
    'transform_sender',
    'upon_error_',
    'UponError',
    'upon_error',
    'upon_stopped_',
    'UponStopped',
    'upon_stopped',
    'when_all_',
    'WhenAll',
    'when_all',
    'when_all_with_variant_',
    'WhenAllWithVariant',
    'when_all_with_variant',
    'with_awaitable_senders_',
    'WithAwaitableSenders',
    'with_awaitable_senders',
    'with_query_value_',
    'WithQueryValue',
    'with_query_value',
)