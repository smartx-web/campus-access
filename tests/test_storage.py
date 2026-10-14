import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from campus_access import RequestStore


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.store = RequestStore()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'requests.json'

    def test_creation_five_fields(self):
        self.assertEqual(self.store.create_request('F001', 'visitor'), {
            'id': 'A001', 'fellow_id': 'F001', 'card_type': 'visitor',
            'status': 'requested', 'approved_by': None})

    def test_invalid_creation_does_not_consume_id(self):
        for fellow, card in [('', 'visitor'), ('  ', 'staff'), (None, 'visitor'),
                             (1, 'student'), ('F1', 'other'), ('F1', []), ('F1', None)]:
            with self.subTest(fellow=fellow, card=card):
                with self.assertRaises(ValueError):
                    self.store.create_request(fellow, card)
                self.assertEqual(self.store.list_requests(), [])
        self.assertEqual(self.store.create_request('F1', 'staff')['id'], 'A001')

    def test_lookup_rejects_malformed_and_unknown_ids(self):
        self.store.create_request('F1', 'staff')
        for value in ['A000', 'A01', 'A0001', 'A٠٠١', 'A００１', ' A001', 'A002', None, 1]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.store.get_request(value)

    def test_reads_and_create_results_are_detached(self):
        result = self.store.create_request('F1', 'staff')
        result['status'] = 'returned'
        self.store.get_request('A001')['fellow_id'] = 'changed'
        self.store.list_requests()[0]['card_type'] = 'bad'
        self.assertEqual(self.store.get_request('A001')['status'], 'requested')
        self.assertEqual(self.store.get_request('A001')['fellow_id'], 'F1')
        self.assertEqual(self.store.get_request('A001')['card_type'], 'staff')

    def test_restart_id_and_large_id(self):
        self.store.create_request('F1', 'visitor')
        self.store.save_requests(self.path)
        restarted = RequestStore()
        restarted.load_requests(self.path)
        self.assertEqual(restarted.create_request('F2', 'student')['id'], 'A002')
        data = self.store.list_requests()
        data[0]['id'] = 'A999'
        self.path.write_text(json.dumps(data))
        restarted.load_requests(self.path)
        self.assertEqual(restarted.create_request('F3', 'staff')['id'], 'A1000')

    def test_invalid_load_preserves_data_and_counter(self):
        original = self.store.create_request('F1', 'visitor')
        missing = dict(original)
        del missing['approved_by']
        invalid_state = dict(original, status='lost')
        no_approver = dict(original, status='issued')
        unexpected = dict(original, extra=True)
        cases = ['', '{broken', '{}', json.dumps([missing]), json.dumps([original, original]),
                 json.dumps([invalid_state]), json.dumps([no_approver]), json.dumps([unexpected]),
                 '[{"id":"A001","id":"A002"}]']
        for raw in cases:
            with self.subTest(raw=raw):
                self.path.write_text(raw)
                with self.assertRaises(ValueError):
                    self.store.load_requests(self.path)
                self.assertEqual(self.store.list_requests(), [original])
        self.assertEqual(self.store.create_request('F2', 'staff')['id'], 'A002')

    def test_missing_file_preserves_memory(self):
        original = self.store.create_request('F1', 'visitor')
        with self.assertRaises(FileNotFoundError):
            self.store.load_requests(self.path)
        self.assertEqual(self.store.list_requests(), [original])

    def test_empty_array_is_valid_but_empty_file_is_not(self):
        self.path.write_text('[]')
        self.store.load_requests(self.path)
        self.assertEqual(self.store.create_request('F1', 'visitor')['id'], 'A001')

    def test_failed_replace_preserves_file_and_cleans_temporary(self):
        self.store.create_request('F1', 'visitor')
        self.store.save_requests(self.path)
        before = self.path.read_bytes()
        self.store.create_request('F2', 'staff')
        with patch('campus_access.storage.os.replace', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                self.store.save_requests(self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_failed_serialization_preserves_file(self):
        self.store.create_request('F1', 'visitor')
        self.store.save_requests(self.path)
        before = self.path.read_bytes()
        with patch('campus_access.storage.json.dump', side_effect=OSError('write failed')):
            with self.assertRaises(OSError):
                self.store.save_requests(self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_rejected_transitions_leave_every_field_unchanged(self):
        original = self.store.create_request('F1', 'visitor')
        for target, approver in [('issued', None), ('returned', None), ('approved', ''),
                                 ('approved', '  '), ('approved', 1), ('lost', None)]:
            with self.subTest(target=target, approver=approver):
                with self.assertRaises(ValueError):
                    self.store.transition_request('A001', target, approver)
                self.assertEqual(self.store.get_request('A001'), original)

    def test_mutation_boundary_full_workflow_and_final_state(self):
        self.store.create_request('F1', 'visitor')
        for target, approver in [('approved', 'M01'), ('issued', None), ('returned', None)]:
            self.assertEqual(self.store.transition_request('A001', target, approver)['status'], target)
        before = self.store.get_request('A001')
        for target in ['issued', 'returned', 'approved']:
            with self.assertRaises(ValueError):
                self.store.transition_request('A001', target)
            self.assertEqual(self.store.get_request('A001'), before)
        self.store.save_requests(self.path)
        restarted = RequestStore()
        restarted.load_requests(self.path)
        self.assertEqual(restarted.get_request('A001'), before)


if __name__ == '__main__':
    unittest.main()
