# Model and dependency notices

This repository contains benchmark code, metadata, documentation, and preserved JSON/log evidence. It does not contain model weights.

Model identities, pinned revisions, GGUF sources, hashes, and license labels are recorded in models/ and provenance/. Public distribution must comply with each upstream license:

- Ministral 3 3B: Apache-2.0; https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512
- Qwen3 4B: Apache-2.0; https://huggingface.co/Qwen/Qwen3-4B
- Qwen2.5 3B: Qwen Research License as recorded in the frozen manifest; https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- IBM Granite 4.1 3B: Apache-2.0; https://huggingface.co/ibm-granite/granite-4.1-3b
- NVIDIA Nemotron 3 Nano 4B: NVIDIA Nemotron Open Model License; https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16
- Meta Llama 3.2 3B Instruct: Llama 3.2 Community License; https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

The benchmark uses Python standard-library modules in the checked-in implementation. llama.cpp is an external runtime pinned by commit and is not vendored in this repository. Source links and revision identities are provenance, not redistribution of upstream weights or license grants.

