import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from campus_access import RequestStore
from campus_access.cli import run_menu


class MenuTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'requests.json'

    def run_inputs(self, values):
        iterator = iter(values)
        output = []
        def read(prompt):
            try:
                item = next(iterator)
            except StopIteration:
                raise EOFError
            if isinstance(item, BaseException):
                raise item
            return item
        return run_menu(self.path, read, output.append), '\n'.join(output)

    def test_challenge_board_and_restart(self):
        code, output = self.run_inputs(['1','F001','visitor','4','A001',
            '3','A001','','3','A001','M01','4','A001','5','A001',
            '5','A001','4','A001','unexpected','2','A001','6','7','8','9'])
        self.assertEqual(code, 0)
        self.assertIn('Invalid option', output)
        self.assertIn('Error:', output)
        self.assertEqual(json.loads(self.path.read_text())[0]['status'], 'returned')
        self.run_inputs(['1','F002','student','9'])
        self.assertEqual([r['id'] for r in json.loads(self.path.read_text())], ['A001','A002'])

    def test_corrupt_startup_is_not_overwritten(self):
        self.path.write_text('{broken')
        code, output = self.run_inputs(['9'])
        self.assertEqual(code, 1)
        self.assertIn('Cannot load', output)
        self.assertEqual(self.path.read_text(), '{broken')

    def test_corrupt_reload_preserves_live_data(self):
        store = RequestStore()
        store.create_request('F001', 'visitor')
        store.save_requests(self.path)
        def read(prompt):
            if prompt == 'Choose 1-9: ':
                self.path.write_text('{broken')
                return next(choices)
            raise AssertionError(prompt)
        choices = iter(['8','6','9'])
        output=[]
        self.assertEqual(run_menu(self.path, read, output.append), 0)
        self.assertTrue(any('A001' in text for text in output))
        self.assertEqual(json.loads(self.path.read_text())[0]['id'], 'A001')

    def test_failed_quit_save_retries(self):
        original = RequestStore.save_requests
        calls=[]
        def save(store, path):
            calls.append(path)
            if len(calls) == 1:
                raise OSError('simulated failure')
            return original(store, path)
        with patch.object(RequestStore, 'save_requests', save):
            code, output = self.run_inputs(['1','F001','visitor','9','9'])
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 2)
        self.assertIn('simulated failure', output)
        self.assertEqual(json.loads(self.path.read_text())[0]['id'], 'A001')

    def test_eof_and_interrupt_save_dirty_data(self):
        for exit_signal in [EOFError(), KeyboardInterrupt()]:
            with self.subTest(signal=type(exit_signal).__name__):
                self.path.unlink(missing_ok=True)
                code, _ = self.run_inputs(['1','F001','visitor',exit_signal])
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(self.path.read_text())[0]['id'], 'A001')

    def test_reload_requires_discard_confirmation(self):
        code, output = self.run_inputs(['1','F001','visitor','8','no','9'])
        self.assertEqual(code, 0)
        self.assertIn('Reload cancelled', output)
        self.assertEqual(len(json.loads(self.path.read_text())), 1)
