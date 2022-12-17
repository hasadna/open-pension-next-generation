#!/bin/python3

from openpyxl import load_workbook
from typing import NamedTuple

class ParsedReport(NamedTuple):
    date: int
    company: str
    route: str
    route_number: int

def parse_book(file):
    workbook = load_workbook(file)
    main_sheet = workbook['סכום נכסי הקרן']
    return ParsedReport(
        date = main_sheet['C1'].value,
        company = main_sheet['C2'].value,
        route = main_sheet['C3'].value,
        route_number = main_sheet['C4'].value,
    )
