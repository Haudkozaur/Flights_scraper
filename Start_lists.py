import re
from datetime import date, timedelta
import PySimpleGUI as sg
from request_func import get_request


class Start_Lists():
    def __init__(self, url):
        self.starter = get_request(url, 'iso-8859-2')

    def get_incoming_events_list(self):
        self.table = self.starter.find('table', class_='rg2-table')
        self.rows = self.table.find_all('tr')
        self.events_names_list = []

        for row in self.rows:
            try:
                self.temp_strs_list = []
                self.cell = row.find_all('td')

                self.text_h3 = self.cell[0].find('h3')
                self.temp_strs_list.append(self.text_h3.text)

                self.text_font = self.cell[0].find('font')
                self.temp_strs_list.append(self.text_font.text)

                self.text_date = self.cell[0].text
                self.text_date = re.search(r'\d{2}.\d{2}.\d{4}', self.text_date)
                self.text_date = str(self.text_date)[-12:-2]
                self.text_date = self.text_date.split('.')
                self.text_date = date(int(self.text_date[2]), int(self.text_date[1]), int(self.text_date[0]))
                self.temp_strs_list.append(self.text_date)

                self.text_span = self.cell[0].find('span')
                self.temp_strs_list.append(self.text_span.text)

                self.href = self.cell[1].find_all('a')
                for a in self.href:
                    if a.text == 'Szczegóły':
                        self.temp_strs_list.append(f'https://starter.pzla.pl/{a["href"]}')
                        self.events_names_list.append(self.temp_strs_list)

            except:
                pass
        self.events_names_list.sort(key=lambda x: x[2])

        self.month = timedelta(weeks=4)
        self.events_names_list_updated = []
        for i in self.events_names_list:
            if (i[2] < (date.today() + self.month)) and (i[2] > date.today()):
                self.events_names_list_updated.append(i)
        print(self.events_names_list_updated)

    def get_links_to_start_lists(self):
        self.links_list = []
        for event in self.events_names_list_updated:
            self.event = get_request(event[4], 'iso-8859-2')
            self.event = self.event.find('a', class_="link", href=True, target="_blank")
            self.links_list.append(f'https://starter.pzla.pl/{self.event["href"]}')
        print(self.links_list)

    def get_athletes_lists(self):
        self.startlists_list = []
        for link in self.links_list:
            self.startlist = []
            self.startlist_html = get_request(link, 'iso-8859-2')
            self.startlist_html = self.startlist_html.find_all('td', align="left")
            for cell in self.startlist_html:
                for athl in cell.find_all('a'):
                    self.startlist.append(athl.text)
            self.startlists_list.append(self.startlist)
        print(self.startlists_list)
        print(len(self.startlists_list))

    def check_if_participated(self, first_last_name):
        self.events_where_will_start = []
        self.first_last_name = first_last_name
        self.first_last_name = list(self.first_last_name.partition(" "))
        self.first_last_name[0] = self.first_last_name[0].lower().capitalize()
        self.first_last_name[2] = self.first_last_name[2].upper()
        self.last_first_name = str(self.first_last_name[2] + " " + self.first_last_name[0])
        for startlist in self.startlists_list:
            for athl in startlist:
                if athl == self.last_first_name and not self.events_names_list_updated[self.startlists_list.index(
                        startlist)] in self.events_where_will_start:
                    self.events_where_will_start.append(
                        self.events_names_list_updated[self.startlists_list.index(startlist)])
        print(self.events_where_will_start)

    def produce_basic_layout(self):
        self.headings = ['Event', 'Localization', 'Date']

        self.fifth_tab_layout = [
            [sg.Text('Insert athletes data to find events in which he will be participating during incoming month')],
            [sg.InputText('athelete name', key='name_startlist')],
            [sg.InputText('athelete last name', key='last_name_startlist')],
            [sg.Button('Find events', key='find_events_startlist'), sg.Button('See all')],
            [sg.Table(
                values=[],
                headings=self.headings,
                col_widths=[50, 15, 12],
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-startlist-',
                row_height=35)]]
