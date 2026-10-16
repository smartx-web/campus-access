# Assisted repair for Engineer B

## What changed and why

- Removed main's `campus-access` gitlink. It referred to a nested repository instead of including Python source. The repair contains ordinary source files; no history was rewritten and B's original branch remains available.
- Included A's storage, schema checks and tests. One RequestStore now owns all records and the next ID.
- Adapted B's three workflow functions to call the guarded storage method. Mutating `store.list_requests()` cannot update the store because those records are copies. This was the central integration failure.
- Added explicit demonstration authorization for M01/M02. A nonempty string alone is not authorization. B should confirm the policy and explain why this does not authenticate a person.
- Replaced the hardcoded demo request with the full menu. Startup loads JSON, saves are explicit, quitting saves, and reload of dirty memory requires confirmation. No corrupt file is automatically replaced at startup.
- Added CLI and workflow regression tests. The original workflow tests were adapted rather than counted as newly independent B-authored tests. No compiled Python files are included in the repair tree.

## What the tests demonstrate

The CLI challenge test creates F001/A001 with requested/null, rejects early issue and blank approval, approves M01, issues, returns, rejects further returns/issues, saves/reloads, retries unexpected text, and restarts to create A002. Storage tests prove entire-record preservation, malformed JSON rejection and atomic failed-save protection. Additional menu tests prove corrupt startup refusal, failed reload preserving memory, failed quit-save retry, and EOF/Ctrl+C save behavior.

All 25 tests were run successfully on the repair before opening the PR. This is feature-branch evidence, not merged-main evidence. The initial B review previously reproduced unauthorized approval, loss on restart and copied-list integration failure; this repair addresses those findings. Human execution and review remain pending.

## B's review and learning tasks

1. Check out this branch and run `python3 -m unittest discover -s tests -v` yourself.
2. Explain why workflow functions must call `transition_request`, and why a returned copy cannot update live storage.
3. Test an unauthorized approver and compare all fields before/after. Test corrupt JSON using a disposable file.
4. Confirm the demonstration staff allowlist or propose the campus's actual policy.
5. Complete two real learning cycles in your log, including predictions, actual output, decisions and personal reflections; do not present templates as completed experiments.
6. Leave at least two meaningful review observations on the PR. Request changes if needed. Do not claim an approval that GitHub disallows for the same account.
7. After approved merge, rerun all tests from main, demonstrate the eight challenge cases and record the main SHA. Resolve earlier PR #3 as superseded only after reviewing the repair.

## Known limits

This is single-process JSON storage. Abrupt process termination outside handled EOF/Ctrl+C can lose unsaved changes. If EOF/Ctrl+C occurs while the filesystem cannot save, the program reports failure and exits nonzero rather than claiming a successful save. It cannot guarantee persistence to an unavailable filesystem. The identifier allowlist is not user authentication. Atomic file replacement does not provide full database transactions or concurrent-writer protection.
