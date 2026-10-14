
import unittest
from copy import deepcopy

from workflow import approve_request, issue_card, return_card


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.requests = [
            {
                "id": "A001",
                "fellow_id": "F001",
                "card_type": "visitor",
                "status": "requested",
                "approved_by": None,
            }
        ]

    def test_approve_request(self):
        result = approve_request(self.requests, "A001", "M01")

        self.assertEqual(result["status"], "approved")
        self.assertEqual(result["approved_by"], "M01")

    def test_blank_approver_is_rejected(self):
        original = deepcopy(self.requests)

        with self.assertRaises(ValueError):
            approve_request(self.requests, "A001", "   ")

        self.assertEqual(self.requests, original)

    def test_unknown_request_is_rejected(self):
        original = deepcopy(self.requests)

        with self.assertRaises(ValueError):
            approve_request(self.requests, "A999", "M01")

        self.assertEqual(self.requests, original)

    def test_cannot_approve_twice(self):
        approve_request(self.requests, "A001", "M01")
        original = deepcopy(self.requests)

        with self.assertRaises(ValueError):
            approve_request(self.requests, "A001", "M02")

        self.assertEqual(self.requests, original)

    def test_cannot_issue_before_approval(self):
        original = deepcopy(self.requests)

        with self.assertRaises(ValueError):
            issue_card(self.requests, "A001")

        self.assertEqual(self.requests, original)

    def test_complete_workflow(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")

        self.assertEqual(self.requests[0]["status"], "issued")

        return_card(self.requests, "A001")

        self.assertEqual(self.requests[0]["status"], "returned")

    def test_cannot_return_twice(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")

        original = deepcopy(self.requests)

        with self.assertRaises(ValueError):
            return_card(self.requests, "A001")

        self.assertEqual(self.requests, original)

    def test_cannot_issue_returned_card(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")

        original = deepcopy(self.requests)

        with self.assertRaises(ValueError):
            issue_card(self.requests, "A001")

        self.assertEqual(self.requests, original)


if __name__ == "__main__":
    unittest.main()
