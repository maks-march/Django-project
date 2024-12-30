import pandas as pd
import sqlite3

import requests, csv
import xml.etree.ElementTree as ET

def parse_response(r):
    root = ET.fromstring(r.content).iter('*')
    for sitemap in root:
        children = list(sitemap)
        for child in children:
            xmlDict = {}
            child = list(child)
            xmlDict['CharCode'] = child[1].text
            xmlDict['VunitRate'] = child[5].text
            yield xmlDict
        break


def get_dates(year_from = 2000, year_to = 2025):
    date = "01"
    months = [str(x) if x > 9 else '0' + str(x) for x in range(1, 13)]
    years = [str(x) for x in range(year_from, year_to)]
    return ["/".join([date, month, year]) for year in years for month in months][:-1]

def write_currency_table():
    conn = sqlite3.connect('C:\\Users\\march\\Documents\\GitHub\\Django-project\\db.sqlite3')
    header = ('date', 'BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL')
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
    dates = get_dates()
    order_dictionary = {
        'date': 0, 'BYR': 1, 'USD': 2, 'EUR': 3, 'KZT': 4, 'UAH': 5, 'AZN': 6, 'KGS': 7, 'UZS': 8, 'GEL': 9
    }
    with (open('local_files/currency.csv', 'w', newline='') as f):
        csv.writer(f).writerow(header)
        for date in dates:
            row = [None] * 10
            response = parse_response(requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date))
            for dictionary in response:
                if dictionary['CharCode'] in header:
                    row[order_dictionary[dictionary['CharCode']]] = float(dictionary['VunitRate'].replace(',', '.'))
            row[0] = "-".join(reversed(date[3:].split('/')))
            csv.writer(f).writerow(row)

    currency_df = pd.read_csv('local_files/currency.csv', low_memory=False)
    currency_df.to_sql('currency', conn, index=False, if_exists='replace',
              dtype={'date': 'String', 'BYR': 'Real', 'USD': 'Real', 'EUR': 'Real', 'KZT': 'Real', 'UAH': 'Real', 'AZN': 'Real', 'KGS': 'Real', 'UZS': 'Real', 'GEL': 'Real'})


def get_salary(salary_from, salary_to, curr_coef):
    if pd.isna(salary_from) and pd.isna(salary_to):
        return None
    elif pd.isna(salary_from):
        return float(salary_to * curr_coef)
    elif pd.isna(salary_to):
        return float(salary_from * curr_coef)
    else:
        return float((salary_from+salary_to) / 2 * curr_coef)

def get_koef(currency, date, conn):
    if currency == 'RUR':
        return 1
    if pd.isna(currency):
        return None
    cursor = conn.execute(
        f"""
            SELECT {currency} 
            FROM 'currency'
            WHERE date = {date}
        """
    )
    for row in cursor:
        return row


def main():
    df = pd.read_csv('local_files/vacancies_2024.csv', low_memory = False)
    conn = sqlite3.connect('C:\\Users\\march\\Documents\\GitHub\\Django-project\\db.sqlite3')





    df = df.assign(
        date=lambda x: [x[:7] for x in df['published_at']]
        ).assign(
            id = lambda x: [x for x in range(1,len(df['published_at'])+1)]
        )
    df = df.assign(
            salary_average = lambda x:[
                get_salary(salary_from, salary_to, get_koef(salary_currency,date, conn))
                for (salary_from, salary_to, salary_currency, date) in zip(df['salary_from'], df['salary_to'], df['salary_currency'], df['date'])
            ]
        )
    df.to_sql('vacancies', conn, index=False, if_exists='replace',
              dtype={'name': 'String', 'key_skills': 'Real', 'salary_from': 'Real', 'salary_to': 'Real', 'salary_average': 'Real', 'salary_currency': 'Real', 'area_name': 'Real', 'published_at': 'Real', 'UZS': 'Real', 'GEL': 'Real'})


    print()

if __name__ == "__main__":
    # write_currency_table()
    main()