# Campus Access — AI Learning Log

**Engineer:** Engineer B  
**Project:** Campus Access  
**Responsibility:** Approval, card issuing, card returns, CLI and workflow testing

## Learning Cycle 1 — Understanding `ValueError` and Validation

**Question:** Why should the program reject a request that has already been approved?

**My initial understanding:** [Write what you understood before the experiment.]

**AI explanation:** `ValueError` is used when a function receives a value that is not allowed. Checking the current status before changing a request prevents invalid actions.

**Prediction:** If a request is already approved, trying to approve it again should raise a `ValueError`. Its existing information should remain unchanged.

**Experiment:**

```bash
python -m unittest discover -s tests -p "test_workflow.py" -k test_cannot_approve_twice -v
```

**Verification:** [Paste your actual test output here.]

**Decision:** [Explain whether the experiment confirmed your prediction.]

**Personal reflection:** [Explain in your own words why validation must happen before updating a dictionary.]

---

## Learning Cycle 2 — Understanding State Transitions

**Question:** Why can't a card be issued before approval?

**AI explanation:** A state machine controls which actions are allowed. Campus Access follows:

`requested → approved → issued → returned`

Skipping approval would break the workflow rules.

**Prediction:** Attempting to issue a card with status `requested` should raise a `ValueError`, and the status should remain `requested`.

**Experiment:**

```bash
python -m unittest discover -s tests -p "test_workflow.py" -k test_cannot_issue_before_approval -v
```

**Verification:** [Paste your actual test output here.]

**Decision:** [Record what you accepted or changed after testing.]

**Personal reflection:** [Explain why checking the status inside the function is important, even when the CLI has menu options.]

---

## Testing Evidence

Earlier, I ran the workflow test suite and obtained:

- Tests run: 8
- Passed: 8
- Failed: 0

The tests covered approval, blank approvers, repeated approval, issuing before approval, issuing returned cards, repeated returns, the complete workflow and unknown requests.

## Code Review — Engineer A

**Code reviewed:** Request registration, ID validation and JSON storage.

**AI-assisted observations:**

- Request IDs are validated using ASCII digits.
- Records are validated before being stored.
- Saving uses a temporary file and replacement.
- The integration between `RequestStore` and Engineer B's workflow needs verification.
- Approver authorization requirements need clarification.

**My own review findings:** [Record what you personally checked and what you discussed with Engineer A.]

**GitHub PR link:** [Add link.]

## Final Reflection

**What surprised me:** [Your answer.]

**One function I can explain without AI:** [Your answer.]

**One AI suggestion I accepted, improved or rejected:** [Your answer, with evidence.]

**What I learned from working with Engineer A:** [Your answer.]