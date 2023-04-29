import os
from input_encoding_func import encode_input


class Add_To_Fav():
    def __init__(self, active_tab, values):
        self.active_tab = active_tab
        self.values = values
        self.filename = 'fav.txt'
        self.filepath = os.path.abspath(self.filename)
        self.tab_keys_dict = {'-tab2-': ['name', 'last_name'],
                              '-tab3-': ['name_PZLA_domtel', 'last_name_PZLA_domtel'],
                              '-tab4-': ['name_PZLA', 'last_name_PZLA'],
                              '-tab5-': ['name_startlist', 'last_name_startlist'],
                              '-tab6-': ['name_recent', 'last_name_recent']}
        self.tab_menus_list = ['-tab_menu1-', '-tab_menu2-', '-tab_menu3-', '-tab_menu4-', '-tab_menu5-']

    def get_active_tab_and_add_to_fav(self, window):
        match self.active_tab:
            case '-tab2-':
                self.first_last_name = encode_input(self.values, self.tab_keys_dict['-tab2-'][0],
                                                    self.tab_keys_dict['-tab2-'][1])
            case '-tab3-':
                self.first_last_name = encode_input(self.values, self.tab_keys_dict['-tab3-'][0],
                                                    self.tab_keys_dict['-tab3-'][1])
            case '-tab4-':
                self.first_last_name = encode_input(self.values, self.tab_keys_dict['-tab4-'][0],
                                                    self.tab_keys_dict['-tab4-'][1])
            case '-tab5-':
                self.first_last_name = encode_input(self.values, self.tab_keys_dict['-tab5-'][0],
                                                    self.tab_keys_dict['-tab5-'][1])
            case '-tab6-':
                self.first_last_name = encode_input(self.values, self.tab_keys_dict['-tab6-'][0],
                                                    self.tab_keys_dict['-tab6-'][1])
        if os.path.isfile(self.filepath):
            with open(self.filepath, "r", encoding='utf-8') as f:
                self.file_content = f.read()
                if str(self.first_last_name) in self.file_content:
                    print('Already in Fav')

                else:
                    with open(self.filepath, "a", encoding='utf-8') as f:
                        f.write(str(self.first_last_name) + "\n")
                    print('Added to Fav')
                    for menu in self.tab_menus_list:
                        window[menu].update(['menu', create_hints_lists()])
        else:
            with open(self.filepath, "w", encoding='utf-8') as f:
                f.write(str(self.first_last_name) + "\n")
            for menu in self.tab_menus_list:
                window[menu].update(['menu', create_hints_lists()])
            print('Fav-folder created, athlete added')

    def fill_the_textboxes_and_find(self, window, event):
        self.first_last_name = self.values[event].partition(" ")
        match self.active_tab:
            case '-tab2-':
                window[self.tab_keys_dict['-tab2-'][0]].update(self.first_last_name[2])
                window[self.tab_keys_dict['-tab2-'][1]].update(self.first_last_name[0])

            case '-tab3-':
                window[self.tab_keys_dict['-tab3-'][0]].update(self.first_last_name[2])
                window[self.tab_keys_dict['-tab3-'][1]].update(self.first_last_name[0])

            case '-tab4-':
                window[self.tab_keys_dict['-tab4-'][0]].update(self.first_last_name[2])
                window[self.tab_keys_dict['-tab4-'][1]].update(self.first_last_name[0])

            case '-tab5-':
                window[self.tab_keys_dict['-tab5-'][0]].update(self.first_last_name[2])
                window[self.tab_keys_dict['-tab5-'][1]].update(self.first_last_name[0])

            case '-tab6-':
                window[self.tab_keys_dict['-tab6-'][0]].update(self.first_last_name[2])
                window[self.tab_keys_dict['-tab6-'][1]].update(self.first_last_name[0])



def create_hints_lists():
    with open('fav.txt', 'r', encoding='utf-8') as f:
        options_all = [line.strip() for line in f]
        options_name = []
        options_last_name = []
        for option in options_all:
            options_name.append((option.partition(" "))[2])
            options_last_name.append((option.partition(" "))[0])
    return options_all
