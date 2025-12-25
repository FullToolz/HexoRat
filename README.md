# HexoRat
Rating the Sh*t out of Binaries

HexoRat is a small, focused Python utility that "rates" windows of a binary for suspicious control-flow and data-manipulation patterns (CMP, JCC, XOR, backward jumps). It's intended as a fast triage scanner to highlight likely areas of interest when reverse-engineering PE/ELF files — for example, potential string-decode loops, conditional-cluster hotspots, and other heuristics that often indicate obfuscation or unpacking logic.

NOTE: Use this tool only on binaries you are authorized to analyze. See the "Legal & Security" section below.

Table of contents
- About
- Features
- Requirements
- Installation
- Usage
- Outputs
- Development
- Contributing
- License
- Legal & Security

About
-----
HexoRat performs a sliding-window analysis over a binary and scores each window for the presence of:
- CMP-like bytes (heuristic: 0x38–0x3F)
- JCC short/near opcodes (heuristic: 0x70–0x7F and 0x0F 0x8x)
- XOR-like opcodes (heuristic: 0x30–0x35)
- Backward/negative jumps (heuristic detection of a negative relative offset after JCC)

Windows are scored and, depending on thresholds and interactive options, reported as HIGH / MED / LOW hints. The script produces a terminal table and writes a plain-text hints file.

Features
--------
- Lightweight Python implementation
- Human-friendly terminal tables (uses rich)
- Writes hints to output.txt for offline review
- Configurable verbosity via interactive prompts (include MED/LOW hints)

Requirements
------------
- Python 3.8+ (3.10/3.11 recommended)
- pip

Runtime dependency
- rich — used to render colorful tables in the terminal

Example requirements.txt (recommended)
```text
rich>=13.0.0
```

Installation
------------
Clone the repository and install dependencies:

```bash
git clone https://github.com/FullToolz/HexoRat.git
cd HexoRat

# optional: create virtualenv
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows (PowerShell)

# install runtime dependency
pip install -r requirements.txt
# or
pip install rich
```

If you prefer not to use a virtual environment, ensure you understand the implications for your global Python environment.

Usage
-----
Run the scanner from the command line. The script will prompt whether to include LOW / MED hints and will write results to output.txt:

```bash
# basic usage (run from repo root)
python HexoRat.py /path/to/target.bin
```

Behavior:
- Prompts:
  - "Include LOW level hints? [Y/N]" — whether to include low-confidence hints
  - "Include MED level hints? [Y/N]" — whether to include medium-confidence hints
- Output:
  - A terminal table summarizing detected hints (levels, offsets, patterns)
  - A file named output.txt containing hint lines like:
    [HIGH] 0x1234 — XOR loop (possible string decoder)

Programmatic usage:
```python
import HexoRat
HexoRat.main("binaries/sample.exe")
```

Notes about scanning:
- The heuristics are intentionally simple and tuned for speed; expect false positives.
- If scanning very large binaries, consider running on a copy or using streaming variants (not currently implemented).

Outputs
-------
- Terminal table rendered via rich.
- output.txt in the current working directory with one hint per line.

Development
-----------
If you plan to extend HexoRat:

- Keep the dependency list minimal; add any new runtime dependencies to requirements.txt.
- Add unit tests under tests/ for core functions (scoring, pattern detection).
- Use black and flake8 for formatting and linting.

Suggested developer commands:
```bash
pip install -r requirements-dev.txt   # if you add one
black .
flake8
pytest -q
```

Contributing
------------
Contributions are welcome. Typical workflow:
1. Fork the repository
2. Create a feature branch (git checkout -b feat/description)
3. Implement the change and add tests
4. Open a pull request with a clear description and rationale

When changing heuristics, include justification and notes on expected false positives.

License
-------
This repository includes a [LICENSE](LICENSE) file — consult it for license details.

Legal & Security
----------------
- Only analyze binaries you own or have explicit permission to analyze.
- Running untrusted binaries can be dangerous. Perform analysis in an isolated environment (VM/sandbox).
- The author/maintainers are not responsible for misuse.

Acknowledgements / Related
--------------------------
HexoRat is a focused heuristic tool meant to be complementary to disassemblers, debuggers, and other binary analysis tools. Use its hints to guide deeper manual or automated analysis.

If you'd like, I can:
- Add a pinned requirements.txt and open a PR with it.
- Add a CLI argument parser to skip interactive prompts (e.g., `--low / --med`),
- Add unit tests for the scoring functions and pattern detection.
