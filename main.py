from Table_class import Table
from Find_event import Links_Generator
import PySimpleGUI as sg
from Fav_athls import Favourite
from PZLA_stats import PZLA
from Start_lists import Start_Lists
from GUI_run_class import GUI_run
from sub_GUI_run_class import sub_GUI_run

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

GUI_events = GUI_run()



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
        # Main loop
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                self.window.close()
                break
            elif event in self.sub_windows and not self.sub_windows[event].close:
                self.sub_windows[event].hide()
            elif event == 'Submit':
                GUI_events.get_atlete_PRs(values, temp, self.window)
            elif event == 'Outdoor':
                GUI_events.choose_outdoor(temp, self.window)
            elif event == 'Indoor':
                GUI_events.choose_indoor(temp, self.window)
            elif event == 'Find events':
                GUI_events.advanced_events_searching(values, stats, self.window)
            elif event == 'find_events_PZLA_domtel':
                GUI_events.find_season_results(values, self.window, stats)
            elif event == 'Outdoor_season':
                GUI_events.change_season_to_outdoor(self.window, stats)
            elif event == 'Indoor_season':
                GUI_events.change_season_to_indoor(self.window, stats)
            elif event == 'Choose':
                GUI_events.change_year(values, self.window, stats)
            elif event == 'find_events_startlist':
                GUI_events.get_startlists(values, startlisty, self.window)
            elif event == 'See all':
                GUI_events.show_all_startlists(startlisty, self.window)
            else:
                self.event = event

                print(self.competitions_lists_list)

                sub_window = SubWindow(event, self.competitions_lists_list, self.events_names_list[event])
                self.sub_windows[event] = sub_window

        self.window.close()


class SubWindow:
    def __init__(self, title, competitions_lists_list, events_names_list):
        self.events_names_list = events_names_list
        self.competitions_lists_list = competitions_lists_list
        self.title = title
        print(self.competitions_lists_list)
        print(self.events_names_list)
        sub_GUI_events_temp=sub_GUI_run()
        sub_GUI_events_temp.create_sub_layout(self.competitions_lists_list, GUI, self.events_names_list)
        self.window = sub_GUI_events_temp.window
        # sub Loop
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
