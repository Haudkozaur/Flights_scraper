import PySimpleGUI as sg


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
        print(self.competitions_lists_list[GUI.event])
        # the monstrosity below was forced by the nature of the pysimpleGUI library
        # which can't read a list when creating a column item inside layout
        for i in range(0, len(self.competitions_lists_list[GUI.event]), 6):
            print('wtf1')
            self.column_1.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(1, len(self.competitions_lists_list[GUI.event]), 6):
            print('wtf2')
            self.column_2.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(2, len(self.competitions_lists_list[GUI.event]), 6):
            print('wtf3')
            self.column_3.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(3, len(self.competitions_lists_list[GUI.event]), 6):
            print('wtf4')
            self.column_4.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(4, len(self.competitions_lists_list[GUI.event]), 6):
            print('wtf5')
            self.column_5.append([sg.Button(self.competitions_lists_list[GUI.event][i][0], key=i)])
        for i in range(5, len(self.competitions_lists_list[GUI.event]), 6):
            print('wtf6')
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
