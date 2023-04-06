import requests
from Table_class import Table

requested_html = requests.get(
    'https://hmps.domtel-sport.pl/?seria=0&dzien=2023-02-19&runda=3&konkurencja=M200&impreza=6')


event_results = Table(requested_html)
event_results.get_headers()
event_results.get_rows()




