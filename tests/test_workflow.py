"""B's original workflow cases adapted to RequestStore; repair adds authorization."""
import unittest
from campus_access import RequestStore
from campus_access.workflow import approve_request, issue_card, return_card


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.store = RequestStore()
        self.store.create_request('F001', 'visitor')

    def rejected(self, action, *args):
        before = self.store.list_requests()
        with self.assertRaises(ValueError):
            action(self.store, *args)
        self.assertEqual(self.store.list_requests(), before)

    def test_approve(self):
        self.assertEqual(approve_request(self.store, 'A001', 'M01')['approved_by'], 'M01')
        self.assertEqual(self.store.get_request('A001')['status'], 'approved')

    def test_blank_and_unauthorized(self):
        for approver in ['', '  ', None, 'NOT_AUTHORIZED']:
            self.rejected(approve_request, 'A001', approver)

    def test_unknown_and_malformed(self):
        for request_id in ['A999', 'A٠٠١', None, 'A01']:
            self.rejected(approve_request, request_id, 'M01')
            self.rejected(issue_card, request_id)
            self.rejected(return_card, request_id)

    def test_no_second_approval(self):
        approve_request(self.store, 'A001', 'M01')
        self.rejected(approve_request, 'A001', 'M02')

    def test_no_early_issue_or_return(self):
        self.rejected(issue_card, 'A001')
        self.rejected(return_card, 'A001')
        approve_request(self.store, 'A001', 'M01')
        self.rejected(return_card, 'A001')

    def test_full_workflow(self):
        approve_request(self.store, 'A001', 'M01')
        issue_card(self.store, 'A001')
        return_card(self.store, 'A001')
        self.assertEqual(self.store.get_request('A001')['status'], 'returned')
        self.assertEqual(self.store.get_request('A001')['approved_by'], 'M01')

    def test_returned_is_final(self):
        self.test_full_workflow()
        self.rejected(return_card, 'A001')
        self.rejected(issue_card, 'A001')
        self.rejected(approve_request, 'A001', 'M02')
