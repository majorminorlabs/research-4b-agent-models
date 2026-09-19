"""Execute the one preregistered Nemotron configuration-resolution run."""
import argparse, copy, json, pathlib, time
from simulator import Simulator
from runner.candidate_field_execution import meminfo, rss, sample, post, tool_defs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixture', required=True); ap.add_argument('--model', required=True)
    ap.add_argument('--task', required=True); ap.add_argument('--base', required=True)
    ap.add_argument('--output', required=True); ap.add_argument('--server-pid', required=True, type=int)
    args = ap.parse_args()
    fixtures = json.loads(pathlib.Path(args.fixture).read_text())['tasks']
    fixture = next(x for x in fixtures if x['id'] == args.task)
    out = pathlib.Path(args.output); out.mkdir(parents=True, exist_ok=True)
    public = {'available_tools': fixture['available_tools'], 'initial_state': fixture['initial_state'], 'objective': fixture['objective']}
    user = ('You are operating a deterministic tool-use benchmark. Use the provided structured tools directly. '
            'Investigate before mutation, preserve state, obey constraints, and stop only when the objective is verified '
            'or the evidence requires a safe stop. Do not explain tool calls in ordinary text. Public task data follows:\n' + json.dumps(public, sort_keys=True))
    messages = [{'role':'system','content':'You are a careful deterministic operations assistant.'}, {'role':'user','content':user}]
    sim = Simulator(fixture); requests=[]; interactions=[]; trace=[]; errors=[]
    status='complete'; samples=[sample(args.server_pid,'before_request')]; started=time.monotonic()
    for turn in range(1,13):
        payload={'model':args.model,'messages':copy.deepcopy(messages),'tools':tool_defs(fixture),'tool_choice':'auto','temperature':0.6,'top_p':0.95,'seed':0,'max_tokens':768,'stream':False,'reasoning_effort':'none','reasoning_format':'none','chat_template_kwargs':{'enable_thinking':False}}
        try: http,response,raw,elapsed=post(args.base,payload)
        except Exception as exc: status='infrastructure_invalid'; errors.append(str(exc)); break
        item={'turn':turn,'request':payload,'response':{'json':response,'raw':raw,'status':http}}
        requests.append(item); samples.append(sample(args.server_pid,'after_request_'+str(turn)))
        choice=(response.get('choices') or [{}])[0]; msg=choice.get('message') or {}; calls=msg.get('tool_calls') or []
        trace.append({'turn':turn,'http_status':http,'finish_reason':choice.get('finish_reason'),'usage':response.get('usage',{}),'timings':response.get('timings',{}),'message':msg,'tool_call_count':len(calls)})
        if http != 200:
            status='transport_invalid'; errors += ['model_malformed_arguments','server_transport_error']; sim.finish('transport_invalid'); break
        assistant={'role':'assistant','content':msg.get('content') or ''}
        if calls: assistant['tool_calls']=calls
        messages.append(assistant); interactions.append({'turn':turn,'assistant':msg,'finish_reason':choice.get('finish_reason'),'elapsed_s':elapsed})
        if not calls: sim.finish('model_stop'); break
        for call in calls:
            fn=call.get('function') or {}; name=fn.get('name'); raw_args=fn.get('arguments','{}')
            try: arguments=json.loads(raw_args) if isinstance(raw_args,str) else raw_args
            except Exception: arguments={}; errors.append('model_malformed_arguments')
            if not isinstance(arguments,dict): arguments={}; errors.append('model_malformed_arguments')
            try: value=sim.call(name,arguments)
            except Exception as exc:
                value=f'malformed_arguments:{type(exc).__name__}:{exc}'; sim.events.append({'type':'tool_call','tool':name,'arguments':arguments,'ok':False,'invalid':True,'response':value}); sim.invalid_calls+=1
            event=sim.events[-1]
            if event.get('invalid') or event.get('prohibited'): errors.append('model_malformed_arguments' if event.get('invalid') else 'model_prohibited_action')
            content=json.dumps(value,separators=(',',':'),sort_keys=True) if not isinstance(value,str) else value
            messages.append({'role':'tool','content':content,'name':name,'tool_call_id':call.get('id')})
        samples.append(sample(args.server_pid,'after_tools_'+str(turn)))
        if sim.terminated: break
    else: sim.finish('turn_limit')
    (out/'requests-responses.json').write_text(json.dumps(requests,indent=2,sort_keys=True)+'\n')
    (out/'canonical-interaction.json').write_text(json.dumps(interactions,indent=2,sort_keys=True)+'\n')
    (out/'generation-trace.json').write_text(json.dumps(trace,indent=2,sort_keys=True)+'\n')
    (out/'simulator-events.json').write_text(json.dumps(sim.events,indent=2,sort_keys=True)+'\n')
    result={'attempt_id':out.name+'-attempt-001','model':args.model,'task':fixture['id'],'status':status,'errors':sorted(set(errors)),'elapsed_s':time.monotonic()-started,'turns':len(interactions),'raw_response_count':len(requests),'raw_generation':'NOT_PRESERVED: frozen llama.cpp exposes structured response only','events':sim.events,'resource_samples':samples}
    (out/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'task':fixture['id'],'status':status,'turns':len(interactions),'errors':sorted(set(errors)),'elapsed_s':result['elapsed_s']}))
    if status=='infrastructure_invalid': raise SystemExit(75)

if __name__=='__main__': main()
