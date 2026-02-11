# AGENTS.md

## Purpose
This repository is configured for completing laboratory assignments in the subject **Modeling**.

## Global rule before any implementation
1. **Extract coding-only requirements from the prompt first.**
   - Keep only implementation-relevant constraints (inputs, outputs, algorithms, language, edge cases, required artifacts).
   - Remove non-coding details (deadlines, report formatting, submission mechanics, grading bureaucracy, etc.).
2. **Confirm programming language from the prompt.**
   - The programming language for each lab is defined by the prompt.

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
   - If no examples: design and run **2–3 basic test cases**.
4. **Visualization Validation**
   - Confirm required plots are generated.
   - Confirm `.py` execution saves figures to files (no interactive-only behavior).
5. **Environment Validation**
   - Verify solution runs correctly inside the specified **uv environment**.

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
- `explanation.md` — detailed theory, background concepts, and mapping theory to implementation.
- `simple.md` — same material in simpler language for a first-year technical student.

## Output checklist per lab
- [ ] Coding-only requirements extracted from prompt.
- [ ] Execution Agent produced one `.py` and one equivalent `.ipynb`.
- [ ] Plot files are saved from `.py` execution when required.
- [ ] Execution instructions for `uv` environment are provided.
- [ ] Validation Agent completed independent requirement-by-requirement verification.
- [ ] Validation report includes checklist, tests, issues, and recommendations.
- [ ] `explanation.md` written in Russian.
- [ ] `simple.md` written in Russian.
