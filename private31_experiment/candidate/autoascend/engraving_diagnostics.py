"""Passive bounded observations. No RNG, game actions, or seed access."""
import os,time,json,threading,functools
_lock=threading.RLock()
_path=None
_trace=None
_count=0
_dropped=0
_failed=0

def event(kind, agent=None, **data):
    global _count,_dropped,_failed
    if _path is None: return
    try:
        with _lock:
            if _count>=20000 and kind!='end':
                _dropped+=1; return
            if agent is not None:
                data.update(turn=int(agent.blstats.time),position=[int(agent.blstats.y),int(agent.blstats.x)],level=list(agent.current_level().key()))
            row=dict(trace=_trace,event=kind,sequence=_count,**data)
            with open(_path,'a') as f: f.write(json.dumps(row)+'\n')
            _count+=1
    except Exception: _failed+=1

def start():
    global _path,_trace,_count,_dropped,_failed
    _path=None; _count=_dropped=_failed=0
    directory=os.environ.get('PRIVATE31_TRACE_DIR')
    if not directory: return
    try:
        _trace=f'{os.getpid()}-{time.monotonic_ns()}'
        _path=os.path.join(directory,_trace+'.jsonl')
        with open(_path,'x'): pass
        event('start',association='unmapped')
    except Exception: _path=None

def end():
    event('end',dropped=_dropped,write_failures=_failed)

def attempt(fn):
    @functools.wraps(fn)
    def wrapped(agent,text):
        event('attempt',agent,requested=text[:1024],requested_length=len(text))
        try:
            result=fn(agent,text)
            event('attempt_return',agent,result=result)
            return result
        except BaseException as exc:
            event('attempt_error',agent,error=type(exc).__name__)
            raise
    return wrapped

def emit(agent,requested,payload):
    if _path is None:
        yield from payload
        return
    sent=''; completed=False
    event('emission_start',agent,requested=requested[:1024],blind=bool(agent.character.prop.blind),planned_payload=payload[:1024],payload_length=len(payload))
    try:
        for char in payload:
            sent+=char
            yield char
        completed=True
    finally:
        event('emission_end',agent,emitted_payload=sent[:1024],emitted_length=len(sent),completed=completed,interrupted=not completed,truncated=len(sent)>1024)
