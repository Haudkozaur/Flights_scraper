import requests
from bs4 import BeautifulSoup


class Links_Generator():
    def get_events_links(self, events_calendar_url):
        self.events_calendar_url = events_calendar_url
        self.events_calendar_html = requests.get(self.events_calendar_url)
        self.events_calendar_html.encoding = 'utf-8'
        self.events_calendar_html_text = self.events_calendar_html.text
        self.bigos = BeautifulSoup(self.events_calendar_html_text, 'lxml')
        self.events_id_list = []
        for a in self.bigos.find_all('a', class_='roundbutton darkblue', href=True):
            self.events_id_list.append(a['href'])

        self.events_links_list = []
        for i in range(0, len(self.events_id_list)):
            self.events_links_list.append(f'https://domtel-sport.pl/{self.events_id_list[i]}')

    def get_events_results_links(self):
        self.events_results_links_list=[]
        for j in range(0,len(self.events_links_list)):
            self.event_html = requests.get(self.events_links_list[j])
            self.event_html.encoding = 'utf-8'
            self.event_html_text = self.event_html.text
            self.bowl = BeautifulSoup(self.event_html_text, 'lxml')

            for x in self.bowl.find_all('a', class_='roundbutton2x font-12 yellowbut', href=True):

                self.events_results_links_list.append(x['href'])



# hmp2023 = Links_Generator()
# hmp2023.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
# hmp2023.get_events_results_links()