# Hi, I'm Soki Fukuda (createcentury)

**AI Systems Engineer · Apple Silicon kernel optimization**

Getting next-generation AI architectures to run natively, and fast, on Apple Silicon — hand-rolled Metal kernels, not framework-bound.

---

## ⚡ Featured: [mamba-metal](https://github.com/createcentury/mamba-metal)

**Mamba (Selective State Space Model) inference in Metal Shading Language**, end-to-end on Apple Silicon.

- **Custom MSL kernels** for selective scan: parallel prefix scan over `(a, b)` pairs, SIMD-group + threadgroup-memory bridge, inter-chunk running prefix held in SRAM.
- **Forward-pass feature parity** with Mamba's official CUDA kernel (variable B/C, D skip, `delta_softplus`, z gate, fp16 data + fp32 accumulation, arbitrary `seqlen` via chunking).
- **End-to-end inference** of `state-spaces/mamba-{130m, 370m, 1.4b}-hf` checkpoints — load HuggingFace weights, tokenize with `transformers`, generate text.
- **O(L) incremental decoding** via SSM state + conv1d sliding-window caching: flat **~7 ms/token (≈ 145 tok/s)** on M4 Max for mamba-130m, **independent of decode horizon** measured up to 2000 tokens.
- **Selective scan kernel throughput**: ~187 GFLOPS at `seqlen=32k`; Unified Memory bandwidth measured at ~290 GB/s with vec4 loads.
- Bilingual (EN/JA) docs + per-step experimental log.

## 🧠 Technical focus

- **Low-level optimization on Apple Silicon**: writing kernels directly in Metal Shading Language, controlling SIMD-group primitives and threadgroup memory by hand.
- **Parallel scan algorithms**: turning sequential recurrences into associative operators that map onto warp-level prefix scans (Blelloch / Hillis-Steele).
- **Hardware-aware AI**: SSM/Mamba family, in-SRAM state caching, fp16 data with fp32 accumulation, Unified Memory bandwidth profiling.

## 🛠️ Stack

- **Languages**: Python, Metal Shading Language (MSL)
- **Frameworks**: MLX (Apple), `transformers` (tokenizer), NumPy
- **Areas**: selective state space models, parallel prefix scan, kernel fusion, hardware bandwidth analysis

---

## 📬 Connect

- **LinkedIn**: [fukuda-soki](https://www.linkedin.com/in/fukuda-soki/)
- **Blog**: [createcentury.github.io/blog](https://createcentury.github.io/blog) — step-by-step write-ups of each kernel
- **Status**: Open to roles where low-level optimization meets next-generation AI architectures.

---

## 🗓️ 今日の名言

<!--START_SECTION:quote-->
🗓️ 2026-05-16
💬 "Life is just a chance to grow a soul." — A. Powell Davies
<!--END_SECTION:quote-->
