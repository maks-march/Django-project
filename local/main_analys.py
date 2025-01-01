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


def get_salary(salary_from, salary_to, salary_currency, date, conn):
    curr_coef = get_koef(salary_currency, date, conn)
    if pd.isna(salary_from) and pd.isna(salary_to):
        return salary_from
    elif pd.isna(salary_from):
        return float(salary_to * curr_coef)
    elif pd.isna(salary_to):
        return float(salary_from * curr_coef)
    else:
        return float((salary_from+salary_to) / 2 * curr_coef)

def get_koef(currency, date, conn):
    if currency == 'RUR' or pd.isna(currency):
        return 1
    cursor = conn.execute(
        f"""
            SELECT {currency}
            FROM 'currency'
            WHERE date = '{date}'
        """
    )
    for row in cursor:
        if row[0] == None:
            return 1
        else:
            return row[0]

def write_vacancies(conn):
    df = pd.read_csv('local_files/vacancies_2024.csv', low_memory=False)
    df = df.assign(
        date=lambda x: [x[:7] for x in df['published_at']]
    ).assign(
        id=lambda x: [x for x in range(1, len(df['published_at']) + 1)]
    )

    df = df.assign(
        salary_average=lambda x: [
            get_salary(salary_from, salary_to, salary_currency, date, conn)
            for (salary_from, salary_to, salary_currency, date) in
            zip(df['salary_from'], df['salary_to'], df['salary_currency'], df['date'])
        ]
    )
    df = df[df['salary_average'] < 10000000]
    df.to_sql('vacancies', conn, index=False, if_exists='append',
              dtype={'id': 'Int', 'name': 'String', 'key_skills': 'String', 'salary_from': 'Real', 'salary_to': 'Real',
                     'salary_average': 'Real', 'salary_currency': 'String', 'area_name': 'String', 'published_at': 'String'})

def write_skills(conn):

    dictionary = {}
    cursor = conn.execute(
        f"""
            SELECT key_skills, name
            FROM 'vacancies'
            WHERE key_skills != '' AND (instr(name, 'C++') OR instr(name, ' C '))
        """
    )

    for row in cursor:
        if str(row[0]).isnumeric():
            continue
        value = [y for x in row[0].lower().split('\n') for y in x.split(', ')]
        for skill in value:
            if skill == '':
                continue
            if skill in dictionary.keys():
                dictionary[skill] += 1
            else:
                dictionary[skill] = 1

    df = pd.DataFrame({'name': dictionary.keys(), 'count': dictionary.values()})

    # df.to_sql('skills', conn, index=False, if_exists='append',
    #           dtype={'name': 'String', 'count': 'Int'})
    df.to_sql('skills_filtered', conn, index=False, if_exists='append',
              dtype={'name': 'String', 'count': 'Int'})

def write_years(conn):
    dictionary_count = {}
    dictionary_avg = {}
    cursor = conn.execute(
        f"""
    		SELECT date, SUM(salary_average), COUNT(date)
    		FROM 'vacancies'
            WHERE instr(name, 'C++') OR instr(name, ' C ')
    		GROUP BY date
    	"""
    )

    for row in cursor:
        if row[0][:4] in dictionary_count.keys():
            if row[1] != None:
                dictionary_avg[row[0][:4]] += row[1]
            dictionary_count[row[0][:4]] += row[2]
        else:
            if row[1] != None:
                dictionary_avg[row[0][:4]] = row[1]
            else:
                dictionary_avg[row[0][:4]] = 0
            dictionary_count[row[0][:4]] = row[2]

    for key in dictionary_count.keys():
        dictionary_avg[key] = round(dictionary_avg[key]/dictionary_count[key], 2)

    df = pd.DataFrame({'year': dictionary_avg.keys(), 'average_salary': dictionary_avg.values(), 'count': dictionary_count.values()})
    df.to_sql('years_filtered', conn, index=False, if_exists='append',
              dtype={'year': 'String', 'average_salary': 'Real', 'count': 'Int'})

def write_cities(conn):
    dictionary_count = {}
    dictionary_avg = {}
    cursor = conn.execute(
        f"""
    		SELECT area_name, SUM(salary_average), COUNT(date)
    		FROM 'vacancies'
            WHERE area_name != '' AND (instr(name, 'C++') OR instr(name, ' C '))
    		GROUP BY date
    	"""
    )

    for row in cursor:
        if row[0] in dictionary_count.keys():
            if row[1] != None:
                dictionary_avg[row[0]] += row[1]
            dictionary_count[row[0]] += row[2]
        else:
            if row[1] != None:
                dictionary_avg[row[0]] = row[1]
            else:
                dictionary_avg[row[0]] = 0
            dictionary_count[row[0]] = row[2]

    summary = sum(dictionary_count.values())
    for key in dictionary_count.keys():
        dictionary_avg[key] = round(dictionary_avg[key]/dictionary_count[key], 2)
        dictionary_count[key] = round(100*dictionary_count[key]/summary, 4)

    df = pd.DataFrame({'name': dictionary_avg.keys(), 'average_salary': dictionary_avg.values(), 'proportion': dictionary_count.values()})
    df.to_sql('cities_filtered', conn, index=False, if_exists='append',
              dtype={'name': 'String', 'average_salary': 'Real', 'proportion': 'Int'})

def main():
    conn = sqlite3.connect('C:\\Users\\march\\Documents\\GitHub\\Django-project\\db.sqlite3')
    # write_currency_table()
    # write_vacancies(conn)
    # write_skills(conn)
    # write_cities(conn)
    # write_years(conn)

    print('finally!!!')

if __name__ == "__main__":
    main()