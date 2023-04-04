import requests
from bs4 import BeautifulSoup


class Scraper():

    def scrapowanie():
        print("scrapu, scrapu")


requested_html_text = requests.get(
    'https://hmps.domtel-sport.pl/?seria=3&dzien=2023-02-19&runda=1&konkurencja=M200&impreza=6')
requested_html_text.encoding = 'utf-8'
html_text = requested_html_text.text
# with open('HMP_2023.html', 'r', encoding='utf-8') as html_file:
soup = BeautifulSoup(html_text, 'lxml')
pretty_soup = soup.prettify()

rows = soup.find_all('a', href=True, onclick=True)

for row in rows:
    print(row.text)
