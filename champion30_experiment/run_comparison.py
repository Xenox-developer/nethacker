"""Foreground sequential native arena batches; never reruns an episode."""
import os,sys,json,subprocess,datetime
from pathlib import Path
E=Path(__file__).resolve().parent
f=json.loads((E/'freeze.json').read_text())
for arm in ('baseline','hybrid'):
 env=os.environ.copy();env.pop('NETHACK_ARENA_SECRET',None)
 env['CHAMPION30_DIAGNOSTICS']='1';env['CHAMPION30_DIAGNOSTICS_DIR']=str(E/'diagnostics'/arm)
 cmd=[sys.executable,'-m','nethackers.arena.run','--solution',str(E/arm),'--batch',json.dumps(f['batch']),'--evaluation-id','local','--secret','public','--max-steps','1000000','--no-progress-timeout','10000','--action-timeout','120','--max-parallel-evals','4','--out',str(E/(arm+'-raw.json'))]
 (E/(arm+'-command.json')).write_text(json.dumps({'argv':cmd,'diagnostics_env':{k:v for k,v in env.items() if k.startswith('CHAMPION30_')},'started':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
 print('Starting '+arm,flush=True)
 with (E/(arm+'.stdout')).open('w') as out,(E/(arm+'.stderr')).open('w') as err:
  result=subprocess.run(cmd,stdout=out,stderr=err,env=env)
 (E/(arm+'-exit.json')).write_text(json.dumps({'exit_code':result.returncode,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
 print('Finished '+arm+' exit='+str(result.returncode),flush=True)
