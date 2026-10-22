# Algorithm Analysis: Counting Steps — e-textbook on algorithm analysis

Mathematical analysis of nonrecursive (Lecture 4) and recursive (Lecture 5) algorithms, Levitin §2.3–2.5.
Interactive textbook with worked examples, quizzes, problems with solutions, glossary and sources.

**Open the textbook:** the GitHub Pages link of this repository (Settings → Pages). Three language versions:

| Language | Folder |
|---|---|
| Русский | `ru/` |
| Қазақша | `kk/` |
| English | `en/` |

The root `index.html` is a language chooser (it also redirects old `#page` links). Each version is one static page with
animations (sorting, Tower of Hanoi, Fibonacci call tree, loop grid), charts, and in-page answer checking with saved progress.
It needs no installation and works on a phone. Fonts are self-hosted (`fonts/`); formulas are typeset with MathJax, loaded from a CDN,
so an internet connection is needed.

## Code (`code/`)

| File | What it does |
|---|---|
| `empirical_tasks.py` | Operation counters for the empirical tasks E1 and E2; compares measured counts with the formulas. |
| `verify_answers.py` | Checks the closed forms and problem answers used in the textbook. |

```
python code/empirical_tasks.py 1          # Module 1
python code/empirical_tasks.py 2          # Module 2
python code/empirical_tasks.py 1 --plot   # also saves module1_plot.png (needs: pip install matplotlib)
python code/verify_answers.py
```

Each run ends with `ALL CHECKS PASSED` (or a summary for `verify_answers.py`).

## Task tracker

`tracker_Counting_Steps.xlsx` — task table: stage, task, owner, reviewer, status, comment.



## Group

Beiimbet Sansyzbay, Arunaz Makhabayeva, Nurbol Sairambay
