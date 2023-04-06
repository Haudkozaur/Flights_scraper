import requests
from Table_class import Table

requested_html = requests.get(
    'https://wmaci2023.domtel-sport.pl/?seria=0&runda=3&konkurencja=MTJ_35&dzien=&impreza=6')


event_results = Table(requested_html)
event_results.get_headers()
event_results.get_rows()
event_results.display_table()



