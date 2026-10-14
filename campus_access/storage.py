"""Registration and transactional JSON storage owned by Engineer A."""

import json
import os
from pathlib import Path
import re
import tempfile


FIELDS = {"id", "fellow_id", "card_type", "status", "approved_by"}
CARD_TYPES = {"visitor", "student", "staff"}
STATUSES = {"requested", "approved", "issued", "returned"}


def nonblank(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value


def id_number(value):
    if not isinstance(value, str) or not re.fullmatch(r"A[0-9]{3,}", value):
        raise ValueError("Request ID must use A followed by ASCII digits, e.g. A001")
    number = int(value[1:])
    if number < 1 or value != f"A{number:03d}":
        raise ValueError("Request ID must be canonical and positive, e.g. A001")
    return number


def validate_record(record):
    if not isinstance(record, dict) or set(record) != FIELDS:
        raise ValueError("Each request must have exactly id, fellow_id, card_type, status, approved_by")
    id_number(record["id"])
    nonblank(record["fellow_id"], "fellow_id")
    if not isinstance(record["card_type"], str) or record["card_type"] not in CARD_TYPES:
        raise ValueError("card_type must be visitor, student or staff")
    if not isinstance(record["status"], str) or record["status"] not in STATUSES:
        raise ValueError("Invalid request status")
    if record["status"] == "requested":
        if record["approved_by"] is not None:
            raise ValueError("Requested records must have approved_by null")
    else:
        nonblank(record["approved_by"], "approved_by")
    return dict(record)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


class RequestStore:
    """Single-process owner of records; callers receive copies, never live dicts."""

    def __init__(self):
        self._requests = {}
        self._next_number = 1

    def create_request(self, fellow_id, card_type):
        record = validate_record({
            "id": f"A{self._next_number:03d}", "fellow_id": fellow_id,
            "card_type": card_type, "status": "requested", "approved_by": None,
        })
        self._requests[record["id"]] = record
        self._next_number += 1
        return dict(record)

    def get_request(self, request_id):
        id_number(request_id)
        if request_id not in self._requests:
            raise ValueError(f"Unknown request ID: {request_id}")
        return dict(self._requests[request_id])

    def list_requests(self):
        return [dict(record) for record in sorted(
            self._requests.values(), key=lambda record: id_number(record["id"]))]

    def transition_request(self, request_id, target_status, approved_by=None):
        """B's mutation boundary. B must authorize approvers before calling this."""
        current = self.get_request(request_id)
        next_states = {"requested": "approved", "approved": "issued", "issued": "returned"}
        if not isinstance(target_status, str) or next_states.get(current["status"]) != target_status:
            raise ValueError(f"Cannot transition {current['status']} to {target_status}")
        candidate = dict(current)
        if target_status == "approved":
            candidate["approved_by"] = nonblank(approved_by, "approved_by")
        elif approved_by is not None:
            raise ValueError("approved_by may only be supplied during approval")
        candidate["status"] = target_status
        candidate = validate_record(candidate)
        self._requests[request_id] = candidate
        return dict(candidate)

    def save_requests(self, path):
        """Replace destination only after complete serialization and fsync."""
        destination = Path(path)
        records = [validate_record(record) for record in self.list_requests()]
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                             dir=destination.parent, delete=False) as handle:
                temporary = handle.name
                json.dump(records, handle, indent=2, ensure_ascii=False, allow_nan=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, destination)
        finally:
            if temporary is not None and os.path.exists(temporary):
                os.unlink(temporary)

    def load_requests(self, path):
        """Validate into temporary memory; failures leave this store unchanged."""
        try:
            with open(path, encoding="utf-8") as handle:
                records = json.load(handle, object_pairs_hook=unique_object)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValueError(f"Invalid JSON file: {error}") from error
        if not isinstance(records, list):
            raise ValueError("JSON root must be a list of request records")
        candidate = {}
        for raw in records:
            record = validate_record(raw)
            if record["id"] in candidate:
                raise ValueError(f"Duplicate request ID: {record['id']}")
            candidate[record["id"]] = record
        next_number = max((id_number(key) for key in candidate), default=0) + 1
        self._requests = candidate
        self._next_number = next_number
