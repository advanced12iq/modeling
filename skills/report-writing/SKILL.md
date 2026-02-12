---
name: report-writing
description: Generate a complete Russian-language laboratory report in LaTeX using a strict reusable template with fixed title page and a mandatory 5-part body structure. Use when you need to create report.tex/report.pdf for modeling labs, build section 5 from validation_report.md, use shared emblem.png from repository root, and store report files in labN/report/.
---

# Report Writing Skill

Follow this workflow exactly.

## 1) Collect required inputs
Determine the target lab folder first (`lab1/`, `lab2/`, ...).  
All report files must be placed in `labN/report/` only.

Read these files from `labN/` if they exist:
- `Sollution.md` (priority source for full code listing in report when present/required)
- `solution.py`
- `solution.ipynb`
- `comparison.csv`
- `validation_report.md` (mandatory source for section 5)
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
- title page;
- section headings;
- overall section order and formatting;
- do not change title-page formatting or text;
- do not add placeholders on title page.

Required report structure:
0. `Титульный лист`
1. `Постановка задачи`
2. `Исследовательский этап`
3. `Конструкторский этап`
4. `Технологический этап`
5. `Тестирование, измерения и выводы`

## 3) Content rules
- Write in Russian.
- Keep academic style formal but simple: level of an intelligent first-year student.
- Keep logic connected from постановка задачи to исследование, декомпозиция, аппробация, and final validation outcomes.
- In section `Тестирование, измерения и выводы`, use `validation_report.md` as the primary source.
- Section 5 must explicitly include:
  - requirements checklist (pass/fail),
  - test-case results,
  - detected issues,
  - fix/improvement recommendations,
  - final conclusions.
- If visualizations are required by the lab, insert figures from files (no screenshots) in relevant sections and keep references local to `labN/report/`.
- Use shared root emblem for title page (`../../emblem.png` from `labN/report/`, or copied local asset if explicitly required by template constraints).

## 4) Validation report fallback policy
`validation_report.md` is mandatory for a complete section 5.

If `validation_report.md` is missing:
- do not silently skip validation content;
- insert an explicit technical note in section 5 that the validation source file is missing and the section is incomplete.

## 5) Figure policy
- Use figures only when they are required by the assignment or needed to support measured outcomes.
- Each figure must have `\caption{...}` and `\label{...}`.
- Use `\begin{figure}[H]` and `\centering`.
- Recommended width: `0.85\textwidth` to `0.95\textwidth`.

## 6) Program code usage in report
If assignment/report requirements include code presence, include implementation without truncation:
- full implementation code with `minted`/`lstlisting`, or
- full file include via `\lstinputlisting{...}` / `\inputminted{...}`.

Strict rule for this repository:
- the **Технологический этап** section must contain the full project code (not a link-only mention).
- if `labN/Sollution.md` exists, include code **exactly from this file** in full.
- if `labN/Sollution.md` is missing but code listing is required, create `labN/Sollution.md` from `solution.py` (UTF-8), then include it.

Preferred include order:
1. `\inputminted[encoding=utf8]{python}{../Sollution.md}`
2. `\lstinputlisting[language=Python,inputencoding=utf8]{../Sollution.md}`
3. fallback with explicit non-UTF encoding only if source is truly non-UTF and cannot be normalized.

Before compiling, normalize code listing source to UTF-8 without BOM whenever possible.

## 7) Output artifacts
Produce:
1. `labN/report/report.tex` (completed report)
2. `labN/report/report.pdf` (compiled via pdfLaTeX-compatible tool)
3. intermediate LaTeX artifacts in the same folder (`labN/report/`), if generated (`.aux`, `.log`, `.out`, etc.)
4. keep generated code outputs in `labN/`; if report needs them, create copies in `labN/report/` rather than moving originals

## 8) Compilation and validation
Use the same PDF compilation tool as in this repository workflow:
- `C:\Users\kkras\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`

Run from `labN/report/` with the same flags:
- `cd labN/report && "C:\Users\kkras\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" -shell-escape -interaction=nonstopmode -halt-on-error report.tex`

Run compilation twice to stabilize references and table/figure links.

Verify after build:
- `labN/report/report.pdf` exists;
- no broken image paths;
- title page uses shared root `emblem.png` (or validated copied equivalent);
- section `Технологический этап` includes the full code listing from `Sollution.md` when required;
- section 5 contains all validation blocks from `validation_report.md` or explicit fallback note if source is missing.

## 9) Encoding and Cyrillic safety
- Save `.tex` and `.md` strictly in UTF-8 without BOM.
- Never pass Russian text through non-UTF pipelines without explicit encoding control.
- Before handoff, check there is no mojibake (`вЂ`, `Ð`, `Ñ`) and no accidental `?` replacement in human-readable Russian text.

## 10) Fallback when LaTeX compiler is unavailable
If the specified MiKTeX `pdflatex.exe` is unavailable in the environment:
- still produce valid `labN/report/report.tex`;
- report exact missing command/tool in the final status;
- provide an alternative compile command for Overleaf/local TeX installation, keeping `labN/report/` as working folder.
