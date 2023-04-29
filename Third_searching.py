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
        self.links_list = []
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
                # step_1 = event[1].partition("?")
                # print(step_1)
                # step_2 = step_1[2].partition('dzien')
                # print(step_2)
                # step_3 = f'{step_1[0]}{step_1[1]}{step_2[1]}{step_2[2]}'
                # print(step_3)
                # step_4 = step_3.replace('rank=1', '')
                # print(step_4)
                # self.where_participated_events.append(step_4)
                step_1 = event[1].partition("?")
                print(step_1)
                step_2 = step_1[-1].partition('&')
                print(step_2)
                step_3 = step_2[-1].replace('&rank=1', "")
                print(step_3)
                step_4 = (step_3.partition('impreza='))[-2] + (step_3.partition('impreza='))[-1]
                print(step_4)
                step_5 = step_1[0] + step_1[1] + step_4
                self.where_participated_events.append(step_5)
            # getting competition name
            self.link = event[1].partition("konkurencja=")
            self.link = (self.link[-1].partition('&'))[0]
            self.links_list.append(self.link)
            print(self.links_list)
            self.layout_list_1.append(event[1])
            print(self.where_participated_events)
        for i in range(0, len(self.where_participated_events)):
            print(self.where_participated_events[i])
            print(events_dict[self.where_participated_events[i]])
            print(self.where_participated_events.index(self.where_participated_events[i]))
            self.layout_list_2.append(f'{events_dict[self.where_participated_events[i]]} {self.links_list[i]}')

        self.layout_list_full = list(zip(self.layout_list_1, self.layout_list_2))
        print(self.layout_list_full)

    def create_basic_layout(self):
        self.menu = ['menu', create_hints_lists()]
        self.sixth_tab_layout = [
            [sg.Text(
                "Enter an athlete's details to find events in which they were participating recently (only for biggest events)")],
            [sg.InputText('name', key='name_recent'),
             sg.ButtonMenu('Choose from Favourites', self.menu, key='-tab_menu5-', size=(20, 1))],
            [sg.InputText('last name', key='last_name_recent'),
             sg.Button('Add to Favourites', key='-add_athl5-', size=(18, 1)),
             sg.ButtonMenu('Delete from Favourites', self.menu, key='-del_menu5-', size=(20, 1))],
            [sg.Button('Find events', key='find_events_recent', size=(39, 1))],
            [sg.Table(
                values=[],
                headings=['', 'event'],
                col_widths=[0, 80],
                auto_size_columns=False,
                display_row_numbers=False,
                vertical_scroll_only=False,
                justification='center',
                key='-THIRD_TABLE-',
                row_height=35,
                enable_events=True)]]
