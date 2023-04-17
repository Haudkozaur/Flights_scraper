import requests
from bs4 import BeautifulSoup
import re
import PySimpleGUI as sg

sg.theme('DarkAmber')


# imie = 'Albert'
# nazwisko = 'Komański'
# athl = imie + " " + nazwisko
# print(athl)


class Favourite:
    def encode(self, first_last_name):
        self.first_last_name = first_last_name
        print(self.first_last_name)
        self.first_last_name = self.first_last_name.upper()
        print(self.first_last_name)
        self.first_last_name_encoded = self.first_last_name.encode(encoding='iso-8859-2')
        print(self.first_last_name)
        self.first_last_name_encoded = str(self.first_last_name_encoded).replace('\\x', '%')
        print(self.first_last_name_encoded)
        self.first_last_name_encoded = self.first_last_name_encoded.upper()
        self.first_last_name_encoded = str(self.first_last_name_encoded).replace("B'", "").replace("'", "")
        print(self.first_last_name_encoded)
        self.first_last_name_encoded_part = self.first_last_name_encoded.partition(" ")
        print(self.first_last_name_encoded_part)

    def find_in_PZLA(self):
        self.stats_website = f'https://statystyka.pzla.pl/baza/?file=Szukaj&zawodnik={self.first_last_name_encoded_part[2]}&zawodnik_imie={self.first_last_name_encoded_part[0]}'
        print(self.stats_website)
        self.athl_domtel_html = requests.get(self.stats_website)
        self.athl_domtel_html.encoding = 'utf-8'
        self.athl_domtel_html_text = self.athl_domtel_html.text
        self.stew = BeautifulSoup(self.athl_domtel_html_text, 'lxml')
        self.athl_domtel = ""
        for link in self.stew.find_all('a', class_='p1', href=True):
            self.athl_domtel = (link['href'])
            break
        self.athl_domtel = f'https://statystyka.pzla.pl/{self.athl_domtel.replace("..", "")}'
        print(self.athl_domtel)
        self.athl_number = re.findall('\d+', self.athl_domtel)
        self.athl_number.sort()
        self.athl_number = self.athl_number[-1]
        print(self.athl_number)
        with open("fav.txt", mode='a') as file:
            file.write(f'{self.first_last_name_encoded} {self.athl_number}\n')
        # winter
        self.athl_domtel_winter = f'{self.athl_domtel}&sezon_Z_L=Z'
        print(self.athl_domtel_winter)

    def get_empty_table(self):
        self.headings_list = ['competition', 'result', 'date', 'city', 'age group']
        self.layout = [
            [sg.InputText('athelete name', key='name')],
            [sg.InputText('athelete last name', key='last_name')],
            [sg.Button('Submit')],
            [sg.Button('Outdoor', visible=False), sg.Button('Indoor', visible=False)],
            [sg.Table(
                values=[],
                headings=self.headings_list,
                def_col_width=15,
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-TABLE-',
                row_height=35)]]

    def get_athl_site(self):

        self.athl_site_html = requests.get(self.athl_domtel)
        self.athl_site_html.encoding = 'iso-8859-2'
        self.athl_site_html_text = self.athl_site_html.text
        self.soup = BeautifulSoup(self.athl_site_html_text, 'lxml')
        self.table = self.soup.find('table', border=0, width="500", cellspacing=False, cellpadding=0, style=False)
        print(self.table)
        self.cols = self.table.find_all('tr')
        self.rows_list_full = []
        for i in range(3, len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for self.row in self.rows:
                self.row_text = self.row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            self.rows_list_full.append(self.rows_list)
        # winter
        self.athl_site_winter_html = requests.get(self.athl_domtel_winter)
        self.athl_site_winter_html.encoding = 'iso-8859-2'
        self.athl_site_winter_html_text = self.athl_site_winter_html.text
        self.soup_winter = BeautifulSoup(self.athl_site_winter_html_text, 'lxml')
        self.table_winter = self.soup_winter.find('table', border=0, width="500", cellspacing=False, cellpadding=0,
                                                  style=False)
        print(self.table_winter)
        self.cols_winter = self.table_winter.find_all('tr')
        self.rows_list_full_winter = []
        for i in range(3, len(self.cols_winter)):
            self.rows_winter = self.cols_winter[i].find_all('td')
            self.rows_list_winter = []
            for self.row in self.rows_winter:
                self.row_text_winter = self.row.text.strip().split()
                self.rows_list_winter.append(" ".join(self.row_text_winter))
            self.rows_list_full_winter.append(self.rows_list_winter)
        print(self.rows_list_full_winter)

        # self.layout = [
        #     [sg.InputText('athelete name', key='name')],
        #     [sg.InputText('athelete last name', key='last_name')],
        #     [sg.Button('Submit')],
        #     [sg.Table(
        #         values=self.rows_list_full,
        #         headings=self.headings_list,
        #         def_col_width=50,
        #         auto_size_columns=False,
        #         display_row_numbers=False,
        #         vertical_scroll_only=False,
        #         justification='center',
        #         num_rows=len(self.rows_list_full),
        #         key='-TABLE_UP-',
        #         row_height=35)]
        # ]

# athl = Favourite()
# athl.encode(athl)
# athl.find_in_PZLA()
# athl.get_athl_site()
