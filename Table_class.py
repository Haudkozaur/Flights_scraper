import PySimpleGUI as sg
from request_func import get_request


class Table:
    def __init__(self, url, event_name, events_results_links_list):
        self.event_name = event_name
        self.prefix = events_results_links_list.partition('.')
        self.soup = get_request(url, 'utf-8')
        self.table = self.soup.find('table', class_='Listy')
        self.sub_windows = {}

    def get_headers(self):
        self.cols = self.table.find_all('tr')
        self.headers_div = self.cols[0].find_all('td')
        self.headings_list = []
        for header in self.headers_div:
            self.header_text = header.text.strip().split()
            self.headings_list.append(" ".join(self.header_text))

    def get_rows(self):
        self.rows_list_full = []
        for i in range(1, len(self.cols)):
            self.rows = self.cols[i].find_all('td')
            self.rows_list = []
            for row in self.rows:
                self.row_text = row.text.strip().split()
                self.rows_list.append(" ".join(self.row_text))
            self.rows_list_full.append(self.rows_list)

    def get_competition_steps(self):
        self.buttons_list = []
        for button in self.soup.find_all('a', class_='konkur_przycisk', href=True, target=False):
            if len(button['href']) > 30:
                self.buttons_list.append([button.text, button['href']])
        if self.buttons_list != []:
            self.column_comp_steps = [[sg.Button(self.buttons_list[0][0], key=0, button_color='darkgreen')]]
            for i in range(1, len(self.buttons_list)):
                self.column_comp_steps.append([sg.Button(self.buttons_list[i][0], key=i)])
        else:
            self.column_comp_steps = []

    def display_table(self):

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
                key='-TABLE_table-',
                row_height=35),
                sg.Column(self.column_comp_steps, vertical_alignment='top')

            ]]

    def Run_table(self):
        self.window = sg.Window(self.event_name, self.layout, keep_on_top=True, size=(1400, 600))
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                self.table_exit = True
                break
            if type(event) == int:

                self.chosen_step = event

                if self.prefix[0] != 'https://online':
                    temp_object = Table(f'{self.prefix[0]}.domtel-sport.pl/{self.buttons_list[self.chosen_step][1]}',
                                        self.buttons_list[self.chosen_step][0],
                                        f'{self.prefix[0]}.domtel-sport.pl/{self.buttons_list[self.chosen_step][1]}')
                else:

                    temp_object = Table(
                        f'{self.prefix[0]}.domtel-sport.pl/index2.php{self.buttons_list[self.chosen_step][1]}',
                        self.buttons_list[self.chosen_step][0],
                        f'{self.prefix[0]}.domtel-sport.pl/index2.php{self.buttons_list[self.chosen_step][1]}')
                temp_object.get_headers()
                temp_object.get_rows()
                temp_object.get_competition_steps()

                self.table_widget = self.window['-TABLE_table-'].Widget
                for cid, text in zip(self.headings_list, temp_object.headings_list):
                    self.table_widget.heading(cid, text=text)
                self.window['-TABLE_table-'].update(values=(temp_object.rows_list_full))
                self.window['-TABLE_table-'].update(num_rows=len(temp_object.rows_list_full))
                for button in range(0, len(self.buttons_list)):
                    self.window[button].update(button_color=sg.theme_button_color()[1])
                self.window[self.chosen_step].update(button_color='darkgreen')

                self.window.refresh()

                self.sub_windows[event] = temp_object
