# Campus Access — AI Learning Log

> Integration note (18 October 2026): imported from Engineer B’s branch at `32eaa82`. The first-person statements below are B’s submitted account, not independently verified human learning evidence. The eight-test output relates to B’s older standalone workflow; current integrated main has 25 tests. The displayed filtered experiment commands would select one test each, while the pasted output shows the whole eight-test suite, so B should add matching command/output evidence. His reflection describes the integrated RequestStore wrapper, although his branch still contains the older list-based implementation. A placeholder remains below for B to resolve. Review text in this file is not a submitted GitHub approval. See issue #6 for outstanding evidence.

**Engineer:** Engineer B
**Project:** Campus Access
**Responsibility:** Approval, card issuing, card returns, CLI and workflow testing

## Learning Cycle 1 — Understanding `ValueError` and Validation

**Question:** Why should the program reject a request that has already been approved?

**My initial understanding:**
At first, I understood that a request should only be approved once, but I did not fully understand why checking its current status was important. I learned that approving the same request twice could overwrite the original approver's information and make the records unreliable.

**AI explanation:** `ValueError` is used when a function receives a value that is not allowed. Checking the current status before changing a request prevents invalid actions.

**Prediction:** If a request is already approved, trying to approve it again should raise a `ValueError`. Its existing information should remain unchanged.

**Experiment:**

```bash
python3 -m unittest discover -s tests -p "test_workflow.py" -k test_cannot_approve_twice -v
```

**Verification:** [Paste your actual test output here.]
test_approve_request (test_workflow.TestWorkflow.test_approve_request) ... ok
test_blank_approver_is_rejected (test_workflow.TestWorkflow.test_blank_approver_is_rejected) ... ok
test_cannot_approve_twice (test_workflow.TestWorkflow.test_cannot_approve_twice) ... ok
test_cannot_issue_before_approval (test_workflow.TestWorkflow.test_cannot_issue_before_approval) ... ok
test_cannot_issue_returned_card (test_workflow.TestWorkflow.test_cannot_issue_returned_card) ... ok
test_cannot_return_twice (test_workflow.TestWorkflow.test_cannot_return_twice) ... ok
test_complete_workflow (test_workflow.TestWorkflow.test_complete_workflow) ... ok
test_unknown_request_is_rejected (test_workflow.TestWorkflow.test_unknown_request_is_rejected) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK

**Decision:**
I accepted the validation approach because a request should not be approved more than once. I learned that the program should check the current status before allowing any change.

**Personal reflection:**
Validation must happen before updating a dictionary because it protects the existing information. If the program updates the dictionary before checking the rules, invalid data could be saved. By checking first, the program can reject the operation without changing the request.

---

## Learning Cycle 2 — Understanding State Transitions

**Question:** Why can't a card be issued before approval?

**AI explanation:** A state machine controls which actions are allowed. Campus Access follows:

`requested → approved → issued → returned`

Skipping approval would break the workflow rules.

**Prediction:** Attempting to issue a card with status `requested` should raise a `ValueError`, and the status should remain `requested`.

**Experiment:**

```bash
python3 -m unittest discover -s tests -p "test_workflow.py" -k test_cannot_issue_before_approval -v
```

**Verification:**
test_approve_request (test_workflow.TestWorkflow.test_approve_request) ... ok
test_blank_approver_is_rejected (test_workflow.TestWorkflow.test_blank_approver_is_rejected) ... ok
test_cannot_approve_twice (test_workflow.TestWorkflow.test_cannot_approve_twice) ... ok
test_cannot_issue_before_approval (test_workflow.TestWorkflow.test_cannot_issue_before_approval) ... ok
test_cannot_issue_returned_card (test_workflow.TestWorkflow.test_cannot_issue_returned_card) ... ok
test_cannot_return_twice (test_workflow.TestWorkflow.test_cannot_return_twice) ... ok
test_complete_workflow (test_workflow.TestWorkflow.test_complete_workflow) ... ok
test_unknown_request_is_rejected (test_workflow.TestWorkflow.test_unknown_request_is_rejected) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK

**Decision:**
I accepted the state-transition approach because it prevents users from skipping important steps. The request must move through the correct statuses before a card can be returned.

**Personal reflection:**
Checking the status inside the function is important because the CLI is not the only way a function can be called. Someone could call the workflow function directly from another Python file or a test. The workflow must enforce the rules regardless of how the function is called.
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

**My own review findings:**
I reviewed the request registration, validation, and JSON storage implementation.

The code is well structured. I particularly like the input validation, duplicate ID checks, and use of temporary files to protect existing data during saves.

I have a few suggestions before integration:

Confirm how transition_request() will connect to Engineer B's approval, issuing, and return functions.
Clarify how authorized approvers should be validated.
Document or handle the case where the JSON destination directory does not exist.
Add integration tests covering the complete workflow and JSON persistence.
Overall, the implementation looks good. I recommend resolving the integration questions and verifying the combined functionality before merging.

**GitHub PR link:** [https://github.com/smartx-web/campus-access/pull/3]

## Final Reflection

**What surprised me:**
I was surprised that a small workflow function could depend on several important rules. I learned that writing a function is not only about making it work when the input is correct, but also about making sure it handles invalid operations safely.

**One function I can explain without AI:**
I can explain the issue_card() function.

```def issue_card(store, request_id):
    return store.transition_request(request_id, "issued")
```
The function receives the storage object and the request ID. It calls transition_request() to change the request status to issued.

The storage method checks whether the request is eligible for issuing. If the request has not been approved, the operation raises a ValueError.

**One AI suggestion I accepted, improved or rejected:**
I accepted the suggestion to use ValueError when a workflow operation is invalid.

I also accepted the approach of keeping status validation and updates inside RequestStore instead of repeating the same logic in different workflow functions.

My recorded workflow tests included successful checks for repeated approval, invalid issuing and returning.

**What I learned from working with Engineer A:**
I learned that teamwork requires clear responsibilities and agreement on how different parts of the program communicate.

Engineer A worked on request storage and validation, while I worked on approval, issuing, returning and workflow testing.

I learned that both parts must follow the same rules for the application to work correctly. I also learned the importance of reviewing another engineer's code and testing how our functions work together.
