import requests
from Table_class import Table
from Find_event import Links_Generator
import PySimpleGUI as sg
from Fav_athls import Favourite
from PZLA_stats import PZLA
import webbrowser
sg.theme('DarkAmber')
last_ten_events = Links_Generator()
last_ten_events.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
last_ten_events.get_events_results_links()
last_ten_events.get_competitions_urls()

temp = Favourite()
temp.get_empty_table()

stats = PZLA('https://statystyka.pzla.pl/spis_imprez.php?Sezon=',
             'https://statystyka.pzla.pl/spis_imprez.php?Sezon=2023Z&FiltrM=&FiltrWoj=')

stats.create_basic_layout()
# stats.get_events_from_athlete_site('https://statystyka.pzla.pl/personal.php?page=profile&nr_zaw=71643&%3Cr=')

class MainWindow:
    def __init__(self, events_names_list, competitions_lists_list):
        self.events_names_list = events_names_list
        self.competitions_lists_list = competitions_lists_list
        self.text1 = sg.Text("Choose the event you are interested in.")
        self.text2 = sg.Text(
            'In the future, you will find the option to track the results of your favorite athletes here.')
        self.column_1 = []
        for i in range(0, len(self.events_names_list)):
            self.column_1.append([sg.Button(self.events_names_list[i], key=i)])
        self.column_final = [[
            self.text1,
            sg.Column(self.column_1, vertical_alignment='top',
                      key=1)]]
        self.layout = [
            [sg.TabGroup([[sg.Tab('Events', self.column_final, element_justification='center')],
                          [sg.Tab('Athletes', temp.layout, key='-table-')],

                          [sg.Tab('Check if participated', stats.third_tab_layout, key='-table-')]],
                         tab_location='topleft')]
        ]
        self.sub_windows = {}

        self.window = sg.Window('Domtel scraper 1.0', self.layout, size=(800, 600), resizable=False,
                                grab_anywhere=False,
                                grab_anywhere_using_control=False, keep_on_top=True)

    def run(self):

        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                self.window.close()
                break
            elif event in self.sub_windows and not self.sub_windows[event].close:
                self.event = event
                self.sub_windows[event].hide()
            elif event == 'Submit':
                try:
                    self.text_input_name = values['name']
                    self.text_input_last_name = values['last_name']
                    print(self.text_input_name + " " + self.text_input_last_name)
                    temp.encode(self.text_input_name + " " + self.text_input_last_name)
                    temp.find_in_PZLA()
                    temp.get_athl_site()
                    self.window['-TABLE-'].update(values=temp.rows_list_full)
                    self.window['Outdoor'].update(visible=True)
                    self.window['Indoor'].update(visible=True)
                    self.window.refresh()
                except:
                    pass
            elif event =='Outdoor':
                if hasattr(temp, 'rows_list_full'):
                    self.window['-TABLE-'].update(values=temp.rows_list_full)

                    self.window.refresh()
            elif event == 'Indoor':
                if hasattr(temp, 'rows_list_full_winter'):
                    self.window['-TABLE-'].update(values=temp.rows_list_full_winter)
                    self.window.refresh()
            elif event == 'Find events':
                self.text_input_name_PZLA = values['name_PZLA']
                self.text_input_last_name_PZLA = values['last_name_PZLA']
                self.text_input_name_PZLA = self.text_input_name_PZLA.lower()
                self.text_input_name_PZLA = self.text_input_name_PZLA.capitalize()
                self.text_input_last_name_PZLA = self.text_input_last_name_PZLA.upper()
                print(self.text_input_name_PZLA + " " + self.text_input_last_name_PZLA)
                stats.find_events()
                stats.check_if_athl_participated(self.text_input_last_name_PZLA + " " + self.text_input_name_PZLA)
                stats.produce_layout()
                self.window['-stats-'].update(values=stats.column_of_events)
                self.window.refresh()

            else:
                self.event = event
                sub_window = SubWindow(event, self.competitions_lists_list, self.events_names_list[event])
                self.event = event
                self.sub_windows[event] = sub_window

        self.window.close()


class SubWindow:
    def __init__(self, title, competitions_lists_list, events_names_list):
        self.events_names_list = events_names_list
        self.competitions_lists_list = competitions_lists_list
        self.title = title
        # the monstrosity below was forced by the nature of the pysimpleGUI library
        # which can't read a list when creating a column item inside layout
        self.column_1 = []
        self.column_2 = []
        self.column_3 = []
        self.column_4 = []
        self.column_5 = []
        self.column_6 = []
        for i in range(0, len(self.competitions_lists_list[GUI.event]), 6):
            self.column_1.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(1, len(self.competitions_lists_list[GUI.event]), 6):
            self.column_2.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(2, len(self.competitions_lists_list[GUI.event]), 6):
            self.column_3.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(3, len(self.competitions_lists_list[GUI.event]), 6):
            self.column_4.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(4, len(self.competitions_lists_list[GUI.event]), 6):
            self.column_5.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(5, len(self.competitions_lists_list[GUI.event]), 6):
            self.column_6.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        self.back = sg.Button('back')
        self.layout_final = [[

            sg.Column(self.column_1, vertical_alignment='top'),
            sg.Column(self.column_2, vertical_alignment='top'),
            sg.Column(self.column_3, vertical_alignment='top'),
            sg.Column(self.column_4, vertical_alignment='top'),
            sg.Column(self.column_5, vertical_alignment='top'),
            sg.Column(self.column_6, vertical_alignment='top')
        ]]

        if self.column_1 != []:
            self.window = sg.Window(self.events_names_list, self.layout_final, size=(800, 600), resizable=False,
                                    grab_anywhere=False,
                                    grab_anywhere_using_control=False, keep_on_top=True, )
        elif self.column_1 == []:
            self.layout_final = [[sg.Text(
                'Unfortunately, we are unable to provide information about the results of the selected event')]]
            self.window = sg.Window(self.events_names_list, self.layout_final,
                                    size=(800, 600), resizable=False,
                                    grab_anywhere=False,
                                    grab_anywhere_using_control=False, keep_on_top=True, )
        while True:
            event, values = self.window.read()
            if type(event) == int:
                self.chosen_event = event
                print(self.chosen_event)
                requested_html = requests.get(
                    last_ten_events.competitions_lists_list[GUI.event][self.chosen_event][1])
                self.event_name = last_ten_events.competitions_lists_list[GUI.event][self.chosen_event][0]
                event_results = Table(requested_html, self.event_name,
                                      last_ten_events.competitions_lists_list[GUI.event][self.chosen_event][1])
                event_results.get_headers()
                event_results.get_rows()
                event_results.get_competition_steps()
                event_results.display_table()

            if event in (sg.WIN_CLOSED, 'Close'):
                self.window.close()
                break

    def hide(self):
        self.window.hide()
        self.closed = True

    def close(self):
        if not self.closed:
            self.window.close()
            self.closed = True


GUI = MainWindow(last_ten_events.events_names_list, last_ten_events.competitions_lists_list)
GUI.run()
