import sys,os,json,subprocess,datetime,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
name=sys.argv[1]; arm='candidate' if name.startswith('candidate') else 'baseline'
ids=list(range(15)) if 'repeat' in name else list(range(15))+list(range(3300,3312))
for p,h in json.loads((R/(arm+'-manifest.json')).read_text()).items(): assert hashlib.sha256((R/arm/p).read_bytes()).hexdigest()==h,p
out=R/name; out.mkdir(); traces=out/'traces'; traces.mkdir()
cmd=[sys.executable,'-m','nethackers.arena.run','--solution',str(R/arm),'--batch',json.dumps([[i,'val-dwa-law-fem'] for i in ids]),'--evaluation-id','local','--secret','public','--max-steps','1000000','--no-progress-timeout','10000','--action-timeout','120','--max-parallel-evals','4','--out',str(out/'results.json')]
env=os.environ.copy(); env['PRIVATE31_TRACE_DIR']=str(traces)
meta=dict(command=cmd,environment={k:v for k,v in env.items() if k in ['PATH','PYTHONPATH','PRIVATE31_TRACE_DIR','NUMBA_CACHE_DIR','XDG_CACHE_HOME','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS']},started=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_manifest=json.loads((R/(arm+'-manifest.json')).read_text()))
(out/'command.json').write_text(json.dumps(meta,indent=2))
with (out/'stdout').open('w') as stdout,(out/'stderr').open('w') as stderr:
 result=subprocess.run(cmd,env=env,stdout=stdout,stderr=stderr)
meta.update(exit_status=result.returncode,ended=datetime.datetime.now(datetime.timezone.utc).isoformat())
(out/'command.json').write_text(json.dumps(meta,indent=2)); print(name,'exit',result.returncode,flush=True)
sys.exit(result.returncode)
