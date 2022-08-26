import concurrent.futures
import csv
import datetime
import logging
import os
import xml.etree.ElementTree as XML

import argparse
import codecs
import requests


API_URL = 'https://gemelnet.cma.gov.il/tsuot/ui/tsuotHodXML.aspx'

GEMELNET_PATH = 'data/gemelnet'

# Theses deserve a separate folder, since there can be >100K of them
GEMELNET_MONTHLY_PORTFOLIO_PATH = 'data/gemelnet-monthly-portfolios'

PENSIANET_PATH = 'data/pensianet'

logging.basicConfig(filename='scraper-gemelnet-log.log', encoding='utf-8')
logger = logging.getLogger(__name__)


def _parse_xml(xml):
    """Convert Gemelnet XML result to array of dict per <Row/>"""
    return [
        dict([(field.tag, field.text) for field in row])
        for row in xml.iter('Row')]


def _load_xml_monthly_portfolio(kupa_id, year, month):
    """Query Gemelnet for a kupa's monthly portfolio. Returns XML node."""
    period = '{:04d}{:02d}'.format(year, month)
    params = {
        'dochot': 1, 'sug': 4,
        'miTkfDivuach': period,
        'adTkfDivuach': period,
        'kupot': kupa_id
    }
    result = requests.get(API_URL, params=params)
    if result.status_code != 200:
        logger.warning(f"kupa: {kupa_id} at {year}-{month} wasn't saved")
        return None
    result.encoding = 'UTF-8'
    xml = XML.fromstring(result.text)
    return xml


def save_csv_monthly_portfolio(kupa_id, year, month):
    """Query Gemelnet for a kupa's monthly portfolio and save as a CSV file. Return file path."""
    result = _load_xml_monthly_portfolio(kupa_id, year, month)
    if result is not None:
        filepath = os.path.join(GEMELNET_MONTHLY_PORTFOLIO_PATH, '{}-{:04d}-{:02d}.csv'.format(kupa_id, year, month))
        with open(filepath, 'w') as outfile:
            # Help Windows detects UTF-8.
            outfile.write(str(codecs.BOM_UTF8, 'utf-8'))
            sheet = csv.writer(outfile)
            sheet.writerow(['קופה', 'תקופה', 'קוד', 'נכס', 'כמות'])
            pretty_month = '{:02d}/{:04d}'.format(month, year)
            for r in result:
                if r.tag != 'ROW':
                    continue
                try:
                    sheet.writerow([
                        kupa_id, pretty_month,
                        r['ID_NATUN'], r['SHM_NATUN'], r['ERECH_NATUN']])
                except Exception as ex:
                    logger.error(ex)
        return filepath


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--kupa_id', type=int)
    parser.add_argument('-y', '--year', type=int)
    parser.add_argument('-m', '--month', type=int)
    args = parser.parse_args()

    print('downloading...')
    kupot_data = []
    now = datetime.datetime.now()

    if args.kupa_id:
        kupot_data = [args.kupa_id]
    with open('data/kupot.csv') as kupot:
        csv_kupot = csv.reader(kupot)
        years = [year for year in range(1999, now.year + 1)]
        if args.year:
            years = [args.year]
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        if args.month:
            months = [args.month]
        for line in csv_kupot:
            if args.kupa_id and line[0] != args.kupa_id:
                continue
            for year in years:
                if year > now.year:
                    break
                for month in months:
                    if year >= now.year and month >= now.month:
                        break
                    kupot_data.append((line[0], year, month))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_kupot = (executor.submit(save_csv_monthly_portfolio, kupa_id, year, month) \
                  for kupa_id, year, month in kupot_data)
        for future in concurrent.futures.as_completed(future_kupot):
            print('saved', future.result())


if __name__ == '__main__':
    main()
