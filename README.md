# Campus Access

Python standard-library command-line application for campus access cards. It creates requests, views individual records, approves, issues, returns, lists, saves, reloads and quits.

## Run

Python 3.10+; no packages or database required. From the repository root:

```sh
python main.py
# Optional alternative JSON file:
python main.py --file /path/to/requests.json
python -m unittest discover -s tests -v
python docs/learning-experiments.py
```

Choose a menu action 1–9. Create `F001` with card type `visitor`, approve A001 using `M01`, issue it, then return it. `student` and `staff` are also valid card types.

Changes stay in memory until Save or Save and quit. Startup loads the selected JSON file; first use starts empty only if the file does not exist. Malformed saved data causes a clear failure without overwriting it. Reload asks for confirmation before discarding unsaved changes. EOF/Ctrl+C attempts to save dirty data. Interactive quit-save failures keep the menu running for retry; a failed save after EOF/Ctrl+C reports failure and exits with status 1 because further input may be unavailable. Save frequently to limit loss if storage is unavailable.

## Approval policy and storage

`campus_access/workflow.py` defines the demonstration allowlist `M01`, `M02`. Confirm or replace these with real authorized campus staff identifiers before operational use. This is identifier validation, not password-based authentication. Workflow wrappers receive one shared `RequestStore`; they never mutate returned dictionaries. The guarded storage method enforces requested → approved → issued → returned. Returned is final.

Request fields: `id`, `fellow_id`, `card_type`, `status`, `approved_by`. IDs use ASCII digits, starting A001, and resume from the largest loaded ID. Copies protect live storage. JSON is validated fully before replacing memory; saves use a temporary file and atomic replacement. Use one process per data file. Loading an older snapshot restores that dataset, not a global historical ID ledger.

## Authorship and collaboration

Engineer A: Codex acting in that role. Engineer B's original workflow/menu/test work is preserved in branch `feature/engineer-b-workflow` (reviewed at `5d8f35a`). This repair was performed by Codex with the user's authorization: it integrates A's storage and adapts B's workflow/tests, expands the menu and adds authorization/CLI regression coverage. These edits are AI-assisted repair, not claimed as B's independent work.

- [Design contract](docs/design-decisions.md)
- [Repair explanations and reviewer checklist](docs/repair-handoff.md)
- [A AI verification log](docs/ai-learning-log.md)
- [B's original learning-log template](docs/engineer-b-learning-log.md), still requiring B's real results/reflections
- [Test evidence](docs/test-evidence.md)
- [A issue](https://github.com/smartx-web/campus-access/issues/1), [B issue](https://github.com/smartx-web/campus-access/issues/2)

The repair branch is `fix/engineer-b-integration`, based on main. A's earlier PR #3 remains open; do not merge it over the repaired main without reviewing its outdated menu/README. Partner reviews, genuine human learning cycles and final merged-main verification remain assessment requirements. After review/merge, run the tests again and record `git rev-parse HEAD`. No completed reciprocal review is claimed.
