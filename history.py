# reads in a csv file,
# for each investor, extract history of investments and their interests

import csv
import requests
from pyquery import PyQuery as pq
import time

csv_input_file = open('csv/sfangels1.csv')
angel_reader = csv.reader(csv_input_file)
csv_output_file = open('csv/sfangels1_output.csv', 'a')
angel_writer = csv.writer(csv_output_file, delimiter='\t')

output_rows = []
for row in angel_reader:
    profile_url = row[0]
    if 'http' not in profile_url:
        # just write headers for first row
        row.append('investments')
        row.append('interests')
        angel_writer.writerow(row)
        continue

    r = requests.get(profile_url)
    d = pq(r.content)
    company_name_elements = d('.company_name')
    companies_invested_in = []
    for company_name_element in company_name_elements:
        company_name = pq(company_name_element)('a').text()
        # company_url = pq(company_name_element)('a').attr('href')
        role_title = pq(company_name_element).next().next().text()
        if role_title == 'Investor':
            companies_invested_in.append(company_name)
    companies_invested_in_string = ', '.join(companies_invested_in)
    interests_elements = d('[data-field="tags_interested_markets"] > div.content > div.value').children()
    interests = ', '.join([interest.text_content() for interest in interests_elements])
    row.append(companies_invested_in_string.encode('ascii', 'ignore'))
    row.append(interests.encode('ascii', 'ignore'))
    print row
    angel_writer.writerow(row)
    csv_output_file.flush()
    time.sleep(1.5)
csv_output_file.close()