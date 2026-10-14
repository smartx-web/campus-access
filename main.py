"""Campus Access command-line entry point."""
import argparse
from campus_access.cli import run_menu


def main():
    parser = argparse.ArgumentParser(description='Campus Access card requests')
    parser.add_argument('--file', default='requests.json', help='JSON save file')
    args = parser.parse_args()
    return run_menu(args.file)


if __name__ == '__main__':
    raise SystemExit(main())
