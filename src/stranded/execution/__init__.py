import importlib as _importlib
import types as _types
import typing as _typing


@_typing.overload
def __getattr__(name: _typing.Literal['apply_sender']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ApplySender']) -> 'type[stranded.execution.apply_sender.ApplySender]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['as_awaitable']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['AsAwaitable']) -> 'type[stranded.execution.as_awaitable.AsAwaitable]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Bulk']) -> 'type[stranded.execution.bulk.Bulk]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_chunked']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['BulkChunked']) -> 'type[stranded.execution.bulk_chunked.BulkChunked]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['bulk_unchunked']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['BulkUnchunked']) -> 'type[stranded.execution.bulk_unchunked.BulkUnchunked]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['connect']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Connect']) -> 'type[stranded.execution.connect.Connect]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['continues_on']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ContinuesOn']) -> 'type[stranded.execution.continues_on.ContinuesOn]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['default_domain']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['DefaultDomain']) -> 'type[stranded.execution.default_domain.DefaultDomain]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['empty_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['EmptyEnv']) -> 'type[stranded.execution.empty_env.EmptyEnv]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['ensure_started']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['EnsureStarted']) -> 'type[stranded.execution.ensure_started.EnsureStarted]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Env']) -> 'type[stranded.execution.env.Env]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['forwarding_query']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ForwardingQuery']) -> 'type[stranded.execution.forwarding_query.ForwardingQuery]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_allocator']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetAllocator']) -> 'type[stranded.execution.get_allocator.GetAllocator]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetCompletionScheduler']) -> 'type[stranded.execution.get_completion_scheduler.GetCompletionScheduler]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_completion_signatures']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetCompletionSignatures']) -> 'type[stranded.execution.get_completion_signatures.GetCompletionSignatures]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_delegation_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetDelegationScheduler']) -> 'type[stranded.execution.get_delegation_scheduler.GetDelegationScheduler]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_domain']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetDomain']) -> 'type[stranded.execution.get_domain.GetDomain]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetEnv']) -> 'type[stranded.execution.get_env.GetEnv]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_forward_progress_guarantee']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetForwardProgressGuarantee']) -> 'type[stranded.execution.get_forward_progress_guarantee.GetForwardProgressGuarantee]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetScheduler']) -> 'type[stranded.execution.get_scheduler.GetScheduler]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['get_stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['GetStopToken']) -> 'type[stranded.execution.get_stop_token.GetStopToken]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['inline_scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InlineScheduler']) -> 'type[stranded.execution.inline_scheduler.InlineScheduler]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_callback']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopCallback']) -> 'type[stranded.execution.inplace_stop_callback.InplaceStopCallback]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_source']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopSource']) -> 'type[stranded.execution.inplace_stop_source.InplaceStopSource]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['inplace_stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['InplaceStopToken']) -> 'type[stranded.execution.inplace_stop_token.InplaceStopToken]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['into_variant']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['IntoVariant']) -> 'type[stranded.execution.into_variant.IntoVariant]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['just']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Just']) -> 'type[stranded.execution.just.Just]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['JustError']) -> 'type[stranded.execution.just_error.JustError]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['just_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['JustStopped']) -> 'type[stranded.execution.just_stopped.JustStopped]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetError']) -> 'type[stranded.execution.let_error.LetError]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetStopped']) -> 'type[stranded.execution.let_stopped.LetStopped]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['let_value']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['LetValue']) -> 'type[stranded.execution.let_value.LetValue]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['never_stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['NeverStopToken']) -> 'type[stranded.execution.never_stop_token.NeverStopToken]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['operation_state']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['OperationState']) -> 'type[stranded.execution.operation_state.OperationState]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['prop']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Prop']) -> 'type[stranded.execution.prop.Prop]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['read_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ReadEnv']) -> 'type[stranded.execution.read_env.ReadEnv]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['receiver']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Receiver']) -> 'type[stranded.execution.receiver.Receiver]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['run_loop']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['RunLoop']) -> 'type[stranded.execution.run_loop.RunLoop]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Schedule']) -> 'type[stranded.execution.schedule.Schedule]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['schedule_from']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['ScheduleFrom']) -> 'type[stranded.execution.schedule_from.ScheduleFrom]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['scheduler']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Scheduler']) -> 'type[stranded.execution.scheduler.Scheduler]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['sender']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Sender']) -> 'type[stranded.execution.sender.Sender]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetError']) -> 'type[stranded.execution.set_error.SetError]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetStopped']) -> 'type[stranded.execution.set_stopped.SetStopped]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['set_value']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SetValue']) -> 'type[stranded.execution.set_value.SetValue]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['split']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Split']) -> 'type[stranded.execution.split.Split]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['start']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Start']) -> 'type[stranded.execution.start.Start]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['start_detached']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StartDetached']) -> 'type[stranded.execution.start_detached.StartDetached]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['starts_on']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StartsOn']) -> 'type[stranded.execution.starts_on.StartsOn]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['static_thread_pool']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StaticThreadPool']) -> 'type[stranded.execution.static_thread_pool.StaticThreadPool]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_callback']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopCallback']) -> 'type[stranded.execution.stop_callback.StopCallback]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_source']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopSource']) -> 'type[stranded.execution.stop_source.StopSource]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['stop_token']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StopToken']) -> 'type[stranded.execution.stop_token.StopToken]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Stopped']) -> 'type[stranded.execution.stopped.Stopped]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StoppedAsError']) -> 'type[stranded.execution.stopped_as_error.StoppedAsError]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['stopped_as_optional']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['StoppedAsOptional']) -> 'type[stranded.execution.stopped_as_optional.StoppedAsOptional]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SyncWait']) -> 'type[stranded.execution.sync_wait.SyncWait]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['sync_wait_with_variant']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SyncWaitWithVariant']) -> 'type[stranded.execution.sync_wait_with_variant.SyncWaitWithVariant]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['system_context']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['SystemContext']) -> 'type[stranded.execution.system_context.SystemContext]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['then']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['Then']) -> 'type[stranded.execution.then.Then]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_env']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['TransformEnv']) -> 'type[stranded.execution.transform_env.TransformEnv]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['transform_sender']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['TransformSender']) -> 'type[stranded.execution.transform_sender.TransformSender]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_error']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponError']) -> 'type[stranded.execution.upon_error.UponError]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['upon_stopped']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['UponStopped']) -> 'type[stranded.execution.upon_stopped.UponStopped]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WhenAll']) -> 'type[stranded.execution.when_all.WhenAll]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['when_all_with_variant']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WhenAllWithVariant']) -> 'type[stranded.execution.when_all_with_variant.WhenAllWithVariant]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_awaitable_senders']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WithAwaitableSenders']) -> 'type[stranded.execution.with_awaitable_senders.WithAwaitableSenders]': ...
@_typing.overload
def __getattr__(name: _typing.Literal['with_query_value']) -> _types.ModuleType: ...
@_typing.overload
def __getattr__(name: _typing.Literal['WithQueryValue']) -> 'type[stranded.execution.with_query_value.WithQueryValue]': ...
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
