from bs4 import BeautifulSoup
import csv, shutil, os
import urllib.request
from urllib.parse import quote

with open ('table.html', encoding='utf-8') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

csv_file = open('states.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)

for row in soup.find_all('tr'):
    texts = []
    for index, tdata in enumerate(row.find_all('td')):
        text = tdata.text
        if index == 0:
            text = text[:-4]
        texts.append(text.strip())

    csv_writer.writerow(texts)

csv_file.close()