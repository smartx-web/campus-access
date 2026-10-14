"""B's workflow adapted to the shared storage contract during assisted repair."""
from .storage import nonblank

# Demonstration policy; replace with the campus-approved staff identifiers.
AUTHORIZED_STAFF = frozenset({'M01', 'M02'})


def approve_request(store, request_id, approved_by, authorized_staff=AUTHORIZED_STAFF):
    nonblank(approved_by, 'approved_by')
    if approved_by not in authorized_staff:
        raise ValueError('Approver is not an authorized staff identifier')
    return store.transition_request(request_id, 'approved', approved_by)


def issue_card(store, request_id):
    return store.transition_request(request_id, 'issued')


def return_card(store, request_id):
    return store.transition_request(request_id, 'returned')
