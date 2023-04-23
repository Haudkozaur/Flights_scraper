import PySimpleGUI as sg
from Table_class import Table


class sub_GUI_run:
    def __init__(self):
        self.column_1 = []
        self.column_2 = []
        self.column_3 = []
        self.column_4 = []
        self.column_5 = []
        self.column_6 = []

    def create_sub_layout(self, competitions_lists_list, GUI, events_names_list):
        self.competitions_lists_list = competitions_lists_list

        # the monstrosity below was forced by the nature of the pysimpleGUI library
        # which can't read a list when creating a column item inside layout unfortunately
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
            self.window = sg.Window(events_names_list, self.layout_final, size=(800, 600), resizable=False,
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
            self.window = sg.Window(events_names_list, self.layout_final,
                                    size=(800, 600), resizable=False,
                                    grab_anywhere=False,
                                    grab_anywhere_using_control=False, keep_on_top=False, )

    def chose_event(self, event, last_ten_events, GUI):
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
