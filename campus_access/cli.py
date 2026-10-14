"""Interactive menu with explicit save/reload and recoverable storage errors."""
import json
from .storage import RequestStore
from .workflow import approve_request, issue_card, return_card

MENU = '''
===== CAMPUS ACCESS =====
1. Create request
2. View request
3. Approve request
4. Issue card
5. Return card
6. List requests
7. Save JSON
8. Reload JSON
9. Save and quit'''


def run_menu(path='requests.json', input_fn=input, output=print):
    store = RequestStore()
    try:
        store.load_requests(path)
    except FileNotFoundError:
        output('No saved file found. Starting a new dataset.')
    except (ValueError, OSError) as error:
        output(f'Cannot load saved data: {error}. File left unchanged.')
        return 1
    dirty = False
    while True:
        try:
            output(MENU)
            choice = input_fn('Choose 1-9: ').strip()
            if choice == '1':
                result = store.create_request(input_fn('Fellow ID: '), input_fn('Card type (visitor/student/staff): '))
                dirty = True
                output(json.dumps(result, indent=2))
            elif choice == '2':
                output(json.dumps(store.get_request(input_fn('Request ID: ')), indent=2))
            elif choice in {'3', '4', '5'}:
                request_id = input_fn('Request ID: ')
                if choice == '3':
                    result = approve_request(store, request_id, input_fn('Authorized approver ID: '))
                elif choice == '4':
                    result = issue_card(store, request_id)
                else:
                    result = return_card(store, request_id)
                dirty = True
                output(json.dumps(result, indent=2))
            elif choice == '6':
                output(json.dumps(store.list_requests(), indent=2))
            elif choice == '7':
                store.save_requests(path)
                dirty = False
                output('Saved.')
            elif choice == '8':
                if dirty and input_fn('Discard unsaved changes and reload? Type YES: ') != 'YES':
                    output('Reload cancelled; changes kept.')
                    continue
                store.load_requests(path)
                dirty = False
                output('Reloaded.')
            elif choice == '9':
                store.save_requests(path)
                output('Saved. Goodbye!')
                return 0
            else:
                output('Invalid option. Choose 1-9 and try again.')
        except (ValueError, OSError) as error:
            output(f'Error: {error}. Changes remain in memory; you can retry.')
        except (EOFError, KeyboardInterrupt):
            if dirty:
                try:
                    store.save_requests(path)
                except (ValueError, OSError) as error:
                    output(f'Exit save failed: {error}. Changes could not be saved; exiting with failure.')
                    # A closed input stream cannot offer an interactive retry.
                    # Return failure explicitly; never claim a successful safe save.
                    return 1
            output('Goodbye!')
            return 0
