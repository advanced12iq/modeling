---
name: modeling-lab-executor
description: Execute Modeling labs with a strict two-agent workflow: Execution Agent implements artifacts (.py + .ipynb + plots + uv instructions), Validation Agent independently verifies requirements, tests, visual outputs, and environment.
---

# Skill: modeling-lab-executor

## Goal
Выполнять лабораторные работы по «Моделированию» с жёстким разделением ролей:
- **Execution Agent** — только реализация;
- **Validation Agent** — только независимая проверка.

## Trigger conditions
Используй навык, когда нужно решить лабораторную/практическую работу по моделированию и подготовить код, ноутбук, документацию и проверку.

## Input contract (coding-only extraction)
До реализации извлеки только кодовые требования:
- язык программирования;
- постановка задачи и требуемая функциональность;
- формат входных/выходных данных;
- требуемые методы/алгоритмы;
- ограничения и edge-cases;
- требования к визуализациям;
- примеры для проверки (если даны).

Игнорируй организационные и административные детали, не влияющие на код.

## Role A — Execution Agent (implementation only)

### Responsibilities
1. Проанализировать извлечённые кодовые требования.
2. Спроектировать решение.
3. Реализовать полное решение.
4. Подготовить артефакты:
   - ровно один исполняемый `.py`;
   - ровно один эквивалентный `.ipynb` (логически разбитый по блокам).
5. При необходимости визуализаций:
   - сохранять графики в файлы при запуске `.py`;
   - использовать воспроизводимые и осмысленные имена файлов.
6. Обеспечить качество:
   - запуск без ошибок;
   - соблюдение требуемого языка;
   - читаемость и структурированность.
7. Дать инструкции запуска в **uv-managed virtual environment**.

### Boundary
- Не выполнять финальную проверку покрытия требований.
- Передать артефакты Validation Agent.

### Outputs
- `solution.py`, `solution.ipynb`, файлы графиков (если нужны), инструкция запуска через `uv`.

## Role B — Validation Agent (verification only)

### Responsibilities
1. **Requirement Compliance Check**
   - Проверить каждый пункт требований (pass/fail).
2. **Code Correctness Testing**
   - Запустить программу и подтвердить отсутствие ошибок.
   - Проверить соответствие выходов спецификации.
3. **Example-Based Validation**
   - Если есть примеры — проверить точные примеры.
   - Если примеров нет — выполнить 2–3 базовых теста.
4. **Visualization Validation**
   - Подтвердить генерацию требуемых графиков.
   - Подтвердить сохранение графиков именно из `.py` запуска.
5. **Environment Validation**
   - Подтвердить работу в указанной `uv`-среде.

### Mandatory validation report
Подготовить структурированный отчёт проверки:
1. Чеклист требований (pass/fail по каждому пункту)
2. Результаты тестов
3. Найденные проблемы
4. Рекомендации по исправлению

### Escalation loop
Если найдены критичные проблемы, вернуть задачу Execution Agent, затем повторить валидацию.

## Mandatory documentation (RU)
- `explanation.md` — подробная теория и связь теории с реализацией.
- `simple.md` — упрощённое объяснение для первокурсника технического направления.

## Quality checklist
- [ ] Кодовые требования извлечены до реализации.
- [ ] Роли Execution/Validation разделены.
- [ ] Подготовлены один `.py` и один эквивалентный `.ipynb`.
- [ ] Графики сохраняются из `.py` (если требуются).
- [ ] Есть инструкции запуска через `uv`.
- [ ] Выполнена независимая валидация с отчётом.
- [ ] `explanation.md` на русском.
- [ ] `simple.md` на русском.

## Reusable output template
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
