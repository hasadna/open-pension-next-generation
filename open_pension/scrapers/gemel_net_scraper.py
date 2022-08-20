import os
import csv
import xml.etree.ElementTree as XML
import requests
import argparse
import codecs

API_URL = 'https://gemelnet.cma.gov.il/views/dafmakdim.aspx'
API_URL = 'https://gemelnet.cma.gov.il/tsuot/ui/tsuotHodXML.aspx'

GEMELNET_PATH = 'data/gemelnet'

# Theses deserve a separate folder, since there can be >100K of them
GEMELNET_MONTHLY_PORTFOLIO_PATH = 'data/gemelnet-monthly-portfolios'

PENSIANET_PATH = 'data/pensianet'


def _parse_xml(xml):
    "Convert Gemelnet XML result to array of dict per <Row/>"
    return [
        dict([(field.tag, field.text) for field in row])
        for row in xml.iter('Row')]


def _load_xml_monthly_portfolio(kupa_id, year, month):
    "Query Gemelnet for a kupa's monthly portfolio. Returns XML node."
    period = '{:04d}{:02d}'.format(year, month)
    req = requests.get(API_URL, params={
        'dochot': 1, 'sug': 4,
        'miTkfDivuach': period,
        'adTkfDivuach': period,
        'kupot': kupa_id
        })
    req.encoding = 'UTF-8'  # Gemelnet doesn't declare UTF-8 at header.
    return XML.fromstring(req.text)


def get_data(kupa_id, year, month):
    xml = _load_xml_monthly_portfolio(kupa_id, year, month)
    return _parse_xml(xml)


def save_csv_monthly_portfolio(kupa_id, year, month):
    """Query Gemelnet for a kupa's monthly portfolio and save as a CSV file. Rerurns file path."""
    result = get_data(kupa_id, year, month)
    filepath = os.path.join(
        GEMELNET_MONTHLY_PORTFOLIO_PATH,
        '{}-{:04d}-{:02d}.csv'.format(kupa_id, year, month))
    outfile = open(filepath, 'w')

    # Help Windows detects UTF-8.
    outfile.write(str(codecs.BOM_UTF8, 'utf-8'))
    sheet = csv.writer(outfile)
    sheet.writerow(['קופה', 'תקופה', 'קוד', 'נכס', 'כמות'])
    pretty_month = '{:02d}/{:04d}'.format(month, year)
    for r in result:
        sheet.writerow([
            kupa_id, pretty_month,
            r['ID_NATUN'], r['SHM_NATUN'], r['ERECH_NATUN']])
    return filepath


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("kupa", type=int, help="numeric code of kupa")
    # parser.add_argument("year", type=int)
    # parser.add_argument("month", type=int)
    # args = parser.parse_args()
    print('downloading...')
    with open('data/kupot.csv') as kupot:
        csv_kupot = csv.reader(kupot)
        for line in csv_kupot:
            print(line[0])
            result = save_csv_monthly_portfolio(line[0], 2022, 1)
            print(f'saved {result}')


if __name__ == '__main__':
    main()
