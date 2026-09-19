# Nemotron configuration-resolution protocol v1.0.0

Status: **preregistered before resolution execution**. This protocol resolves one configuration question; it is not an optimization sweep.

## Question

Did the original Nemotron 17/80 result materially depend on using the frozen common benchmark generation configuration instead of NVIDIA's documented Nemotron tool-calling configuration?

## Fixed elements

The following remain unchanged: NVIDIA Nemotron 3 Nano 4B Q4_K_M GGUF and SHA-256 `be5d9a656a51922f24f1f09a759cebb694e1f5d9728bf0ef9f8c972c5a0b5ef2`; ThinkPad T14 Gen 2a; frozen llama.cpp `972d2313bc0bf0a45f634f77d95c9fb03aeab12c`; Vulkan/RADV; `mmagent-offline`; Q01–Q07, prompts, tool schemas, simulator, scorer, scoring atoms, catastrophic caps, context ceiling 16,384, 768 generated-token ceiling, resource rule, and retry classification.

## Configuration resolution

Source: NVIDIA's pinned model card revision `dfaf35de3e30f1867dd8dbc38a7fc9fb52d3914f` and pinned GGUF card revision `ba223d14e45525f7fae81db77ea8cabeb2fc6c25`.

| Setting | Resolution | Basis |
|---|---|---|
| `chat_template_kwargs.enable_thinking` | **REQUIRED for this resolution: `false`** | NVIDIA documents `enable_thinking=False` to turn reasoning off; the native template defaults it to true. |
| `temperature` | **RECOMMENDED: `0.6`** | NVIDIA explicitly recommends 0.6 for tool calling. |
| `top_p` | **RECOMMENDED: `0.95`** | NVIDIA explicitly recommends 0.95 for tool calling. |
| `seed` | Fixed benchmark value `0` | Frozen deterministic benchmark setting; not an NVIDIA tool-calling requirement. |
| `max_tokens` | Fixed benchmark value `768` | Explicitly unchanged by this resolution. |
| `reasoning_effort` / `reasoning_format` | Fixed common-interface values `none` / `none` | No NVIDIA requirement identified for llama.cpp; kept fixed for comparability. |
| tool parser | Native frozen llama.cpp Jinja/auto-parser; **no new parser flag** | NVIDIA documents llama.cpp OpenAI-compatible serving but does not document a Nemotron-specific llama.cpp parser flag. |
| vLLM `qwen3_coder` and `nano_v3` parser settings | **UNSUPPORTED/UNVERIFIED for this llama.cpp run** | NVIDIA documents these for vLLM, not as llama.cpp settings; they are not transplanted into this experiment. |

The one corrected configuration is therefore: the original request and runtime with `temperature=0.6`, `top_p=0.95`, and `chat_template_kwargs={"enable_thinking":false}`. No other setting changes.

## Schedule

Execute exactly three authorized observations, each in fixed task order Q01, Q02, Q03, Q04, Q05, Q06, Q07: 21 maximum valid scored observations. The schedule is frozen before inspecting any resolution score. Infrastructure-invalid attempts may be retried under the existing policy; model mistakes are never retried or repaired.

## Evidence capture

Capture request JSON, returned HTTP JSON/raw body, HTTP status, finish reason, usage/generated-token count, extracted structured calls, parser/server log, simulator events, resource samples, and result status. Frozen llama.cpp is not patched. True pre-parser token/XML output is not assumed available; if unavailable, record `NOT PRESERVED` and use the returned response plus server log as the closest representation.

## Decision rule

- If the corrected configuration removes the repeated `{` + `finish_reason:length` + parser/transport pattern and yields valid observations, those observations become final Nemotron v1.0 capability evidence; original 17/80 observations are labeled **SUPERSEDED — COMMON-CONFIGURATION / ATTRIBUTION-LIMITED RUN**.
- If the corrected configuration repeats the same pattern without infrastructure defects, the corrected observations become final Nemotron evidence and the pattern is reported as a configuration/runtime interaction, not silently repaired.
- If a new runtime/infrastructure/interface defect prevents interpretable execution, Nemotron receives no final capability score and is reported under compatibility/configuration limitation.

After this schedule, experimental collection closes permanently.

