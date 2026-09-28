from pathlib import Path
import subprocess,sys,json,os,time
E=Path('/workspace/evaluation/peer-depth20')
batch=[[s,'val-dwa-law-fem'] for s in list(range(15))+list(range(3000,3008))]
env=os.environ.copy(); env.pop('NETHACK_ARENA_SECRET',None)
for arm,solution in [('baseline',str(E/'baseline')),('hybrid','/workspace')]:
 cmd=[sys.executable,'-m','nethackers.arena.run','--solution',solution,'--batch',json.dumps(batch),'--evaluation-id','local','--secret','public','--max-steps','1000000','--no-progress-timeout','10000','--action-timeout','120','--max-parallel-evals','4','--out',str(E/(arm+'-rows.json'))]
 (E/(arm+'-command.json')).write_text(json.dumps(cmd,indent=2))
 print('START',arm,flush=True); start=time.time()
 with (E/(arm+'.log')).open('w') as log:
  proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=env)
  for line in proc.stdout: log.write(line); log.flush(); print(line,end='',flush=True)
  rc=proc.wait()
 (E/(arm+'-execution.json')).write_text(json.dumps({'returncode':rc,'elapsed_seconds':time.time()-start}))
 if rc: raise SystemExit(rc)
 print('FINISHED',arm,flush=True)
