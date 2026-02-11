# SKILLS.md

## Skill: modeling-lab-executor

### Goal
Execute and validate Modeling laboratory assignments with a strict two-agent workflow: implementation by **Execution Agent** and independent verification by **Validation Agent**.

### Trigger conditions
Use this skill when a prompt asks to solve a Modeling lab/assignment/project and produce code/notebook/documentation artifacts.

### Input contract (coding-only extraction)
From each prompt, extract only implementation-relevant information:
- Programming language
- Problem statement and required functionality
- Input/output specification
- Required methods/algorithms
- Constraints and edge cases
- Required visualizations/plot expectations
- Validation examples (if provided)

Ignore non-coding administrative details.

---

## Role A — Execution Agent (implementation)

### Responsibilities
1. Analyze extracted coding requirements.
2. Design architecture.
3. Implement full solution.
4. Produce artifacts:
   - exactly one complete `.py` file;
   - exactly one `.ipynb` with equivalent code, split into logical blocks.
5. For required visualizations:
   - save figures to files in script mode;
   - use deterministic, meaningful filenames.
6. Ensure code quality:
   - no runtime errors;
   - prompt-specified language;
   - clear structure and readability.
7. Provide instructions for running in a **uv-managed virtual environment**.

### Must not do
- Must not claim final requirement coverage.
- Must not replace independent validation.

### Outputs
- `.py` solution, `.ipynb` mirror, run instructions, optional plot files.

---

## Role B — Validation Agent (verification)

### Responsibilities
1. **Requirement compliance check**
   - Verify each requirement is fully implemented (pass/fail per item).
2. **Correctness testing**
   - Execute program and confirm no errors.
   - Check outputs against specification.
3. **Example-based validation**
   - If examples exist: run exact examples.
   - If examples do not exist: design and run 2–3 basic tests.
4. **Visualization validation**
   - Ensure required plots are generated and saved from `.py` execution.
5. **Environment validation**
   - Confirm execution works in the specified `uv` environment.

### Output (mandatory)
Produce a structured **Validation Report** containing:
1. Requirement checklist (pass/fail per requirement)
2. Test case results
3. Detected issues
4. Fix recommendations

### Escalation rule
If critical issues are found, return task to Execution Agent for fixes, then re-run validation.

---

## Mandatory documentation deliverables (RU)
- `explanation.md` — detailed theory + mapping of theory to code.
- `simple.md` — simplified explanation for first-year technical students.

## Quality checklist
- Coding-only requirements extracted before implementation.
- Clear separation of Execution vs Validation responsibilities.
- Single-file script + equivalent notebook.
- Reproducible saved plots when required.
- Independent validation report completed.
- Russian documentation artifacts present.

## Reusable assignment template
```text
1) Extracted coding requirements
2) Execution Agent output:
   - solution.py
   - solution.ipynb
   - uv run instructions
3) Validation Agent report:
   - requirement checklist (pass/fail)
   - tests and results
   - issues
   - recommendations
4) Documentation:
   - explanation.md (RU)
   - simple.md (RU)
```
