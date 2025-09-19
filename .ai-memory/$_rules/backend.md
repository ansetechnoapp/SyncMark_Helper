# 🧠 Code Quality Standards
> **Goal:** Maintain a clean, stable, and scalable codebase.
---
- 🔹 Write a **test first**
- 🔹 Implement **only what's needed** to pass the test
## 🧭 4. Core Principles

# 🧠 Python Backend Code Quality Standards
> **Goal:** Maintain a clean, stable, and scalable Python codebase.
---
# Applies only to the scrappyodds project

## 📖 SQL Reference Source
The SQL reference source is a set of SQL files containing manually written, tested, and approved queries. For filter-related issues, always check that your code respects the SQL rules in `.ai-memory\sql\postgresql\corrected_sql_filtering_rules.sql`.
---
## ✅ 1. Syntax Error Prevention
- Use static analysis tools (e.g. Pylance, flake8) to catch errors before running code.
---
## 🧪 2. Testing Setup First
- Set up and run tests before developing new features.
- Use `pytest` and `pytest-asyncio` for unit and async tests.
---
## 🚀 3. Feature Development Workflow
1. Work on one feature at a time.
2. Break each feature into simple sub-tasks.
3. For each task:
   - Write a test first.
   - Implement only what's needed to pass the test.
   - Run the test.
   - If it passes, move to the next task.
   - If it fails, debug, fix, and retest.
4. Move to the next feature only after all tests pass.
---
## 🧭 4. Core Principles
- Single Responsibility: one task = one purpose
- Test Early, Test Often
- Iterate Until Success
- Keep the Codebase Stable
---
## 🧩 5. Problem Solving Strategy
Always break down problems into clearly defined tasks.
---
## 🧱 6. Task Breakdown
- Analyze: Understand goals and constraints
- Decompose: Sequence tasks, identify dependencies
- Plan: Estimate effort, define milestones
- Execute & Review: Track progress, validate outcomes, adjust as needed
---
## 🧬 7. Database Best Practices
- Use clear SQL naming conventions.
- For any schema change:
  - Analyze the impact
  - Ensure backward compatibility
  - Backup the database
- Always test changes before production.
- Document every change or migration in `docs/database/`.
---
## 🗑 8. Deletion Protocol
- Never delete files or folders directly.
- Move obsolete files to the `useless/` directory.
---
## 🧪 9. Testing Guidelines
- Organize tests in `tests/`, `__tests__/`, or next to components.
- Isolate the test environment.
- Reset test data between runs.
- Use `pytest` and `pytest-asyncio` for Python tests.
- Update tests whenever code changes.
- Document setup and expected results.
---
## 📚 10. MCP Tools
- Read `.ai-memory\$_rules\MCP.md` for essential MCP tools to speed up development.
---
## 📦 11. Package Management
- For frontend, use `pnpm` only (do not mix with npm/yarn).
- For Python backend, manage dependencies with `requirements.txt` and `pip`.
---
## 📝 12. Logging Guidelines
- Always check for a logging system before making changes.
- Evaluate its clarity and accessibility.
- If needed, implement a structured logging model (e.g. JSON).
- Centralize logs and make them self-descriptive.
- The goal: any developer can debug without documentation.
---
## 📚 13. Documentation Guidelines
- Organize docs in the `docs/` directory.
- Use a consistent structure and tone.
- Update docs with every feature or change.
---