import requests
from Table_class import Table
from Find_event import Links_Generator
import PySimpleGUI as sg
from Fav_athls import Favourite
from PZLA_stats import PZLA
from Start_lists import Start_Lists

sg.theme('DarkTeal10')

last_ten_events = Links_Generator()
last_ten_events.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
last_ten_events.get_events_results_links()
last_ten_events.get_competitions_urls()

temp = Favourite()
temp.get_empty_table()

stats = PZLA('https://statystyka.pzla.pl/spis_imprez.php?Sezon=',
             'https://statystyka.pzla.pl/spis_imprez.php?Sezon=2023Z&FiltrM=&FiltrWoj=')

stats.create_basic_layout()
stats.create_basic_layout_domtel()

startlisty = Start_Lists('https://starter.pzla.pl/?Typ=888')
startlisty.produce_basic_layout()


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
            self.text1],
            [sg.Column(self.column_1, vertical_alignment='top',
                      key=1)]]
        self.layout = [
            [sg.TabGroup([[sg.Tab('Events', self.column_final, element_justification='center')],
                          [sg.Tab('Athletes', temp.layout, key='-table-')],
                          [sg.Tab('Check recent results', stats.fourth_tab_layout, key='-table-')],
                          [sg.Tab('Advanced searching', stats.third_tab_layout, key='-table-')],
                          [sg.Tab('Check startlists', startlisty.fifth_tab_layout, key='-table-')],

                          ],
                         tab_location='topleft')]
        ]
        self.sub_windows = {}

        self.window = sg.Window('Domtel scraper 1.0', self.layout, size=(800, 600), resizable=False,
                                grab_anywhere=False,
                                grab_anywhere_using_control=False, keep_on_top=False)

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
                    self.window['Outdoor'].update(visible=True, button_color='darkgreen')
                    self.window['Indoor'].update(visible=True)
                    self.window['Indoor'].update(button_color=sg.theme_button_color()[1])
                    self.window.refresh()
                except:
                    sg.popup('Enter the correct data.')
            elif event == 'Outdoor':
                if hasattr(temp, 'rows_list_full'):
                    self.window['-TABLE-'].update(values=temp.rows_list_full)
                    self.window['Outdoor'].update(button_color='darkgreen')
                    self.window['Indoor'].update(button_color=sg.theme_button_color()[1])
                    self.window.refresh()
            elif event == 'Indoor':
                if hasattr(temp, 'rows_list_full_winter'):
                    self.window['-TABLE-'].update(values=temp.rows_list_full_winter)
                    self.window['Indoor'].update(button_color='darkgreen')
                    self.window['Outdoor'].update(button_color=sg.theme_button_color()[1])
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
            elif event == 'find_events_PZLA_domtel':
                self.season = 'Out'
                self.text_input_name_PZLA = values['name_PZLA_domtel']
                self.text_input_last_name_PZLA = values['last_name_PZLA_domtel']
                self.text_input_name_PZLA = self.text_input_name_PZLA.lower()
                self.text_input_name_PZLA = self.text_input_name_PZLA.capitalize()
                self.text_input_last_name_PZLA = self.text_input_last_name_PZLA.upper()
                print(self.text_input_name_PZLA + " " + self.text_input_last_name_PZLA)
                temp_fav_object = Favourite()
                temp_fav_object.encode(self.text_input_name_PZLA + " " + self.text_input_last_name_PZLA)
                temp_fav_object.find_in_PZLA()
                stats.get_events_from_athlete_site(temp_fav_object.athl_domtel)
                if stats.years_outdoor_list != []:
                    stats.get_season_results(stats.years_outdoor_list[-1])
                    self.window['-stats-domtel-'].update(values=stats.rows_list_full)
                    self.window['-years-'].update(visible=True)
                    self.window['-years-'].update(values=stats.years_nums_outdoor_list)
                else:
                    self.window['-stats-domtel-'].update(values=[['no data']])
                    self.window['-years-'].update(values=stats.years_nums_outdoor_list)
                    self.window.refresh()

                self.window['Outdoor_season'].update(visible=True)
                self.window['Indoor_season'].update(visible=True)
                self.window['Choose'].update(visible=True)
                self.window['Outdoor_season'].update(button_color='darkgreen')
                self.window['Indoor_season'].update(button_color=sg.theme_button_color()[1])

            elif event == 'Outdoor_season':
                self.season = 'Out'
                self.window['Outdoor_season'].update(button_color='darkgreen')
                self.window['Indoor_season'].update(button_color=sg.theme_button_color()[1])
                if stats.years_outdoor_list != []:
                    stats.get_season_results(stats.years_outdoor_list[-1])

                    self.window['-stats-domtel-'].update(values=stats.rows_list_full)
                    self.window['-years-'].update(values=stats.years_nums_outdoor_list)
                else:
                    self.window['-stats-domtel-'].update(values=[['no data']])
                    self.window['-years-'].update(values=stats.years_nums_outdoor_list)
                    self.window.refresh()

            elif event == 'Indoor_season':
                self.season = 'In'
                self.window['Indoor_season'].update(button_color='darkgreen')
                self.window['Outdoor_season'].update(button_color=sg.theme_button_color()[1])
                if stats.years_indoor_list != []:
                    stats.get_season_results(stats.years_indoor_list[-1])
                    self.window['-stats-domtel-'].update(values=stats.rows_list_full)
                    self.window['-years-'].update(values=stats.years_nums_indoor_list)
                    self.window.refresh()
                else:
                    self.window['-stats-domtel-'].update(values=[['no data']])
                    self.window['-years-'].update(values=stats.years_nums_indoor_list)
                    self.window.refresh()
            elif event == 'Choose':
                self.selected_option = values['-years-']
                self.selected_option = int((str(self.selected_option)).replace('[', "").replace(']', ""))
                print(type(self.selected_option))
                print(self.selected_option)
                if self.season == 'Out':
                    stats.get_season_results(stats.outdoor_dictionary[self.selected_option])
                    self.window['-stats-domtel-'].update(values=stats.rows_list_full)
                elif self.season == 'In':
                    stats.get_season_results(stats.indoor_dictionary[self.selected_option])
                    self.window['-stats-domtel-'].update(values=stats.rows_list_full)
            elif event == 'find_events_startlist':
                self.text_input_name_startlist = values['name_startlist']
                self.text_input_last_name_startlist = values['last_name_startlist']
                if not hasattr(startlisty, 'startlists_list'):
                    startlisty.get_incoming_events_list()
                    startlisty.get_links_to_start_lists()
                    startlisty.get_athletes_lists()
                print(self.text_input_name_startlist + " " + self.text_input_last_name_startlist)
                startlisty.check_if_participated(
                    self.text_input_name_startlist + " " + self.text_input_last_name_startlist)
                if startlisty.events_where_will_start!=[]:
                    self.window['-startlist-'].update(values=startlisty.events_where_will_start)
                else:
                    self.window['-startlist-'].update(values=[['no data']])
                self.window['See all'].update(button_color=sg.theme_button_color()[1])
            elif event == 'See all':
                if not hasattr(startlisty, 'startlists_list'):
                    startlisty.get_incoming_events_list()
                    startlisty.get_links_to_start_lists()
                    startlisty.get_athletes_lists()
                self.window['-startlist-'].update(values=startlisty.events_names_list_updated)
                self.window['See all'].update(button_color='darkgreen')
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

        self.layout_final = [[

            sg.Column(self.column_1, vertical_alignment='top', size=(100, 600)),
            sg.Column(self.column_2, vertical_alignment='top', size=(100, 600)),
            sg.Column(self.column_3, vertical_alignment='top', size=(100, 600)),
            sg.Column(self.column_4, vertical_alignment='top', size=(100, 600)),
            sg.Column(self.column_5, vertical_alignment='top', size=(100, 600)),
            sg.Column(self.column_6, vertical_alignment='top', size=(100, 600)),
            sg.Column([[sg.Button('back', pad=[[70, 0], [550, 0]])]], element_justification='right', size=(200, 600))

        ]]

        if self.column_1 != []:
            self.window = sg.Window(self.events_names_list, self.layout_final, size=(800, 600), resizable=False,
                                    grab_anywhere=False,
                                    grab_anywhere_using_control=False, keep_on_top=False, )
        elif self.column_1 == []:
            self.layout_final = [[sg.Text(
                'Unfortunately, we are unable to provide information about the results of the selected event')],
                [sg.Column(self.column_1, vertical_alignment='top', size=(100, 600)),
                 sg.Column(self.column_2, vertical_alignment='top', size=(100, 600)),
                 sg.Column(self.column_3, vertical_alignment='top', size=(100, 600)),
                 sg.Column(self.column_4, vertical_alignment='top', size=(100, 600)),
                 sg.Column(self.column_5, vertical_alignment='top', size=(100, 600)),
                 sg.Column(self.column_6, vertical_alignment='top', size=(100, 600)),
                 sg.Column([[sg.Button('back', pad=[[70, 0], [530, 0]])]], element_justification='right',
                           size=(200, 600))

                 ]
            ]
            self.window = sg.Window(self.events_names_list, self.layout_final,
                                    size=(800, 600), resizable=False,
                                    grab_anywhere=False,
                                    grab_anywhere_using_control=False, keep_on_top=False, )
        while True:
            event, values = self.window.read()
            if type(event) == int:
                self.chosen_event = event
                self.window[event].update(button_color='darkgreen')
                self.event_name = last_ten_events.competitions_lists_list[GUI.event][self.chosen_event][0]
                event_results = Table(last_ten_events.competitions_lists_list[GUI.event][self.chosen_event][1],
                                      self.event_name,
                                      last_ten_events.competitions_lists_list[GUI.event][self.chosen_event][1])
                event_results.get_headers()
                event_results.get_rows()
                event_results.get_competition_steps()
                event_results.display_table()
                event_results.Run_table()
                if hasattr(event_results, 'table_exit'):
                    for key in range(0, self.chosen_event + 1):
                        try:
                            self.window[key].update(button_color=sg.theme_button_color()[1])
                        except:
                            pass
            if event in (sg.WIN_CLOSED, 'Close') or event == 'back':
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
