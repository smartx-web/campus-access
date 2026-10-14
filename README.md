# Campus Access

Python standard-library CLI project for campus access card requests. This branch delivers **Engineer A's registration and data safety layer**. Engineer B's authorized approval wrappers and full interactive menu are pending; this is not yet the complete assignment.

## Run Engineer A's CLI

Python 3.10+; no pip packages or database required. Run from the repository root:

```sh
python main.py create F001 visitor
python main.py view A001
python main.py list
python -m unittest discover -s tests -v
python docs/learning-experiments.py
```

Use `--file /path/to/requests.json` before the command for another data file. Each successful create loads existing data, validates the request and saves atomically. A missing file is initialized only for create; a corrupt file causes a clear error and is never replaced with empty data. Commands exit with code 1 on validation/storage failure. Default local data is ignored by Git.

## Interface for Engineer B

```python
from campus_access import RequestStore
store = RequestStore()
request = store.create_request('F001', 'visitor')
request = store.get_request('A001')
requests = store.list_requests()
# B checks M01 against the authorized staff allowlist BEFORE approval:
store.transition_request('A001', 'approved', approved_by='M01')
store.transition_request('A001', 'issued')
store.transition_request('A001', 'returned')
store.save_requests('requests.json')
store.load_requests('requests.json')
```

Records returned to callers are copies. Never modify private storage. Invalid operations raise `ValueError`; file errors raise `OSError`. Follow [the proposed design contract](docs/design-decisions.md).

## Collaboration and evidence

- Engineer A: Codex acting in that role; human learner identity/reflection pending.
- Engineer B: not assigned yet.
- A branch: `feat/1-request-validation`; B branch: `feat/2-access-workflow`.
- [A issue](https://github.com/smartx-web/campus-access/issues/1), [B issue](https://github.com/smartx-web/campus-access/issues/2).
- [AI verification log](docs/ai-learning-log.md), [test evidence](docs/test-evidence.md).

B should review A's PR with two substantive observations and run the tests; A addresses feedback before approval/merge. A then reviews B's separate substantive PR. No reciprocal review or merged-main validation is claimed. After integration, demonstrate all eight challenge cases, run the suite again, and record `git rev-parse HEAD`. The current tests are A/AI-authored, not B-authored.

Suggested local Git workflow:

```sh
git switch -c feat/2-access-workflow
# implement and test your own changes
git status
git add main.py campus_access tests docs README.md
git commit -m "feat: implement authorized card workflow"
git push -u origin feat/2-access-workflow
# open PR on GitHub; partner reviews; address feedback; merge after approval
git switch main
git pull --ff-only
python -m unittest discover -s tests -v
git rev-parse HEAD
```

Use one process per data file. Saves replace snapshots; no deletion or multi-process locking is provided.
