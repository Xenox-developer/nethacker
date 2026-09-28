"""Sequential foreground native arena commands, no episode rerolls."""
import os,sys,json,subprocess,datetime,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent
freeze=json.loads((E/'freeze.json').read_text())
def verify():
 for arm,files in freeze['arms'].items():
  for p,h in files.items():assert hashlib.sha256((E/arm/p).read_bytes()).hexdigest()==h,(arm,p)
for batch in freeze['batches']:
 verify();name=batch['name'];arm=batch['arm']
 env=os.environ.copy();env.pop('NETHACK_ARENA_SECRET',None)
 env['PRIVATE31_DIAGNOSTICS']='1';env['PRIVATE31_DIAGNOSTICS_DIR']=str(E/'diagnostics'/name)
 cmd=[sys.executable,'-m','nethackers.arena.run','--solution',str(E/arm),'--batch',json.dumps([[s,'val-dwa-law-fem'] for s in batch['seeds']]),'--evaluation-id','local','--secret','public','--max-steps','1000000','--no-progress-timeout','10000','--action-timeout','120','--max-parallel-evals','4','--out',str(E/(name+'-raw.json'))]
 (E/(name+'-command.json')).write_text(json.dumps({'argv':cmd,'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'diagnostics_env':{k:v for k,v in env.items() if k.startswith('PRIVATE31_')}},indent=2))
 print('Starting '+name,flush=True)
 with (E/(name+'.stdout')).open('w') as out,(E/(name+'.stderr')).open('w') as err:result=subprocess.run(cmd,stdout=out,stderr=err,env=env)
 (E/(name+'-exit.json')).write_text(json.dumps({'exit_code':result.returncode,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
 print('Finished '+name+' exit='+str(result.returncode),flush=True)
verify()
