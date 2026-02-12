---
name: report-writing
description: Generate a complete Russian-language laboratory report in LaTeX using a strict reusable template with fixed formatting and fixed title page content. Use when you need to create report.tex/report.pdf for modeling labs, keep the exact section structure from template.tex, include plots produced by .py scripts in section "Анализ результатов", use shared emblem.png from repository root, and store report files in labN/report/.
---

# Report Writing Skill

Follow this workflow exactly.

## 1) Collect required inputs
Determine the target lab folder first (`lab1/`, `lab2/`, ...).  
All report files must be placed in `labN/report/` only.

Read these files from `labN/` if they exist:
- `solution.py`
- `solution.ipynb`
- `comparison.csv`
- `validation_report.md`
- generated images (for example `trajectory_comparison.png`)
- repository root `emblem.png` (mandatory shared asset for title page)

If plot files are missing, run `solution.py` first so plots are generated before writing the report.

Before writing report files:
- create `labN/report/` if missing;
- keep generated artifacts in `labN/` as source of truth;
- copy (do not move) report resources into `labN/report/` when needed for LaTeX paths (for example required figures and optional `images/` folder);
- do not move `explanation.md` or `simple.md` into `labN/report/`.

## 2) Build report from strict template
Use `template.tex` from this skill as the base.
Preserve these structural elements:
- title page
- section headings
- overall section order and formatting
- do not change title-page formatting or text
- do not add placeholders on title page

Required section order:
1. `Цель работы`
2. `Постановка задачи`
3. `Теоретические основы`
4. `Программная реализация`
5. `Анализ результатов`
6. `Заключение`

## 3) Content rules
- Write in Russian.
- Keep academic style formal but simple: level of an intelligent first-year student.
- Keep theory grammatically correct and logically connected to the implementation.
- In `Анализ результатов`, always include all generated plots from `.py` execution.
- Insert figures from files (no screenshots).
- Keep references local to `labN/report/` for report assets (for example `trajectory_comparison.png` or `images/...`).
- Use shared root emblem for title page (`../../emblem.png` from `labN/report/`, or copied local asset if explicitly required by template constraints).

## 4) Figure policy
- All figures must be in `Анализ результатов`.
- Each figure must have `\caption{...}` and `\label{...}`.
- Use `\begin{figure}[H]` and `\centering`.
- Recommended width: `0.85\textwidth` to `0.95\textwidth`.

## 5) Program code section
In `Программная реализация`, include either:
- full implementation code with `minted`/`lstlisting`, or
- full file include via `\lstinputlisting{solution.py}`.

Mandatory rule: insert the implementation code **in full** (`solution.py` entirely), without omissions, truncation, or shortened fragments.
Prefer `\lstinputlisting{solution.py}` when the template allows it.
If `solution.py` remains in `labN/`, reference it from report folder with a relative path (for example `\lstinputlisting{../solution.py}`).

## 6) Output artifacts
Produce:
1. `labN/report/report.tex` (completed report)
2. `labN/report/report.pdf` (compiled via pdfLaTeX-compatible tool)
3. intermediate LaTeX artifacts in the same folder (`labN/report/`), if generated (`.aux`, `.log`, `.out`, etc.)
4. keep generated code outputs in `labN/`; if report needs them, create copies in `labN/report/` rather than moving originals

## 7) Compilation and validation
Compile with a pdfLaTeX-compatible pipeline. Preferred command:
- `cd labN/report && pdflatex -interaction=nonstopmode report.tex`

If bibliography is not used, one or two pdflatex passes are enough.

Verify after build:
- `labN/report/report.pdf` exists
- no broken image paths
- title page uses shared root `emblem.png` (or validated copied equivalent)
- all plots are present inside `Анализ результатов`

## 8) Fallback when LaTeX compiler is unavailable
If `pdflatex` is unavailable in the environment:
- still produce valid `labN/report/report.tex`
- report exact missing command/tool in the final status
- provide exact compile command for Overleaf/local TeX installation, keeping `labN/report/` as working folder
