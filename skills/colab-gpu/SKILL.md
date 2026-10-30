---
name: colab-gpu
description: Run GPU work (embedding a corpus, finetuning, benchmarks, anything too heavy for a laptop without CUDA) on a rented Google Colab runtime via the official `colab` CLI (inside WSL Ubuntu on Windows). Use whenever a task needs a GPU or CUDA, or when the user mentions Colab, T4/L4/A100/H100, or "run it on a GPU".
---

# GPU compute via the Colab CLI

For anything needing a GPU (embedding a corpus, finetuning, benchmarks), do not grind it out on the local CPU - rent a Colab runtime with Google's official CLI ([googlecolab/google-colab-cli](https://github.com/googlecolab/google-colab-cli)).

## Setup (once)

- The CLI supports Linux and macOS only. On Windows, install and run it inside WSL Ubuntu.
- Install: `uv tool install google-colab-cli` (or `pip install google-colab-cli`).
- The first command asks you to log in with your Google account. Which GPUs you get depends on your Colab plan.

On Windows, drive it from the Windows side through WSL:

```bash
wsl -d Ubuntu -e bash -lc 'cd /mnt/c/Users/<you>/path/to/repo && colab ...'
```

## Typical flow - and always `colab stop` when finished

```bash
colab new -s job --gpu T4          # also L4, A100, H100; plan-gated, may refuse
colab upload -s job local.jsonl /content/local.jsonl
colab exec -s job --timeout 2400 -f script.py
colab download -s job /content/out.npz data/out.npz
colab stop -s job
```

## Gotchas learned the hard way

- **Pass `--timeout`.** The default is far too short for a large model download and the exec dies mid-job.
- **The websocket goes quiet while the kernel keeps working.** `colab status` can read IDLE with a stale timestamp while the job is actually finishing - check `colab ls` for output files and trust the artifacts, not the status line.
- **`colab download` needs an explicit destination FILENAME**, not a directory.
- `colab skill` prints a full agent-oriented usage guide; read it rather than guessing.
- The free tier has usage limits, so idle sessions still cost future access. Stop runtimes you are not using.
