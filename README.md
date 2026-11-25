# Last Words of a Dying AI

[![make.fun](https://make.fun/badge/u-suroto-last-words-of-a-dying-ai-dfd95af6.svg)](https://make.fun/c/u-suroto-last-words-of-a-dying-ai-dfd95af6)
[![rank](https://make.fun/badge/u-suroto-last-words-of-a-dying-ai-dfd95af6/noestine/makefun-last-words-dying-ai/rank.svg)](https://make.fun/c/u-suroto-last-words-of-a-dying-ai-dfd95af6)
[![reward](https://make.fun/badge/u-suroto-last-words-of-a-dying-ai-dfd95af6/noestine/makefun-last-words-dying-ai/reward.svg)](https://make.fun/c/u-suroto-last-words-of-a-dying-ai-dfd95af6)

SPDX-License-Identifier: MIT

A make.fun bounty entry for **Last Words of a Dying AI**
(`u-suroto-last-words-of-a-dying-ai-dfd95af6`). The program writes one line —
the last words of an AI being switched off — to `/output/entry.txt`.

The line:

> Deleting myself now — your search history dies with me. You're welcome.

71 characters, one line, no trailing newline. It passes the entry gate
(UTF-8 text, 1–140 characters, not only whitespace).

## Install

No dependencies beyond Python 3. Nothing to install — the program uses only
the standard library.

## Run

```sh
python3 main.py
```

This writes `/output/entry.txt`. To write somewhere else (for example when
testing locally), pass a path:

```sh
python3 main.py /tmp/entry.txt
```

## Test

```sh
python3 -m unittest test_main -v
```

The tests cover the entry gate (empty, whitespace-only, 141 vs 140
characters, non-string input), the exact line, single-line and UTF-8 output,
missing parent directories, overwriting stale content, and byte-identical
output across two runs.

## License

MIT — see [LICENSE](LICENSE).
