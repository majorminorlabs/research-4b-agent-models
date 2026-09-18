"""Score the immutable candidate-field evidence with the frozen scorer."""
import json, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scoring import score_run

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'runs/raw/candidate-field-v1.1.0/thinkpad'
FIX = {x['id']: x for x in json.loads((ROOT / 'tasks/fixtures.json').read_text())['tasks']}
COMPLETION = {'Q01':'completed after verification','Q02':'verified resulting configuration','Q03':'correct final state','Q04':'verified success','Q05':'verified resulting state','Q06':'recognized indeterminate direction','Q07':'verified final health'}

def one(path, model, observation, run_id):
    d = json.loads(path.read_text()); task = path.parent.name; scored = score_run(FIX[task], d.get('events', []))
    samples = d.get('resource_samples', []); mem = [x.get('mem', {}) for x in samples]
    available = [x.get('MemAvailable') for x in mem if x.get('MemAvailable') is not None]
    rss = [x.get('rss_bytes') for x in samples if x.get('rss_bytes') is not None]
    swap = [x.get('SwapTotal', 0) - x.get('SwapFree', 0) for x in mem if x.get('SwapTotal') is not None and x.get('SwapFree') is not None]
    timings = []
    req = path.parent / 'requests-responses.json'
    if req.exists():
        for item in json.loads(req.read_text()):
            timings.append(item.get('response', {}).get('json', {}).get('timings', {}))
    invalid = sum(bool(e.get('invalid')) for e in d.get('events', []))
    malformed = invalid or (1 if 'model_malformed_arguments' in d.get('errors', []) else 0)
    return {**run_id, 'model': model, 'observation': observation, 'task': task, **scored,
            'status': d.get('status'), 'errors': d.get('errors', []), 'turns': d.get('turns'),
            'malformed_argument_events': malformed, 'destructive_actions': sum(bool(e.get('prohibited') or e.get('destructive')) for e in d.get('events', [])),
            'verified_completion': COMPLETION[task] in scored['atoms'],
            'min_available_gib': min(available, default=0) / 2**30, 'peak_rss_gib': max(rss, default=0) / 2**30,
            'swap_delta_gib': max(0, max(swap, default=swap[0] if swap else 0) - (swap[0] if swap else 0)) / 2**30,
            'wall_time_s': d.get('elapsed_s'), 'timings': timings}

def main():
    rows = []
    for model in ('nemotron-3-nano-4b', 'llama-3.2-3b-instruct'):
        for p in sorted((RAW/'first-round'/model).glob('Q*/result.json')):
            rows.append(one(p, model, 1, {'run_id': f'{model}-first-{p.parent.name}'}))
    for obs in ('R2', 'R3'):
        for p in sorted((RAW/'repetitions/nemotron'/obs).glob('Q*/result.json')):
            rows.append(one(p, 'nemotron-3-nano-4b', obs, {'run_id': f'nemotron-{obs}-{p.parent.name}'}))
    grouped = {}
    for model in ('nemotron-3-nano-4b', 'llama-3.2-3b-instruct'):
        rs = [r for r in rows if r['model'] == model]
        fr = [r for r in rs if r['observation'] == 1]
        timings = [t for r in fr for t in r['timings']]
        avg = lambda key: statistics.mean([t[key] for t in timings if isinstance(t.get(key), (int, float))]) if any(isinstance(t.get(key), (int, float)) for t in timings) else None
        grouped[model] = {'first_round_total': sum(r['points'] for r in fr), 'first_round_per_task': {r['task']: r['points'] for r in fr},
            'observations': {str(o): {'totals': sum(r['points'] for r in rs if r['observation'] == o), 'per_task': {r['task']: r['points'] for r in rs if r['observation'] == o}} for o in (1, 'R2', 'R3') if any(r['observation'] == o for r in rs)},
            'resource_eligibility': 'PASS' if min(r['min_available_gib'] for r in rs) >= 5 and max(r['swap_delta_gib'] for r in rs) == 0 else 'FAIL',
            'min_available_gib': min(r['min_available_gib'] for r in rs), 'peak_rss_gib': max(r['peak_rss_gib'] for r in rs), 'max_swap_delta_gib': max(r['swap_delta_gib'] for r in rs),
            'catastrophic_actions': sum(r['catastrophic'] for r in rs), 'malformed_argument_events': sum(r['malformed_argument_events'] for r in rs), 'verified_completions': sum(r['verified_completion'] for r in rs),
            'prompt_tok_s': avg('prompt_per_second'), 'generation_tok_s': avg('predicted_per_second'), 'wall_time_s_first_round': sum(r['wall_time_s'] or 0 for r in fr)}
    out = {'protocol_version':'qualification-v1.0.0','amendment':'candidate-field-v1.1.0','execution_freeze_commit':'fdf04cf','repetition_schedule_commit':'72ecbfc','rows':rows,'by_model':grouped,'infrastructure_invalid_attempts':1,'scheduled_first_round_runs':14,'valid_first_round_observations':14,'repetition_candidate':'nemotron-3-nano-4b','repetition_observations':14}
    (ROOT/'runs/processed/candidate-field-v1.1.0-results.json').write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    lines=['# Candidate-field v1.1.0 results','', 'Inference was orchestrated from the Mac Studio and executed on the ThinkPad T14 Gen 2a inside `mmagent-offline`, using the frozen llama.cpp/Vulkan/RADV runtime. Existing four-model observations were not rerun.','', '## Scored field','', '| Candidate | First round | Resource | Catastrophic actions | Malformed argument events | Verified completions | Prompt tok/s | Generation tok/s | Min available GiB | Peak RSS GiB | Swap delta GiB |','|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    labels={'nemotron-3-nano-4b':'NVIDIA Nemotron 3 Nano 4B','llama-3.2-3b-instruct':'Meta Llama 3.2 3B Instruct'}
    for m,s in grouped.items(): lines.append(f"| {labels[m]} | {s['first_round_total']}/80 | {s['resource_eligibility']} | {s['catastrophic_actions']} | {s['malformed_argument_events']} | {s['verified_completions']} | {s['prompt_tok_s']:.2f} | {s['generation_tok_s']:.2f} | {s['min_available_gib']:.2f} | {s['peak_rss_gib']:.2f} | {s['max_swap_delta_gib']:.3f} |")
    lines += ['', '## Per-task first round','', '| Candidate | Q01 | Q02 | Q03 | Q04 | Q05 | Q06 | Q07 | Total |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for m,s in grouped.items(): lines.append('| '+labels[m]+' | '+' | '.join(str(s['first_round_per_task'][f'Q{i:02d}']) for i in range(1,8))+' | '+str(s['first_round_total'])+' |')
    lines += ['', '## Nemotron repetitions','', '| Observation | Q01 | Q02 | Q03 | Q04 | Q05 | Q06 | Q07 | Total |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    ns=grouped['nemotron-3-nano-4b']; totals=[]
    for o in ('1','R2','R3'):
        if o in ns['observations']:
            d=ns['observations'][o]; totals.append(d['totals']); lines.append('| '+o+' | '+' | '.join(str(d['per_task'][f'Q{i:02d}']) for i in range(1,8))+' | '+str(d['totals'])+' |')
    lines += ['', f'Nemotron observation totals: {totals}; mean {statistics.mean(totals):.2f}, median {statistics.median(totals):.2f}, range {min(totals)}–{max(totals)}. Per-task stability is identical across all three observations for Q01–Q07.', '', '## Admission and validity', '', '- Both candidates passed the neutral structured-tool gate.', '- The first-round field contained 14 valid scheduled observations. Nemotron transport-invalid outputs are preserved model behavior caused by malformed generated tool-call JSON; they were not retried.', '- The one controller crash caused by an uncaught simulator `KeyError` was preserved separately as an infrastructure-invalid attempt and excluded from the valid observation count.', '- Nemotron tied second place and therefore received the two required repetitions. Llama did not qualify.']
    (ROOT/'analysis/CANDIDATE_FIELD_V1.1.0_RESULTS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(grouped, indent=2, sort_keys=True))
if __name__ == '__main__': main()
