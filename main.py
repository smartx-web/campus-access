
from workflow import approve_request, issue_card, return_card


def show_menu():
    print("\n===== CAMPUS ACCESS SYSTEM =====")
    print("1. View card requests")
    print("2. Approve a request")
    print("3. Issue a card")
    print("4. Return a card")
    print("5. Exit")


def view_requests(requests):
    if not requests:
        print("No card requests found.")
        return

    for request in requests:
        print(f"\nRequest ID: {request['id']}")
        print(f"Fellow ID: {request['fellow_id']}")
        print(f"Card Type: {request['card_type']}")
        print(f"Status: {request['status']}")
        print(f"Approved By: {request['approved_by']}")


def main():
    requests = [
        {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "visitor",
            "status": "requested",
            "approved_by": None
        }
    ]

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_requests(requests)

        elif choice == "2":
            request_id = input("Enter request ID: ").strip()
            approved_by = input("Enter approver ID: ").strip()

            try:
                approve_request(requests, request_id, approved_by)
                print("Request approved successfully.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "3":
            request_id = input("Enter request ID: ").strip()

            try:
                issue_card(requests, request_id)
                print("Card issued successfully.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "4":
            request_id = input("Enter request ID: ").strip()

            try:
                return_card(requests, request_id)
                print("Card returned successfully.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose 1-5.")


if __name__ == "__main__":
    main()
