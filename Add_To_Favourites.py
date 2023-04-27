import os
from input_encoding_func import encode_input


class Add_To_Fav():
    def __init__(self):
        self.filename = 'fav.txt'
        self.filepath = os.path.abspath(self.filename)
        self.tab_keys_dict = {'-tab2-': ['name', 'last_name'],
                              '-tab3-': ['name_PZLA_domtel', 'last_name_PZLA_domtel'],
                              '-tab4-': ['name_PZLA', 'last_name_PZLA'],
                              '-tab5-': ['name_startlist', 'last_name_startlist'],
                              '-tab6-': ['name_recent', 'last_name_recent']}


    def get_active_tab_and_add_to_fav(self, active_tab, values):
        match active_tab:
            case '-tab2-':
                self.first_last_name = encode_input(values, self.tab_keys_dict['-tab2-'][0],
                                                    self.tab_keys_dict['-tab2-'][1])
            case '-tab3-':
                self.first_last_name = encode_input(values, self.tab_keys_dict['-tab3-'][0],
                                                    self.tab_keys_dict['-tab3-'][1])
            case '-tab4-':
                self.first_last_name = encode_input(values, self.tab_keys_dict['-tab4-'][0],
                                                    self.tab_keys_dict['-tab4-'][1])
            case '-tab5-':
                self.first_last_name = encode_input(values, self.tab_keys_dict['-tab5-'][0],
                                                    self.tab_keys_dict['-tab5-'][1])
            case '-tab6-':
                self.first_last_name = encode_input(values, self.tab_keys_dict['-tab6-'][0],
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
        else:
            with open(self.filepath, "w", encoding='utf-8') as f:
                f.write(str(self.first_last_name) + "\n")

            print('Fav-folder created, athlete added')

def create_hints_lists():
    with open('fav.txt', 'r', encoding='utf-8') as f:
        options_all = [line.strip() for line in f]
        options_name = []
        options_last_name = []
        for option in options_all:
            options_name.append((option.partition(" "))[2])
            options_last_name.append((option.partition(" "))[0])
    print(options_all)
    print(options_name)
    print(options_last_name)
    return options_all


