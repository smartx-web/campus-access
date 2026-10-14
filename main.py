
from workflow import approve_request, issue_card, return_card


def show_menu():
    print("\n===== CAMPUS ACCESS SYSTEM =====")
    print("1. Create request ticket")
    print("2. View requests")
    print("3. Approve request")
    print("4. Issue card")
    print("5. Return card")
    print("6. Exit")


def main():
    store = RequestStore()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_request_ticket(store)

        elif choice == "2":
            for request in store.list_requests():
                print(request)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option or option not yet connected.")

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
