"""Engineer A's storage inspection CLI; Engineer B will provide the full menu."""
import argparse
import json
import sys
from campus_access import RequestStore


def main(argv=None):
    parser = argparse.ArgumentParser(description='Campus Access registration/storage CLI (Engineer A)')
    parser.add_argument('--file', default='requests.json')
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('create')
    create.add_argument('fellow_id')
    create.add_argument('card_type')
    view = commands.add_parser('view')
    view.add_argument('request_id')
    commands.add_parser('list')
    args = parser.parse_args(argv)
    store = RequestStore()
    try:
        try:
            store.load_requests(args.file)
        except FileNotFoundError:
            if args.command != 'create':
                raise
        if args.command == 'create':
            result = store.create_request(args.fellow_id, args.card_type)
            store.save_requests(args.file)
        elif args.command == 'view':
            result = store.get_request(args.request_id)
        else:
            result = store.list_requests()
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
