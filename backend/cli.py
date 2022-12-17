#!/bin/python3

import argparse
from parser import parse_book

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'parse-sheets',
        description = 'Fetches the spreadsheets and parses them',
    )
    actions = parser.add_subparsers(title="actions", dest='action')

    single_file = actions.add_parser("file", help="Parse a specific file")
    single_file.add_argument("file", type=argparse.FileType('rb'), help="The file to parse")
    single_file.add_argument("-n","--dryrun", action='store_true')

    actions.add_parser("website", help="Fetch files from the website")

    args = parser.parse_args()
    return args

def parse_file(file, dryrun:bool):
    # Parse the workbook
    parsed = parse_book(file)
    if dryrun:
        print(parsed)

def main():
    args = parse_args()
    if args.action == 'file':
        parse_file(args.file, dryrun=args.dryrun)
    else:
        raise Exception("dont know how")

main()
