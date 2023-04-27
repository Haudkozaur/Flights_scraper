import PySimpleGUI as sg
from request_func import get_request
from Add_To_Favourites import create_hints_lists

class Third_Searching():
    def find_events_in_domtel(self, competitions_lists_list):
        self.competitions_lists_list = competitions_lists_list
        self.competitions_rankings_list = []
        for event in self.competitions_lists_list:
            if event != []:
                for competition in range(0, len(event)):
                    self.competitions_rankings_list.append(f'{event[competition][1]}&rank=1')
        print(self.competitions_rankings_list)
        self.athletes_in_competitions_list = []
        for ranking in self.competitions_rankings_list:
            self.list = get_request(ranking, 'utf-8')
            self.list = self.list.find('table', class_='Listy')
            self.list = self.list.find_all('tr')
            for i in range(1, len(self.list)):
                self.rows = self.list[i].find_all('td')
                self.names_last_names_list = []
                for row in self.rows:
                    if row.find_all('a', href=True) != []:
                        self.athletes_in_competitions_list.append([row.text.replace('\n', ""), ranking])
        print(self.athletes_in_competitions_list)

    def check_if_participated(self, first_last_name):
        self.where_participated = []
        for athlete in self.athletes_in_competitions_list:
            if first_last_name in athlete:
                self.where_participated.append(athlete)
        print(self.where_participated)

    def reverse_links_generator(self, events_dict):
        self.where_participated_events = []
        self.layout_list_1 = []
        self.layout_list_2 = []
        for event in self.where_participated:
            prefix = event[1].partition('.')
            if str(prefix[0]) == 'https://live':
                step_1 = event[1].partition("?")
                step_2 = (step_1[0])[:-1]
                self.where_participated_events.append(step_2)
            elif str(prefix[0]) != 'https://online':
                step_1 = event[1].partition("?")
                step_2 = f'{step_1[0]}'
                self.where_participated_events.append(step_2)
            else:
                step_1 = event[1].partition("?")
                step_2 = step_1[2].partition('dzien')
                step_3 = f'{step_1[0]}{step_1[1]}{step_2[1]}{step_2[2]}'
                step_4 = step_3.replace('rank=1', '')
                self.where_participated_events.append(step_4)
            self.layout_list_1.append(event[1])
            print(self.where_participated_events)
        for event in self.where_participated_events:
            print(event)
            print(events_dict[event])
            self.layout_list_2.append(events_dict[event])

        self.layout_list_full = list(zip(self.layout_list_1, self.layout_list_2))
        print(self.layout_list_full)
        print(type(self.layout_list_full[0]))

    def create_basic_layout(self):
        self.menu = ['menu', create_hints_lists()]
        self.sixth_tab_layout = [
            [sg.Text('Insert athletes data to find events in which he will be participating recently')],
            [sg.InputText('athlete name', key='name_recent'),
             sg.ButtonMenu('Choose from Favourites', self.menu, key='-tab_menu-')],
            [sg.InputText('athlete last name', key='last_name_recent'),
             sg.Button('Add to Favourites', key='-add_athl5-')],
            [sg.Button('Find events', key='find_events_recent')],
            [sg.Table(
                values=[],
                headings=['','event'],
                col_widths=[0, 80],
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-THIRD_TABLE-',
                row_height=35)]]

    # def create_layout(self):
    #     self.column = []
    #     for i in range(0, len(self.layout_list_full)):
    #         self.column.append([sg.Button(self.layout_list_full[i][1], key=f'{self.layout_list_full[i][1]}')])



# dupa = Third_Searching()
# dupa.find_events_in_domtel(test.competitions_lists_list)
# dupa.check_if_participated('KOMAŃSKI Albert')
# dupa.reverse_links_generator(test.events_dict)
