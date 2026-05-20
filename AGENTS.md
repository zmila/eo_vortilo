# eo_vortilo — agent instructions

## What this is

Esperanto word-processing tools: syllable splitting (AVK/PVK modes, kevako method), word filtering/classification, and statistics. Pure Python 3 — stdlib + pytest only.

## Commands

```bash
pytest tests/                           # all tests
pytest tests/test_du_litera_silab_ilo.py -v  # single test file
python3 main.py                         # CLI entrypoint (hardcoded paths — may fail as-is)
```

## Key structure

- `main.py` — `Command` enum + `TaskExecutor` dispatcher (hardcoded `data_folder` + `current_task`)
- `iloj/` — processing modules: `prepar_ilo` (XML), `filtr_ilo` (filter/classify), `analiz_ilo` (stats), `du_litera_silab_ilo` (two-letter syllable splitter), `kevak_ilo` (kevako syllable splitter)
- `tests/` — pytest suite (uses `sys.path.insert(0, ...)` hack to import parent)
- `data/` — processed YAML/CSV outputs (gitignored? no — tracked)
- `*.ipynb` — Jupyter notebooks for exploration

## Conventions

- **Esperanto naming** throughout: variables, functions, comments, commit messages
- **Formatter**: `ruff` (VSCode: `charliermarsh.ruff`)
- Only dependency outside stdlib is `pytest` (listed in `requirements-dev.txt`)

## Gotchas

- `main.py` has developer-hardcoded paths (`~/prg/java/PseudoTextGenerator/...`); the `Command` enum + `current_task` tuple are set manually to pick a pipeline stage
- Tests use `sys.path.insert(0, ...)` instead of an installed package — always run from repo root

