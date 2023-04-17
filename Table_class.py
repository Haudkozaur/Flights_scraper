from bs4 import BeautifulSoup
import PySimpleGUI as sg
import requests
sg.theme('DarkAmber')

class Table:
    def __init__(self, url, event_name, events_results_links_list):
        self.prefix = events_results_links_list.partition('.')
        self.event_name = event_name
        self.html = url
        self.html.encoding = 'utf-8'
        self.html_text = self.html.text
        self.soup = BeautifulSoup(self.html_text, 'lxml')
        self.table = self.soup.find('table', class_='Listy')
        self.sub_windows = {}

    def get_headers(self):
        self.cols = self.table.find_all('tr')
        self.headers_div = self.cols[0].find_all('td')
        self.headings_list = []
        for self.header in self.headers_div:
            self.header_text = self.header.text.strip().split()
            self.headings_list.append(" ".join(self.header_text))

    def get_rows(self):
        self.rows_list_full = []
        for i in range(1, len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for self.row in self.rows:
                self.row_text = self.row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            self.rows_list_full.append(self.rows_list)


    def get_competition_steps(self):
        self.buttons_list = []
        for button in self.soup.find_all('a', class_='konkur_przycisk', href=True, target=False):
            if len(button['href']) > 30:
                self.buttons_list.append([button.text, button['href']])

        self.column_comp_steps = []
        for i in range(0, len(self.buttons_list)):
            self.column_comp_steps.append([sg.Button(self.buttons_list[i][0], key=i)])

    def display_table(self):
        self.w, self.h = sg.Window.get_screen_size()
        self.layout = [
            [sg.Table(
                values=self.rows_list_full,
                headings=self.headings_list,
                max_col_width=35,
                auto_size_columns=True,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                num_rows=len(self.rows_list_full),
                key='-TABLE-',
                row_height=35),
                sg.Column(self.column_comp_steps, vertical_alignment='top')

            ]]
        self.window = sg.Window(self.event_name, self.layout, keep_on_top=True, size=(1400, 600))
        self.lock = True
        while self.lock:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event in self.sub_windows and not self.sub_windows[event].close:
                self.event = event
                self.sub_windows[event].hide()
            if type(event) == int:
                self.window.close()
                self.chosen_step = event
                if self.prefix[0] != 'https://online':
                    self.requested_html = requests.get(
                        f'{self.prefix[0]}.domtel-sport.pl/{self.buttons_list[self.chosen_step][1]}')

                    temp_object = Table(self.requested_html, self.buttons_list[self.chosen_step][0],
                                        f'{self.prefix[0]}.domtel-sport.pl/{self.buttons_list[self.chosen_step][1]}')
                else:
                    self.requested_html = requests.get(
                        f'{self.prefix[0]}.domtel-sport.pl/index2.php{self.buttons_list[self.chosen_step][1]}')

                    temp_object = Table(self.requested_html, self.buttons_list[self.chosen_step][0],
                                        f'{self.prefix[0]}.domtel-sport.pl/index2.php{self.buttons_list[self.chosen_step][1]}')
                temp_object.get_headers()
                temp_object.get_rows()
                temp_object.get_competition_steps()
                temp_object.display_table()
                self.chosen_step = event
                self.sub_windows[event] = temp_object
