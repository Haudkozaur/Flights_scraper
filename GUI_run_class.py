import PySimpleGUI as sg
from Fav_athls import Favourite
from input_encoding_func import encode_input
import webbrowser
from Table_class import Table


class GUI_run:

    def create_first_tab_layout(self, events_names_list):
        self.text1 = sg.Text("Choose the event you are interested in.")
        self.column_1 = []
        for i in range(0, len(events_names_list)):
            self.column_1.append([sg.Button(events_names_list[i], key=i)])
        self.column_final = [[
            self.text1],
            [sg.Column(self.column_1, vertical_alignment='top',
                       key=1)]]
        return self.column_final

    def get_atlete_PRs(self, values, temp, window):
        try:
            self.text_input_name = values['name']
            self.text_input_last_name = values['last_name']
            print(self.text_input_name + " " + self.text_input_last_name)
            temp.encode(self.text_input_name + " " + self.text_input_last_name)
            temp.find_in_PZLA()
            temp.get_athl_site()
            window['-TABLE-'].update(values=temp.rows_list_full)
            window['Outdoor'].update(visible=True, button_color='darkgreen')
            window['Indoor'].update(visible=True)
            window['Indoor'].update(button_color=sg.theme_button_color()[1])
            window.refresh()
        except:
            sg.popup('Enter the correct data.')
            window['-TABLE-'].update(values=[])
            window['Indoor'].update(button_color=sg.theme_button_color()[1])
            window['Outdoor'].update(button_color=sg.theme_button_color()[1])

    def choose_outdoor(self, temp, window):
        if hasattr(temp, 'rows_list_full'):
            window['-TABLE-'].update(values=temp.rows_list_full)
            window['Outdoor'].update(button_color='darkgreen')
            window['Indoor'].update(button_color=sg.theme_button_color()[1])
            window.refresh()

    def choose_indoor(self, temp, window):
        if hasattr(temp, 'rows_list_full_winter'):
            window['-TABLE-'].update(values=temp.rows_list_full_winter)
            window['Indoor'].update(button_color='darkgreen')
            window['Outdoor'].update(button_color=sg.theme_button_color()[1])
            window.refresh()

    def advanced_events_searching(self, values, stats, window):
        if not hasattr(stats, 'events_list_full'):
            stats.find_events()
            stats.get_athls_lists()
        stats.check_if_athl_participated(encode_input(values, 'name_PZLA', 'last_name_PZLA'))
        stats.produce_layout()
        window['-TABLE_stats-'].update(values=stats.column_of_events)
        print(stats.column_of_events)
        window.refresh()

    def find_season_results(self, values, window, stats):
        try:
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
                window['-TABLE_stats-domtel-'].update(values=stats.rows_list_full)

                window['-years-'].update(visible=True)
                window['-years-'].update(values=stats.years_nums_outdoor_list)
            else:
                window['-TABLE_stats-domtel-'].update(values=[['no data']])
                window['-years-'].update(values=stats.years_nums_outdoor_list)
                window.refresh()
            window['Outdoor_season'].update(visible=True)
            window['Indoor_season'].update(visible=True)
            window['Choose'].update(visible=True)
            window['Outdoor_season'].update(button_color='darkgreen')
            window['Indoor_season'].update(button_color=sg.theme_button_color()[1])
        except:
            sg.popup('Enter the correct data.')
            window['-TABLE_stats-domtel-'].update(values=[])
            window['Outdoor_season'].update(button_color=sg.theme_button_color()[1])
            window['Indoor_season'].update(button_color=sg.theme_button_color()[1])
            self.season = 'Out'

    def change_season_to_outdoor(self, window, stats):
        self.season = 'Out'
        window['Outdoor_season'].update(button_color='darkgreen')
        window['Indoor_season'].update(button_color=sg.theme_button_color()[1])
        if stats.years_outdoor_list != []:
            stats.get_season_results(stats.years_outdoor_list[-1])

            window['-TABLE_stats-domtel-'].update(values=stats.rows_list_full)
            window['-years-'].update(values=stats.years_nums_outdoor_list)
        else:
            window['-TABLE_stats-domtel-'].update(values=[['no data']])
            window['-years-'].update(values=stats.years_nums_outdoor_list)
            window.refresh()

    def change_season_to_indoor(self, window, stats):
        self.season = 'In'
        window['Indoor_season'].update(button_color='darkgreen')
        window['Outdoor_season'].update(button_color=sg.theme_button_color()[1])
        if stats.years_indoor_list != []:
            stats.get_season_results(stats.years_indoor_list[-1])
            window['-TABLE_stats-domtel-'].update(values=stats.rows_list_full)
            window['-years-'].update(values=stats.years_nums_indoor_list)
            window.refresh()
        else:
            window['-TABLE_stats-domtel-'].update(values=[['no data']])
            window['-years-'].update(values=stats.years_nums_indoor_list)
            window.refresh()

    def change_year(self, values, window, stats):
        self.selected_option = values['-years-']
        self.selected_option = int((str(self.selected_option)).replace('[', "").replace(']', ""))
        if self.season == 'Out':
            stats.get_season_results(stats.outdoor_dictionary[self.selected_option])
            window['-TABLE_stats-domtel-'].update(values=stats.rows_list_full)
        elif self.season == 'In':
            stats.get_season_results(stats.indoor_dictionary[self.selected_option])
            window['-TABLE_stats-domtel-'].update(values=stats.rows_list_full)

    def get_startlists(self, values, startlisty, window):
        self.text_input_name_startlist = values['name_startlist']
        self.text_input_last_name_startlist = values['last_name_startlist']
        if not hasattr(startlisty, 'startlists_list'):
            startlisty.get_incoming_events_list()
            startlisty.get_links_to_start_lists()
            startlisty.get_athletes_lists()
        print(self.text_input_name_startlist + " " + self.text_input_last_name_startlist)
        startlisty.check_if_participated(
            self.text_input_name_startlist + " " + self.text_input_last_name_startlist)
        if startlisty.events_where_will_start != []:
            window['-startlist-'].update(values=startlisty.events_where_will_start)
        else:
            window['-startlist-'].update(values=[['no data']])
        window['See all'].update(button_color=sg.theme_button_color()[1])

    def show_all_startlists(self, startlisty, window):
        if not hasattr(startlisty, 'startlists_list'):
            startlisty.get_incoming_events_list()
            startlisty.get_links_to_start_lists()
            startlisty.get_athletes_lists()
        window['-startlist-'].update(values=startlisty.events_names_list_updated)
        window['See all'].update(button_color='darkgreen')

    def find_and_display_recent_results(self, third_searching, last_ten_events, values, window):
        if not hasattr(third_searching, 'athletes_in_competitions_list'):
            third_searching.find_events_in_domtel(last_ten_events.competitions_lists_list)
        third_searching.check_if_participated(encode_input(values, 'name_recent', 'last_name_recent'))
        third_searching.reverse_links_generator(last_ten_events.events_dict)
        window['-THIRD_TABLE-'].update(values=third_searching.layout_list_full)

    def browse_for_result(self, active_tab, event, stats, third_searching):
        if event != []:
            match active_tab:
                case '-tab4-':
                    webbrowser.open(stats.column_of_events[int(event[0])][1])
                case '-tab6-':
                    temp_table = Table(third_searching.layout_list_full[int(event[0])][0],
                                       third_searching.layout_list_full[int(event[0])][1],
                                       third_searching.layout_list_full[int(event[0])][0])
                    temp_table.get_headers()
                    temp_table.get_rows()
                    # temp_table.get_competition_steps()
                    temp_table.display_table()
                    temp_table.Run_table()
