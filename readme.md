# eo_vortilo — Esperanto Writing Analysis Tools

A collection of utilities for analyzing the written form of the Esperanto language.

## Parts

### 1. CLI application (`main.py`)

A Python CLI that reads a command from the config at the top of `main.py` and executes it. The available commands are defined in the `Command` enum in `main.py`. They cover:

- reading and preparing source XML files (`prepar_ilo`)
- filtering, classifying, and converting word lists (`filtr_ilo`)
- frequency counting, statistics, and analysis (`analiz_ilo`)

> **Note:** `data_folder` and `current_task` at the top of `main.py` are hardcoded for the developer's local setup and must be adjusted before running.

### 2. Interactive Jupyter notebooks

- `dulitera_silabaro.ipynb` — syllable splitting using the **two-letter (AVK/PVK)** approach
- `literumado_laŭ_kevako.ipynb` — syllable splitting using the **kevako** method

Each notebook demonstrates a different algorithm for dividing Esperanto words into syllables.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Run tests

```bash
pytest tests/
# or a single file:
pytest tests/test_du_litera_silab_ilo.py -v
```

## Run the CLI

```bash
python3 main.py
```

*(Edit `data_folder` and `current_task` in `main.py` first.)*

# todo

[ ] statistiko de unuopaj literoj
    [ ] statistiko de unuopaj literoj, grupitaj laŭ klasoj: {_,K,V}, kun diagramo
[ ] statistiko de duopoj
[x] statistiko de triopoj: `all_files_vortoj_oftecoj_triopoj.yml`
[ ] metu la kodon kaj la datumojn sub GITon



garantianto
kantante
antaŭvidanta
anticipanton

kaj 
kelkaj
kajtoj

pro
supro
provo
aprobi

la: 612_479
de: 308_999
kaj: 219_359
en: 146_802
al: 96_398
estas: 71_030
ne: 68_672
mi: 57_988
por: 57_813
li: 56_887
ke: 53_742
pri: 47_697
estis: 37_418
