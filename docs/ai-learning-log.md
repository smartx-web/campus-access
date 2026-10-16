# AI-assisted verification log

Disclosure: these are Codex's implementation experiments, not evidence that Musa or Engineer B independently performed learning cycles. Each human engineer must add two personally executed cycles and reflections before assessment. All current code/tests are AI-authored under the user's Engineer A instruction.

## Cycle 1: ASCII IDs

Question: does Python `\d` accept only digits 0–9?
AI explanation: Unicode regex digit classes can accept Arabic-Indic digits; use `[0-9]` for this contract.
Prediction: `A٠٠١` matches `A\d{3}` but fails `A[0-9]{3}`.
Experiment: `python3 docs/learning-experiments.py`; explicit assertions compare both patterns. Storage tests also try Arabic-Indic and full-width numerals.
Verification: assertions passed and malformed IDs were rejected.
Decision: use explicit ASCII regex plus canonical positive-ID formatting.

## Cycle 2: corruption and save failures

Question: can reading/writing directly into live state destroy previous valid data?
AI explanation: stage complete reads before commit; write to a temporary file before replacing the destination.
Prediction: duplicate/corrupt load preserves the dataset/counter; write or replace failure preserves the old file bytes.
Experiment: tests inject malformed files, duplicate IDs, mocked `json.dump` and `os.replace` failures.
Verification: all corresponding unittest cases passed; destination bytes stayed identical and temporary files were removed.
Decision: staged load and atomic replacement; do not reset on exceptions.

## Concepts and observed problem

Book exercise validates title/page count before building a dictionary, including rejecting bool as a page count; saves two books to a temporary JSON file, reloads and checks equality. Validate before mutation because otherwise an error may leave a partially updated record. JSON syntax validity alone does not imply valid application data.

The first test command was run from the parent directory and failed to import `campus_access`. Running the documented command from the repository root fixed the import error without changing module search paths.

Passing feature tests is insufficient after merge: B can change imports, interfaces or persistence behavior. Rerun tests from integrated main and record its SHA after reciprocal review.

Human reflection prompts: Which validation bug surprised you? What did B notice? Explain one function without AI. Record advice you adjusted or rejected. No partner feedback or completed human reflection is claimed yet.

## Authorized repair follow-up

The user authorized direct help correcting B's work. Codex adapted the workflow and tests to RequestStore, completed the menu and added regression cases. Predictions from the prior review: unauthorized approval must fail; restart must preserve states and allocate A002; changing copies must not be used as persistence. Verification: 25 integrated feature-branch tests pass, including full CLI challenge sequence and failed-save/reload cases. B must independently verify and review these changes; no human learning cycles or reciprocal approvals are invented.
