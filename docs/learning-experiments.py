"""Unrelated book exercises plus verified Unicode validation experiment."""
import json
from pathlib import Path
import re
import tempfile


def validate_book(title, pages):
    if not isinstance(title, str) or not title.strip():
        raise ValueError('title must be nonempty')
    if type(pages) is not int or pages <= 0:
        raise ValueError('pages must be a positive integer')
    return {'title': title, 'pages': pages}


books = [validate_book('Book One', 20), validate_book('Book Two', 40)]
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / 'books.json'
    with path.open('w') as file:
        json.dump(books, file)
    with path.open() as file:
        assert json.load(file) == books
for title, pages in [('', 20), ('Bad', True), ('Bad', 0)]:
    try:
        validate_book(title, pages)
    except ValueError:
        pass
    else:
        raise AssertionError('invalid book accepted')
assert re.fullmatch(r'A\d{3}', 'A٠٠١') is not None
assert re.fullmatch(r'A[0-9]{3}', 'A٠٠١') is None
print('Book validation, temporary JSON round-trip and ASCII-digit experiments passed.')
