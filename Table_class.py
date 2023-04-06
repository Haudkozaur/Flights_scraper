import requests
from bs4 import BeautifulSoup

# requested_html = requests.get(
#     'https://hmps.domtel-sport.pl/?seria=0&runda=3&konkurencja=Mt&dzien=2023-02-19&impreza=6')


class Table:
    def __init__(self, url):
        self.html = url
        self.html.encoding = 'utf-8'
        self.html_text = self.html.text
        self.soup = BeautifulSoup(self.html_text, 'lxml')
        self.table = self.soup.find('table', class_='Listy')

    def get_headers(self):
        self.cols = self.table.find_all('tr')
        self.headers_div = self.cols[0].find_all('td')
        self.headers_list = []
        for self.header in self.headers_div:
            self.header_text = self.header.text.strip().split()
            self.headers_list.append(" ".join(self.header_text))
        # self.headers_list.remove('')
        print(self.headers_list)


    def get_rows(self):
        self.rows_list_full=[]
        for i in range(1,len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for self.row in self.rows:
                self.row_text = self.row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            # for j in range(0,len(self.rows_list)-3):
            #     if self.rows_list[j]=='':
            #         self.rows_list.remove('')
            self.rows_list_full.append(self.rows_list)
        for i in range(0,len(self.rows_list_full)):
            print(self.rows_list_full[i])
# event_results = Table(requested_html)
# event_results.get_headers()
# event_results.get_rows()
