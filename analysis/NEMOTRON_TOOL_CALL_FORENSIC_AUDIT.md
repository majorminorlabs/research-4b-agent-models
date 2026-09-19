# NVIDIA Nemotron 3 Nano 4B tool-call forensic audit

Status: **HOLD — NEMOTRON TOOL-CALL ATTRIBUTION AUDIT**  
Scope: completed `candidate-field-v1.1.0` evidence only. No scored task was rerun, and no score, protocol, raw artifact, model, template, adapter, or llama.cpp checkout was changed.

## 1. Executive finding

The preserved evidence supports a **combination with A primary and B as a strict transport consequence**:

- Nemotron generated a repeated sequence of structured tool calls whose final argument was incomplete JSON (`{`), and the generating response ended with `finish_reason: "length"`. This is the closest preserved representation of model output and is invalid under both the NVIDIA template's argument convention and the OpenAI-compatible JSON-string field.
- Frozen llama.cpp successfully parsed the XML tool-call syntax into OpenAI-compatible `message.tool_calls` and then rejected the incomplete argument when the next turn attempted to render the assistant tool-call history. The HTTP 500 was therefore a server-side transport manifestation of malformed history, not evidence that the benchmark adapter corrupted a valid call.
- The scored controller did not call `runner/adapter.py`; it consumed llama.cpp's structured `message.tool_calls` directly. Consequently, the canonical transcript adapter is not the cause of the nine observed parser/transport incidents. The separate simulator `KeyError` is a real infrastructure-invalid controller defect and remains separate.
- NVIDIA does document an OpenAI-compatible llama.cpp server, but its detailed tool-calling deployment example uses vLLM, `qwen3_coder`, and a custom `nano_v3` reasoning parser. The frozen invocation also used deterministic `temperature: 0` and left the native template's default thinking enabled, whereas NVIDIA recommends `temperature=0.6, top_p=0.95` for tool calling and documents `enable_thinking=False` explicitly. Thus the run was valid under the frozen common benchmark contract, but not identical to NVIDIA's recommended tool-calling settings.

The evidence does **not** support C for the transport failures, and does not establish D: the official template is materially mappable to the common OpenAI tool schema, and admission plus many scored turns prove that mapping works. Because raw token streaming was not preserved, confidence is **moderate**, not high. The 17/80 should remain on publication hold pending a separately preregistered resolution; it should not currently be presented as an unqualified capability score.

## 2. Evidence inventory

The machine-readable per-observation manifest is [analysis/forensics/nemotron/manifest.json](forensics/nemotron/manifest.json). It maps admission, 21 scored Nemotron observations, and the separate infrastructure-invalid attempt to request/response, parsed, adapter, simulator, server-log, and score layers.

Preserved for the scored observations:

- `requests-responses.json`: successful request bodies and returned JSON responses; for most fixed-controller HTTP failures, the HTTP 500 JSON body is also present.
- `canonical-interaction.json`: assistant messages as received from llama.cpp, including structured tool calls.
- `simulator-events.json`: simulator calls and termination events for requests that reached the controller's simulator path.
- `result.json`: status, error labels, turns, event summary, and resource samples.
- `server.log`: model/server timings, parser diagnostics, and launch/runtime messages.

Explicitly **NOT PRESERVED**:

- The raw generated token stream and exact generated XML text before llama.cpp parsing.
- The failed second request body for the first-round Q01 artifact: its `server.log` contains the parser 500, but `requests-responses.json` contains only the successful first response.
- A separate scorer-input file and a separate scorer-atom file for each observation; the final processed result and raw result events are preserved, but those intermediate representations are **NOT PRESERVED** as standalone artifacts.
- A scored-path invocation of `runner/adapter.py`; it was not used, so there is no adapter result artifact for these observations.

Inventory counts:

- Neutral admission: 1 Nemotron exchange with two successful HTTP turns.
- Scored Nemotron: 7 first-round tasks plus R2 and R3, 21 task observations total.
- Parser/transport incidents: 9 total — Q01, Q02, and Q03 in each of the three observations. Eight failed HTTP responses are present in request artifacts; the first-round Q01 failed response is not preserved.
- Separate infrastructure-invalid controller crash: 1, preserved under `infrastructure-invalid/R001-nemotron-controller-crash/` and excluded from the valid observation.

## 3. Failure events and earliest observable layer

| observation/task | turn | model output available? | HTTP / representation | adapter | simulator | earliest observable failure | current classification |
|---|---:|---|---|---|---|---|---|
| first/Q01 | 1→2 | Yes, first response; raw tokens no | 200 with 39 calls; final args `{`; server log records 500; failed body not preserved | NOT APPLIED | transport termination | llama.cpp history argument normalization / HTTP transport | A-supported malformed generation; B strict transport; response body incomplete |
| first/Q02 | 3→4 | Yes, turn 3; raw tokens no | 200, finish `length`, 41 calls, final args `{`; next request 500 | NOT APPLIED | prior calls reached simulator | llama.cpp history argument normalization / HTTP transport | A + B |
| first/Q03 | 4→5 | Yes, turn 4; raw tokens no | 200, finish `length`, 43 calls, final args `{`; next request 500 | NOT APPLIED | prior calls reached simulator | llama.cpp history argument normalization / HTTP transport | A + B |
| R2/Q01–Q03 | corresponding turns | Yes; same preserved pattern | 200 response ending in `{`, then HTTP 500 | NOT APPLIED | prior calls reached simulator | llama.cpp history argument normalization / HTTP transport | A + B; deterministic repetition |
| R3/Q01–Q03 | corresponding turns | Yes; same preserved pattern | 200 response ending in `{`, then HTTP 500 | NOT APPLIED | prior calls reached simulator | llama.cpp history argument normalization / HTTP transport | A + B; deterministic repetition |
| infrastructure-invalid/R001 | controller attempt | Partial server log only | server started; controller crashed on simulator `KeyError` | NOT APPLIED | simulator/controller exception | benchmark controller exception handling | C-like controller defect, infrastructure-invalid only; not model attribution |

The nine parser incidents are therefore not nine adapter rejections. They are nine repetitions of the same server boundary: incomplete arguments were first exposed in a successful structured response, then rejected while the next request's assistant history was normalized.

## 4. Exact scored pipeline

`candidate_field_execution.py` constructs a system message, one user message containing the public task JSON, six or fewer broad simulator tool schemas, `tool_choice: auto`, `temperature: 0`, `seed: 0`, `max_tokens: 768`, `reasoning_effort: none`, and `reasoning_format: none`. It optionally sends `chat_template_kwargs: {enable_thinking: false}` only when the controller is invoked with `--thinking-off`; the Nemotron scored invocation did not set that flag.

The actual path was:

```text
fixture + common messages/tools
  -> POST /v1/chat/completions
  -> frozen llama-server --jinja, native GGUF template, Vulkan/RADV
  -> Nemotron generation using XML tool-call template
  -> llama.cpp parser -> OpenAI message.tool_calls (arguments remain strings)
  -> candidate controller json.loads(function.arguments)
  -> Simulator.call(name, dict)
  -> tool-role message with simulator output
  -> next POST
```

Transformations and failure behavior:

- NVIDIA Jinja template: OpenAI tool definitions become `<tools>` instructions; assistant calls are rendered as `<tool_call><function=...><parameter=...>value</parameter>...</function></tool_call>`; tool results become `<tool_response>...</tool_response>`.
- llama.cpp auto-parser: identifies the tag structure and emits OpenAI-compatible calls. It preserves arguments as strings in `common_chat_tool_call.arguments`.
- llama.cpp request normalization: `func_args_not_string` parses assistant tool-call argument strings as JSON before rendering the next prompt. An incomplete `{` throws `Failed to parse tool call arguments as JSON`, which the server exposes as HTTP 500.
- candidate controller: parses returned argument strings with Python `json.loads`; on failure it substitutes `{}` and records `model_malformed_arguments`. This path was not reached for the 500 request itself; prior successful calls could reach the simulator.
- `runner/adapter.py`: accepts transcript JSON plans such as `{"calls":[...]}` and deliberately performs no repair. It was not invoked by this candidate controller, so it cannot explain the observed 500s.

## 5. NVIDIA interface audit

Pinned sources: [BF16 model card at revision `dfaf35d`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16/tree/dfaf35de3e30f1867dd8dbc38a7fc9fb52d3914f), [pinned tokenizer config](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16/blob/dfaf35de3e30f1867dd8dbc38a7fc9fb52d3914f/tokenizer_config.json), and [GGUF model card at revision `ba223d1`](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF/tree/ba223d14e45525f7fae81db77ea8cabeb2fc6c25).

Findings:

1. The expected native call representation is XML/tag based, not a JSON object emitted directly as the assistant text. The template explicitly requires an inner `<function=...>` block inside `<tool_call>`, with `<parameter=name>` values. The expected tool result is `<tool_response>...</tool_response>`.
2. The pinned tokenizer configuration contains the special markers `<|im_start|>`, `<|im_end|>`, `<think>`, `</think>`, `<tool_call>`, `</tool_call>`, `<tool_response>`, and `</tool_response>`, and the same native template is present in the GGUF metadata as recorded in admission `props.json`.
3. NVIDIA's GGUF card documents launching `llama-server` as an OpenAI-compatible API server. It does not document a Nemotron-specific llama.cpp parser flag. NVIDIA's detailed tool-calling server recipe is instead vLLM `>=0.15.1` with `--enable-auto-tool-choice`, `--tool-call-parser qwen3_coder`, and the custom `nano_v3` reasoning parser.
4. NVIDIA recommends `temperature=0.6, top_p=0.95` for tool calling; the frozen benchmark contract used `temperature=0`, did not set `top_p`, and used `max_tokens=768`. NVIDIA documents `enable_thinking=False` for reasoning-off; the scored Nemotron requests used `reasoning_format: none` but did not send `enable_thinking=False`, while the GGUF template defaults `enable_thinking` to true.
5. The invocation therefore matched the common frozen OpenAI-compatible interface and native template, but did not match every NVIDIA-recommended tool-calling generation setting. This is a reproducibility/integration caveat, not evidence that the common interface was impossible.

## 6. Frozen llama.cpp audit

The exact frozen checkout `972d2313bc0bf0a45f634f77d95c9fb03aeab12` contains `nemotron_h` model architecture support and the Jinja/auto-parser path. It detects the pinned template as a tagged tool format, supports parallel calls, and converts calls to OpenAI-compatible `tool_calls`.

The preserved admission exchange is decisive for the basic path: the frozen server returned HTTP 200 with `get_weather` and `{"city":"test-city"}`, then accepted a tool result and returned a normal final answer. Scored Q04–Q07 also contain many successful multi-turn exchanges. There is no preserved example of a valid NVIDIA call being misparsed into an invalid argument.

The frozen implementation's `func_args_not_string` check is strict: when replaying assistant history, a string argument is parsed as JSON and an exception is raised on `{`. That is a reasonable validation of the OpenAI-compatible contract. It is not a repair or tolerant continuation policy, but the evidence does not show it mishandled valid Nemotron syntax. The server log's 500 is consequently best classified as a strict transport consequence of malformed/incomplete model output, not a demonstrated llama.cpp parser bug.

The server also logged that reasoning preservation was enabled by default because the template supports it. This was a frozen runtime setting difference from NVIDIA's explicit reasoning-off template argument and may have contributed to long generations, but the preserved evidence cannot isolate its causal effect.

## 7. Upstream history after the frozen revision

The following later upstream records are relevant context, not runtime changes to this benchmark:

- [Issue #22043](https://github.com/ggml-org/llama.cpp/issues/22043), opened 2026-04-17 at commit `a279d0f`, reports an infinite loop for this exact 4B GGUF when `parallel_tool_calls=true`; the report says `parallel_tool_calls=false` works. This is a real later Nemotron/tool-calling integration warning, but it concerns repeated generation rather than the preserved `{` replay parse error, and it postdates the frozen revision.
- [Issue #21762](https://github.com/ggml-org/llama.cpp/issues/21762), opened 2026-04-11 at `2b2cd57`, reports a second-request prompt-cache serialization crash for this exact model on Vulkan and gives `--cache-ram 0` as a workaround. The observed benchmark failure was an HTTP JSON parse error, not the reported cache crash; this issue nevertheless shows that Nemotron-H/Vulkan multi-turn behavior had later-known runtime hazards.
- Current upstream's [auto-parser documentation](https://github.com/ggml-org/llama.cpp/blob/master/docs/autoparser.md) documents generated PEG parsing and lists Nemotron-family tagged tool formats. It does not identify a post-freeze change that would turn the preserved incomplete `{` into valid JSON or make the first-round Q01 failed response a valid call.
- Current upstream [issue #26737](https://github.com/ggml-org/llama.cpp/issues/26737) reports a later `tool_choice: required` grammar problem for XML-style Nemotron-3 models. It is a different forced-tool grammar path and does not explain these `tool_choice: auto` observations.

No post-freeze commit or release note located in the available upstream history establishes that frozen llama.cpp incorrectly transformed a valid Nemotron call in these observations. A clean diagnostic comparison could still test current parser behavior, but it is not necessary to identify the preserved failure boundary and was not run.

## 8. Adapter audit

`runner/adapter.py` accepts transcript framing plus JSON plans in `{"calls": [...]}` form, or a small set of canonical single-call shapes. It requires string tool names and dictionary arguments, accepts multiple calls, does not repair malformed JSON, and does not process OpenAI `message.tool_calls` objects. That is a deliberate strict transcript adapter.

The candidate controller bypassed it and directly consumed llama.cpp's OpenAI response. The direct path accepts OpenAI IDs, function names, and string-or-object arguments; it JSON-decodes string arguments and records invalid arguments. No preserved event shows a legitimate structured call rejected or corrupted by this adapter. Therefore classification C does not apply to the nine transport failures. C does apply only to the separate controller-side simulator exception, which is already marked infrastructure-invalid and excluded from the scheduled result.

## 9. Admission versus scored exposure

Admission used one simple `get_weather` call with a short argument, `max_tokens=256`, and a two-turn continuation. It demonstrated that the template, model, server parser, OpenAI response conversion, tool-role message, and basic continuation worked.

Scored exposure changed several stressors simultaneously: six broad tools, long public task instructions and state, `max_tokens=768`, many tool turns, repeated prior assistant/tool history, empty-argument calls, parallel calls, and reasoning-preservation defaults. The failing responses are precisely the long responses that reached `finish_reason: length` and ended with an incomplete `{`. Thus admission passed because it was a short single-call compatibility smoke test; it did not certify bounded-generation robustness, repeated calls, or malformed-history handling.

## 10. Raw-generation responsibility

Raw token generation is **NOT PRESERVED**. The strongest available evidence is the returned structured response: repeated calls, final argument `{`, and `finish_reason: length`; the next server log reports the exact JSON parse failure on replay. The same pattern recurs in all three observations for Q01–Q03, while Q04–Q07 complete with no server parser error.

This supports `MODEL_INVALID` for the particular incomplete argument sequence with moderate confidence, but not a claim about all Nemotron capability. It does not support `LLAMA_CPP_INTERPRETATION` because no valid native call is shown to have been rejected or transformed incorrectly. It does support a narrower `LLAMA_CPP_STRICT_TRANSPORT` label: llama.cpp surfaced malformed history as HTTP 500 rather than returning a recoverable structured error. That behavior amplified the model-side failure into a transport-invalid observation.

## 11. Responsibility classification

| category | finding | confidence |
|---|---|---|
| A — genuine model malformed output | Supported for nine incomplete final arguments; the closest response has `{` and `finish_reason: length`, repeated deterministically | Moderate |
| B — frozen llama.cpp limitation/bug | Strict replay validation and HTTP 500 are supported; an actual bug on valid syntax is not | Moderate for strict transport consequence; low for “bug” |
| C — adapter handling bug | Not supported for transport incidents; adapter was bypassed. Separate simulator exception is infrastructure-invalid | High |
| D — legitimate interface incompatibility | Not supported as the primary explanation; native XML calls were successfully mapped and NVIDIA documents llama.cpp API serving. Recommended settings were not fully followed | Moderate against D |
| E — combination | Best overall description: model-side incomplete generation plus strict server transport, with one separate controller defect | High |

## 12. Publication validity and corrective action

Publication status is **HOLD — NEMOTRON TOOL-CALL ATTRIBUTION AUDIT**. The existing 17/80 must not be presented as a clean, standalone Nemotron capability score while this audit is unresolved. The raw evidence and score files remain unchanged. Eventually, a clean rerun would be scientifically justified only as a new, preregistered observation under explicitly selected settings—ideally either NVIDIA's documented tool-calling settings or a deliberately frozen common interface with the reasoning/thinking behavior stated in advance. It must not overwrite these observations.

This audit does not retroactively invalidate all Nemotron evidence: successful admission, Q04–Q07 turns, and preserved model-side malformed behavior remain useful runtime evidence. It does mean the transport-invalid Q01–Q03 outcomes should eventually be reported as a combined model/runtime interaction or compatibility finding, not silently equated with pure capability failure.

## 13. Future admission gate

Do not change the frozen gate retroactively. For the next benchmark version, require a non-scored compatibility suite containing: at least two tool turns; one multi-call response; nested and non-string argument values; a long-enough generation budget; reasoning on/off explicitly; tool-result continuation; and an intentionally malformed-history probe that verifies the server returns a controlled error without crashing the controller. Preserve raw generated text or token-level parser traces whenever a transport error occurs.

## 14. Return checklist

1. Failure events audited: **9 repeated llama.cpp parser/transport incidents**, plus **1 separate infrastructure-invalid controller crash**; the processed run set also records 299 invalid-argument events across all Nemotron observations.
2. Raw model generation: **not preserved**; closest structured responses are preserved.
3. Exact malformed behavior: repeated tool calls, final argument string `{`, `finish_reason: length`; next request returns HTTP 500 with `Failed to parse tool call arguments as JSON`.
4. NVIDIA expected behavior: XML native tool call and tool response tags; arguments must be complete parameter values; OpenAI-compatible llama.cpp server documented, vLLM parser recipe detailed.
5. Invocation match: common frozen interface yes; all NVIDIA recommendations no (`temperature`, `top_p`, explicit `enable_thinking=False`).
6. Frozen llama.cpp: basic Nemotron/template/tool path worked; strict replay rejection was observed; no valid-call misparse demonstrated.
7. Post-freeze history: issues #22043, #21762, #26737 and current auto-parser documentation are relevant context, not a proven fix for this exact failure.
8. Adapter: correct for its transcript domain and not on the scored path; not causal for the HTTP 500s.
9. Admission/scored difference: short one-call 256-token smoke test versus long, multi-tool, repeated, 768-token exposure with reasoning-preserve default.
10. Overall classification: **E**, specifically A primary + strict B transport consequence; C only for the separately excluded controller crash; D not established.
11. Confidence: **moderate overall; high for the failure boundary, moderate for model attribution, low for claiming a llama.cpp bug**.
12. 17/80: **not scientifically publishable as an unqualified capability score while on hold**.
13. Event invalidation: no raw evidence is edited or silently invalidated; later reporting should separate transport/compatibility effects.
14. Clean rerun: **yes, scientifically justified only as a separately preregistered diagnostic/benchmark run**, never as a replacement of these observations.
15. Future improvement: stronger multi-turn/multi-call/long-generation admission gate and raw-generation preservation.

