import requests
from bs4 import BeautifulSoup
import PySimpleGUI as sg


class PZLA():
    def __init__(self, url, url_winter):
        self.pzla_stats = url
        self.pzla_stats_winter = url_winter

    def find_events(self):
        self.pzla_stats_html = requests.get(self.pzla_stats)
        self.pzla_stats_html.encoding = 'iso-8859-2'
        self.pzla_stats_html_text = self.pzla_stats_html.text
        self.stats = BeautifulSoup(self.pzla_stats_html_text, 'lxml')
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
        print(self.events_list_full)
        print(len(self.events_list_full))
        self.pzla_stats_winter_html = requests.get(self.pzla_stats_winter)
        self.pzla_stats_winter_html.encoding = 'iso-8859-2'
        self.pzla_stats_winter_html_text = self.pzla_stats_winter_html.text
        self.stats_winter = BeautifulSoup(self.pzla_stats_winter_html_text, 'lxml')
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
        print(self.events_list_full)
        print(len(self.events_list_full))

    def check_if_athl_participated(self, first_last_name):
        self.first_last_name = first_last_name
        self.events_list_full_temp = []
        for event in self.events_list_full:
            self.first_last_names_list = []
            self.results_html = requests.get(event[1])
            self.results_html.encoding = 'iso-8859-2'
            self.results_html_text = self.results_html.text
            self.results = BeautifulSoup(self.results_html_text, 'lxml')
            self.rows_results = self.results.find_all('tr')
            for i in range(0, len(self.rows_results)):
                for athlete in self.rows_results[i].find_all('td'):
                    for j in athlete.find_all('a', class_='p1', href=True, onclick=True, target='blank'):
                        self.first_last_names_list.append(j.text)
            print(self.first_last_names_list)

            if self.first_last_name in self.first_last_names_list:
                self.events_list_full_temp.append(event)
        print(self.events_list_full_temp)
        print(len(self.events_list_full_temp))

    def create_basic_layout(self):
        self.headings = ['event name']
        self.third_tab_layout = [
            [sg.Text('Insert athletes data to find events in which he was participating')],
            [sg.InputText('athelete name', key='name_PZLA')],
            [sg.InputText('athelete last name', key='last_name_PZLA')],
            [sg.Button('Find events')],
            [sg.Table(
                values=[],
                headings=self.headings,
                def_col_width=50,
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-stats-',
                row_height=35)]]

    def produce_layout(self):
        self.column_of_events = []

        for i in range(0, len(self.events_list_full_temp)):
            self.column_of_events.append(self.events_list_full_temp[i][0])
            # self.dictionary_of_events[self.events_list_full_temp[i][0]] = self.events_list_full_temp[i][1]
    def create_basic_layout_domtel(self):
        self.headings = ['competition', 'result', 'date', 'city']
        self.fourth_tab_layout = [
            [sg.Text('Insert athletes data to find events in which he was participating this year')],
            [sg.InputText('athelete name', key='name_PZLA_domtel')],
            [sg.InputText('athelete last name', key='last_name_PZLA_domtel')],
            [sg.Button('Find events',key='find_events_PZLA_domtel')],
            [sg.Table(
                values=[],
                headings=self.headings,
                def_col_width=15,
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-stats-domtel',
                row_height=35)]]

    def get_events_from_athlete_site(self, url):
        self.athl_domtel = url
        self.athl_domtel_season = f'{self.athl_domtel.replace("profile","sb")}&sezon=2022&sezon2=L'
        print(self.athl_domtel_season)
        self.athl_site_html = requests.get(self.athl_domtel_season)
        self.athl_site_html.encoding = 'iso-8859-2'
        self.athl_site_html_text = self.athl_site_html.text
        self.soup = BeautifulSoup(self.athl_site_html_text, 'lxml')
        self.table = self.soup.find_all('table', border=0, width="500", cellspacing=0, cellpadding=0, style=False)
        # print(self.table)
        self.cols = self.table[1].find_all('tr')
        self.rows_list_full = []
        for i in range(6, len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for self.row in self.rows:
                self.row_text = self.row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            self.rows_list_full.append(self.rows_list)
        for row in range(0,len(self.rows_list_full)):
            try:
                self.rows_list_full[row].pop(2)
            except:
                pass





# stats = PZLA('https://statystyka.pzla.pl/spis_imprez.php?Sezon=',
#              'https://statystyka.pzla.pl/spis_imprez.php?Sezon=2023Z&FiltrM=&FiltrWoj=')
#
# # stats.find_events()
#
# # stats.check_if_athl_participated('JANIK Emilia')
# stats.get_events_from_athlete_site('https://statystyka.pzla.pl/personal.php?page=profile&nr_zaw=71643&%3Cr=')