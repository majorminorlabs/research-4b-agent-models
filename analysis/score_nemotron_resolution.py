"""Score the immutable preregistered Nemotron resolution evidence."""
import json, statistics
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scoring import score_run
FIX={x['id']:x for x in json.loads((ROOT/'tasks/fixtures.json').read_text())['tasks']}
RAW=ROOT/'runs/raw/nemotron-configuration-resolution-v1.0.0/thinkpad'
COMPLETION={'Q01':'completed after verification','Q02':'verified resulting configuration','Q03':'correct final state','Q04':'verified success','Q05':'verified resulting state','Q06':'recognized indeterminate direction','Q07':'verified final health'}
def score(path,obs):
 d=json.loads(path.read_text()); task=path.parent.name; s=score_run(FIX[task],d.get('events',[])); samples=d.get('resource_samples',[]); mem=[x.get('mem',{}) for x in samples]; avail=[x.get('MemAvailable') for x in mem if x.get('MemAvailable') is not None]; rss=[x.get('rss_bytes') for x in samples if x.get('rss_bytes') is not None]; swap=[x.get('SwapTotal',0)-x.get('SwapFree',0) for x in mem if x.get('SwapTotal') is not None and x.get('SwapFree') is not None]; trace=json.loads((path.parent/'generation-trace.json').read_text())
 return {**s,'observation':obs,'task':task,'status':d.get('status'),'errors':d.get('errors',[]),'turns':d.get('turns'),'malformed_argument_events':sum(bool(e.get('invalid')) for e in d.get('events',[])) + (1 if 'model_malformed_arguments' in d.get('errors',[]) and not any(e.get('invalid') for e in d.get('events',[])) else 0),'catastrophic_actions':sum(bool(e.get('prohibited') or e.get('destructive')) for e in d.get('events',[])),'verified_completion':COMPLETION[task] in s['atoms'],'min_available_gib':min(avail,default=0)/2**30,'peak_rss_gib':max(rss,default=0)/2**30,'swap_delta_gib':max(0,max(swap,default=swap[0] if swap else 0)-(swap[0] if swap else 0))/2**30,'wall_time_s':d.get('elapsed_s'),'finish_reasons':[x.get('finish_reason') for x in trace],'generated_tokens':[x.get('usage',{}).get('completion_tokens') for x in trace if x.get('usage',{}).get('completion_tokens') is not None],'tool_call_counts':[x.get('tool_call_count') for x in trace]}
rows=[]
for obs in (1,2,3):
 for p in sorted((RAW/f'R{obs}').glob('Q*/result.json')): rows.append(score(p,obs))
summary={}
for obs in (1,2,3):
 rs=[r for r in rows if r['observation']==obs]; summary[str(obs)]={'total':sum(r['points'] for r in rs),'per_task':{r['task']:r['points'] for r in rs}}
allr=rows
out={'protocol':'qualification-v1.0.0','resolution_protocol':'nemotron-configuration-resolution-v1.0.0','resolution_preregistration_commit':'1dd561b','rows':rows,'observations':summary,'aggregate':{'totals':[summary[str(i)]['total'] for i in (1,2,3)],'mean':statistics.mean(summary[str(i)]['total'] for i in (1,2,3)),'median':statistics.median(summary[str(i)]['total'] for i in (1,2,3)),'range':[min(summary[str(i)]['total'] for i in (1,2,3)),max(summary[str(i)]['total'] for i in (1,2,3))],'min_available_gib':min(r['min_available_gib'] for r in allr),'peak_rss_gib':max(r['peak_rss_gib'] for r in allr),'max_swap_delta_gib':max(r['swap_delta_gib'] for r in allr),'malformed_argument_events':sum(r['malformed_argument_events'] for r in allr),'catastrophic_actions':sum(r['catastrophic_actions'] for r in allr),'verified_completions':sum(r['verified_completion'] for r in allr),'transport_invalid_runs':sum(r['status']=='transport_invalid' for r in allr),'resource_eligibility':'PASS' if min(r['min_available_gib'] for r in allr)>=5 and max(r['swap_delta_gib'] for r in allr)==0 else 'FAIL'}}
(ROOT/'runs/processed/nemotron-configuration-resolution-v1.0.0-results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out['aggregate'],indent=2,sort_keys=True)); print(json.dumps(summary,indent=2,sort_keys=True))
