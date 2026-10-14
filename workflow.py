# Approves a request
def approve_request(requests, request_id, approved_by):
    for request in requests:
        if request["id"] == request_id:
            if request["status"] != "requested":
                raise ValueError("Request cannot be approved")

            if not isinstance(approved_by, str) or not approved_by.strip():
                raise ValueError("Approver ID cannot be empty")

            request["approved_by"] = approved_by.strip()
            request["status"] = "approved"
            return request

    raise ValueError("Request not found")


# Issues an approved card
def issue_card(requests, request_id):
    for request in requests:
        if request["id"] == request_id:
            if request["status"] != "approved":
                raise ValueError("Request must be approved before issuing")

            approved_by = request["approved_by"]

            if not isinstance(approved_by, str) or not approved_by.strip():
                raise ValueError("Request has no valid approver")

            request["status"] = "issued"
            return request

    raise ValueError("Request not found")


# Returns an issued card
def return_card(requests, request_id):
    for request in requests:
        if request["id"] == request_id:
            if request["status"] != "issued":
                raise ValueError("Only issued cards can be returned")

            request["status"] = "returned"
            return request

    raise ValueError("Request not found")