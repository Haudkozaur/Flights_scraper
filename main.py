import requests
from Table_class import Table
from Find_event import Links_Generator
from GUI_display import GUI

last_ten_events = Links_Generator()
last_ten_events.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
last_ten_events.get_events_results_links()
last_ten_events.get_competitions_urls()

# print(last_ten_events.events_results_links_list)

GUI=GUI(last_ten_events.events_names_list,last_ten_events.competitions_lists_list)
GUI.display_basic()
if GUI.chosen_event!='xd':
    GUI.display_event_competitions_list()


    requested_html = requests.get(last_ten_events.competitions_lists_list[GUI.chosen_event][GUI.chosen_competition][1])
    #     'https://wmaci2023.domtel-sport.pl/?seria=0&runda=3&konkurencja=MTJ_35&dzien=&impreza=6')
    # print(last_ten_events.competitions_lists_list[GUI.chosen_event][GUI.chosen_competition])
    event_results = Table(requested_html)
    event_results.get_headers()
    event_results.get_rows()
    event_results.display_table()
