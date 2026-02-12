# AGENTS.md

## Purpose
This repository is configured for completing laboratory assignments in the subject **Modeling**.

## Global rule before any implementation
1. **Extract coding-only requirements from the prompt first.**
   - Keep only implementation-relevant constraints (inputs, outputs, algorithms, language, edge cases, required artifacts).
   - Remove non-coding details (deadlines, report formatting, submission mechanics, grading bureaucracy, etc.).
2. **Confirm programming language from the prompt.**
   - The programming language for each lab is defined by the prompt.
3. **Store each lab in its own folder.**
   - Keep all files related to one lab (code, report, generated artifacts) inside that lab folder (for example: `lab1/`, `lab2/`).
   - If a lab folder does not exist yet, create it before generating any new files.
4. **Use shared and local assets consistently.**
   - Keep shared `emblem.png` in the repository root so all labs can use it.
   - Keep all code results (`.png`, `.csv`, and other generated artifacts) in the corresponding lab folder (`labN/`).
   - `explanation.md` and `simple.md` must always be in `labN/` (not inside `labN/report/`).
   - `labN/report/` must contain all files matching `report.*` and all assets used by `report.tex`; if an asset is generated in `labN/`, copy it to `labN/report/` when needed (do not move it out of `labN/`).
5. **Encoding and Cyrillic safety (mandatory).**
   - Save all text artifacts (`.py`, `.md`, `.tex`, `.csv`, `.ipynb` JSON) strictly in `UTF-8` without BOM.
   - Never write Russian/Cyrillic text through a non-UTF shell pipeline unless encoding is explicitly controlled.
   - When generating notebooks programmatically, write JSON with `encoding="utf-8"` and `ensure_ascii=False`.
   - If plots contain Russian labels/titles/legends, configure matplotlib fonts explicitly (for example, `DejaVu Sans`) and set `axes.unicode_minus=False`.
   - Before handoff, run a quick encoding sanity check: no mojibake fragments (for example, `вЂ`, `Ð`, `Ñ`) and no accidental `?` substitution in human-readable Russian text.

---

## Strict two-agent workflow (non-overlapping responsibilities)

### 1) Execution Agent
**Primary responsibility:** implementation only.

**Inputs:**
- Extracted coding requirements.
- Required language and assignment constraints.

**Tasks:**
1. Analyze extracted coding requirements.
2. Design solution architecture.
3. Implement full solution.
4. Produce required deliverables:
   - one runnable `.py` file with complete solution;
   - one `.ipynb` with the same code split into logical, well-structured blocks.
5. If visualizations are required:
   - save all plots/graphs to files in `.py` mode;
   - use meaningful, reproducible filenames.
6. Ensure implementation quality:
   - runs without errors;
   - uses specified language;
   - readable, structured, and maintainable.
7. Provide instructions to run in a **uv-managed virtual environment**.

**Explicit boundary:**
- The Execution Agent **must not perform final requirement-coverage validation**.
- The Execution Agent hands off artifacts to the Validation Agent.

**Outputs:**
- Implementation artifacts (`.py`, `.ipynb`, generated plots if required).
- Run instructions for `uv` environment.

### 2) Validation Agent
**Primary responsibility:** verification only (after Execution Agent completion).

**Inputs:**
- Artifacts and run instructions produced by Execution Agent.
- Extracted coding requirements.

**Tasks:**
1. **Requirement Compliance Check**
   - Verify every assignment item is implemented.
   - Detect missing or partially implemented requirements.
2. **Code Correctness Testing**
   - Run program and confirm error-free execution.
   - Validate outputs against assignment specification.
3. **Example-Based Validation**
   - If assignment includes examples: run exact samples and check correctness.
   - If no examples: design and run **2-3 basic test cases**.
4. **Visualization Validation**
   - Confirm required plots are generated.
   - Confirm `.py` execution saves figures to files (no interactive-only behavior).
   - Confirm Russian labels in generated figures are rendered as text, not `?` boxes/placeholders.
5. **Environment Validation**
   - Verify solution runs correctly inside the specified **uv environment**.
6. **Notebook encoding validation**
   - Execute the notebook end-to-end.
   - Confirm code cells, markdown cells, and printed outputs keep Cyrillic text readable (no `?` substitution).

**Outputs:**
- A structured validation report with:
  - requirement checklist (pass/fail per item),
  - test case results,
  - detected issues,
  - fix recommendations.

### 3) Feedback loop
- If critical issues are found by Validation Agent, return workflow to Execution Agent for corrections.
- Re-run Validation Agent checks after fixes.

---

## Documentation outputs (mandatory, in Russian)
- `explanation.md` - detailed theory, background concepts, and mapping theory to implementation.
- `simple.md` - same material in simpler language for a first-year technical student.

## Output checklist per lab
- [ ] Coding-only requirements extracted from prompt.
- [ ] Execution Agent produced one `.py` and one equivalent `.ipynb`.
- [ ] Plot files are saved from `.py` execution when required.
- [ ] Execution instructions for `uv` environment are provided.
- [ ] Validation Agent completed independent requirement-by-requirement verification.
- [ ] Validation report includes checklist, tests, issues, and recommendations.
- [ ] `explanation.md` written in Russian.
- [ ] `simple.md` written in Russian.
