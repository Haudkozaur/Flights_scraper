import PySimpleGUI as sg
import re
from request_func import get_request
from Add_To_Favourites import create_hints_lists


class PZLA():
    def __init__(self, url, url_winter):
        self.pzla_stats = url
        self.pzla_stats_winter = url_winter

    def find_events(self):
        self.stats = get_request(self.pzla_stats, 'iso-8859-2')
        self.events_list_full = []
        self.events_names_list = []
        self.events_links_list = []
        self.rows = self.stats.find_all('tr')
        for i in range(1, len(self.rows)):
            for event in self.rows[i].find_all('td', align='left'):
                self.events_names_list.append(event.text.replace('\n', ' '))
            for event in self.rows[i].find_all('a', title=True, href=True, onclick=True, target='_blank'):
                self.events_links_list.append(f'https://statystyka.pzla.pl/{event["href"]}')
        for j in range(0, len(self.events_names_list)):
            self.events_list_full.append([self.events_names_list[j], self.events_links_list[j]])
        self.stats_winter = get_request(self.pzla_stats_winter, 'iso-8859-2')
        self.events_names_list = []
        self.events_links_list = []
        self.rows = self.stats_winter.find_all('tr')
        for i in range(1, len(self.rows)):
            for event in self.rows[i].find_all('td', align='left'):
                self.events_names_list.append(event.text.replace('\n', ' '))
            for event in self.rows[i].find_all('a', title=True, href=True, onclick=True, target='_blank'):
                self.events_links_list.append(f'https://statystyka.pzla.pl/{event["href"]}')
        for j in range(0, len(self.events_names_list)):
            self.events_list_full.append([self.events_names_list[j], self.events_links_list[j]])

    def get_athls_lists(self):
        # self.first_last_name = first_last_name
        self.first_last_names_list = []
        for event in self.events_list_full:
            self.results = get_request(event[1], 'iso-8859-2')
            self.rows_results = self.results.find_all('tr')
            for i in range(0, len(self.rows_results)):
                for athlete in self.rows_results[i].find_all('td'):
                    for j in athlete.find_all('a', class_='p1', href=True, onclick=True, target='blank'):
                        self.first_last_names_list.append([j.text, event])
        # print(self.first_last_names_list)

    def check_if_athl_participated(self, first_last_name):
        self.events_list_full_temp = []
        self.first_last_name = first_last_name
        for athl in range(0, len(self.first_last_names_list)):
            if self.first_last_name in self.first_last_names_list[athl][0] and not self.first_last_names_list[athl][
                                                                                       1] in self.events_list_full_temp:
                self.events_list_full_temp.append(self.first_last_names_list[athl][1])

    def create_basic_layout(self):
        self.menu = ['menu', create_hints_lists()]
        self.headings = ['event name']
        self.third_tab_layout = [
            [sg.Text("Enter an athlete's details to find events in which they were participating this year")],
            [sg.InputText('name', key='name_PZLA'),
             sg.ButtonMenu('Choose from Favourites', self.menu, key='-tab_menu2-', size=(20, 1))],
            [sg.InputText('last name', key='last_name_PZLA'),
             sg.Button('Add to Favourites', key='-add_athl2-', size=(18, 1)),
             sg.ButtonMenu('Delete from Favourites', self.menu, key='-del_menu2-', size=(20, 1))],
            [sg.Button('Find events', size=(39, 1), key='Find events', disabled=False)],
            [sg.Text('Click on an event to go to the results website.', visible=False, key='-click_text2-')],
            [sg.Table(
                values=[],
                headings=self.headings,
                def_col_width=80,
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-TABLE_stats-',
                row_height=35,
                enable_events=True)]]

    def produce_layout(self):
        self.column_of_events = []
        for i in range(0, len(self.events_list_full_temp)):
            self.column_of_events.append([self.events_list_full_temp[i][0], self.events_list_full_temp[i][1]])
        # print(self.column_of_events)

    def create_basic_layout_domtel(self):
        self.headings = ['competition', 'result', 'date', 'city']
        self.menu = ['menu', create_hints_lists()]
        self.fourth_tab_layout = [
            [sg.Text("Enter an athlete's details to find events in which he was participating during the seasons")],
            [sg.InputText('name', key='name_PZLA_domtel'),
             sg.ButtonMenu('Choose from Favourites', self.menu, key='-tab_menu3-', size=(20, 1))],
            [sg.InputText('last name', key='last_name_PZLA_domtel'),
             sg.Button('Add to Favourites', key='-add_athl3-', size=(18, 1)),
             sg.ButtonMenu('Delete from Favourites', self.menu, key='-del_menu3-', size=(20, 1))
             ],
            [sg.Button('Find events', key='find_events_PZLA_domtel', size=(39, 1)),

             sg.Listbox(values=[], key="-years-", size=(20, 3), visible=False),
             sg.Button("Choose", visible=False, key="Choose")
             ],
            [sg.Button('Outdoor', visible=False, key='Outdoor_season',size=(7, 1)),
             sg.Button('Indoor', visible=False, key='Indoor_season',size=(7, 1))],
            [sg.Table(
                values=[],
                headings=self.headings,
                def_col_width=15,
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-TABLE_stats-domtel-',
                row_height=35,
            )]]

    def get_events_from_athlete_site(self, url):
        self.athl_domtel = url
        self.athl_domtel_season = f'{self.athl_domtel.replace("profile", "sb")}'
        self.season = get_request(self.athl_domtel_season, 'iso-8859-2')
        self.years = self.season.find('table', border=0, width="500", cellspacing=0, cellpadding=0,
                                      style='border: 1 dotted #A4CFFF')
        self.col_season = self.years.find_all('tr')
        self.years_outdoor_list = []
        self.years_indoor_list = []
        for col in self.col_season:
            for row in col.find_all('td', colspan="5"):
                for cell in row.find_all('a', href=True):
                    if (cell["href"])[-1] == 'L':
                        self.years_outdoor_list.append(f'https://statystyka.pzla.pl/{cell["href"]}')
                    if (cell["href"])[-1] == 'Z':
                        self.years_indoor_list.append(f'https://statystyka.pzla.pl/{cell["href"]}')
            break

        self.years_nums_outdoor_list = []
        self.years_nums_indoor_list = []
        for year in self.years_outdoor_list:
            self.year = re.findall('\d+', year)
            self.year = list(map(int, self.year))
            self.year.sort()
            self.years_nums_outdoor_list.append(self.year[-2])
        for year in self.years_indoor_list:
            self.year = re.findall('\d+', year)
            self.year = list(map(int, self.year))
            self.year.sort()
            self.years_nums_indoor_list.append(self.year[-2])

        self.outdoor_dictionary = {years_nums_outdoor_list: years_outdoor_list for
                                   years_nums_outdoor_list, years_outdoor_list in
                                   zip(self.years_nums_outdoor_list, self.years_outdoor_list)}
        self.indoor_dictionary = {years_nums_indoor_list: years_indoor_list for
                                  years_nums_indoor_list, years_indoor_list in
                                  zip(self.years_nums_indoor_list, self.years_indoor_list)}

    def get_season_results(self, url):
        self.soup = get_request(url, 'iso-8859-2')
        self.table = self.soup.find_all('table', border=0, width="500", cellspacing=0, cellpadding=0, style=False)

        self.cols = self.table[1].find_all('tr')
        self.rows_list_full = []
        for i in range(6, len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for self.row in self.rows:
                self.row_text = self.row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            self.rows_list_full.append(self.rows_list)
        for row in range(0, len(self.rows_list_full)):
            try:
                self.rows_list_full[row].pop(2)
            except:
                pass
