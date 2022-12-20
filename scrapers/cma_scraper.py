#!/usr/bin/env python
import argparse
import requests
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--position', type=int)
    parser.add_argument('-i', '--item-position', type=int)
    parser.add_argument('-s', '--stop-at-year', type=int)
    parser.add_argument('-q', '--stop-at-quarter', type=int)
    args = parser.parse_args()
    url = 'https://employersinfocmp.cma.gov.il/api/PublicReporting/GetPublicReports'
    payloads = []
    for year in range(2020, 2023):
        data = {
            "corporation": None,
            "fromYear": year,
            "fromQuarter": 1,
            "toYear": year,
            "toQuarter": 4,
            "reportFromDate": None,
            "reportToDate": None,
            "investmentName": None,
            "reportType": "71100075",
            "systemField": "300002",
            "statusReport": 1
        }
        payloads.append(data)

    for idx, payload in enumerate(payloads):
        print('idx', idx)
        print(payload['fromYear'], payload['toYear'])
        if args.stop_at_year and args.stop_at_year >= idx:
            break
        if args.position and args.position > idx:
            continue
        res = requests.post(url, data=payload)
        res_json = res.json()

        for idx_item, item in enumerate(res_json):
            if args.stop_at_quarter and args.stop_at_quarter >= idx_item:
                break
            if args.item_position and args.item_position > idx_item:
                continue
            elif args.item_position and args.item_position == idx_item:
                args.item_position = 0
            print('idx', idx, 'document', idx_item, item['DocumentId'])
            res = requests.get(
                f"https://employersinfocmp.cma.gov.il/api/PublicReporting/downloadFiles?IdDoc={item['DocumentId']}&extention=xlsx",
                headers={
                    "Accept": "application/json, text/plain, */*"
                }
                )
            with open(f"data/cma/{item['DocumentName']}-{item['ReportPeriodDesc']}-{item['Name']}.xlsx",
                      'wb') as f:
                f.write(res.content)


if __name__ == '__main__':
    main()
