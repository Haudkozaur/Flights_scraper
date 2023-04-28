import re
import PySimpleGUI as sg
from request_func import get_request
from Add_To_Favourites import create_hints_lists


class Favourite:
    def encode(self, first_last_name):
        self.first_last_name = first_last_name
        self.first_last_name = self.first_last_name.upper()
        self.first_last_name_encoded = self.first_last_name.encode(encoding='iso-8859-2')
        self.first_last_name_encoded = str(self.first_last_name_encoded).replace('\\x', '%')
        self.first_last_name_encoded = self.first_last_name_encoded.upper()
        self.first_last_name_encoded = str(self.first_last_name_encoded).replace("B'", "").replace("'", "")
        self.first_last_name_encoded_part = self.first_last_name_encoded.partition(" ")

    def find_in_PZLA(self):
        self.stew = get_request(
            f'https://statystyka.pzla.pl/baza/?file=Szukaj&zawodnik={self.first_last_name_encoded_part[2]}&zawodnik_imie={self.first_last_name_encoded_part[0]}',
            'utf-8')
        for link in self.stew.find_all('a', class_='p1', href=True):
            self.athl_domtel = (link['href'])
            break
        self.athl_domtel = f'https://statystyka.pzla.pl/{self.athl_domtel.replace("..", "")}'
        print(self.athl_domtel)
        self.athl_number = re.findall('\d+', self.athl_domtel)
        self.athl_number.sort()
        self.athl_number = self.athl_number[-1]
        print(self.athl_number)
        # with open("fav.txt", mode='a') as file:
        #     file.write(f'{self.first_last_name_encoded} {self.athl_number}\n')
        # winter
        self.athl_domtel_winter = f'{self.athl_domtel}&sezon_Z_L=Z'
        print(self.athl_domtel_winter)

    def get_empty_table(self):
        self.headings_list = ['competition', 'result', 'date', 'city', 'age group']
        self.menu = ['menu', create_hints_lists()]
        self.second_tab_layout = [
            [sg.Text("Enter athletes data to check his/her PR's ")],
            [sg.InputText('athlete name', key='name'),
             sg.ButtonMenu('Choose from Favourites', self.menu, key='-tab_menu-', size=[20, 1])],
            [sg.InputText('athlete last name', key='last_name'),
             sg.Button('Add to Favourites', key='-add_athl1-', size=[18, 1])],
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
                row_height=35,
                enable_events=True)]]

    def get_athl_site(self):
        self.soup = get_request(self.athl_domtel, 'iso-8859-2')
        self.table = self.soup.find('table', border=0, width="500", cellspacing=False, cellpadding=0, style=False)
        self.cols = self.table.find_all('tr')
        self.rows_list_full = []
        for i in range(3, len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for row in self.rows:
                self.row_text = row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            self.rows_list_full.append(self.rows_list)
        # winter
        self.soup_winter = get_request(self.athl_domtel_winter, 'iso-8859-2')
        self.table_winter = self.soup_winter.find('table', border=0, width="500", cellspacing=False, cellpadding=0,
                                                  style=False)

        self.cols_winter = self.table_winter.find_all('tr')
        self.rows_list_full_winter = []
        for i in range(3, len(self.cols_winter)):
            self.rows_winter = self.cols_winter[i].find_all('td')
            self.rows_list_winter = []
            for row in self.rows_winter:
                self.row_text_winter = row.text.strip().split()
                self.rows_list_winter.append(" ".join(self.row_text_winter))
            self.rows_list_full_winter.append(self.rows_list_winter)
