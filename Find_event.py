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
        self.events_results_links_list = []
        self.events_names_list = []
        for j in range(0, len(self.events_links_list)):

            self.event_html = requests.get(self.events_links_list[j])
            self.event_html.encoding = 'utf-8'
            self.event_html_text = self.event_html.text
            self.bowl = BeautifulSoup(self.event_html_text, 'lxml')
            for i in self.bowl.find_all('h1', class_='small bold'):
                self.events_names_list.append(i.text)
            for x in self.bowl.find_all('a', class_='roundbutton2x font-12 yellowbut', href=True):
                self.events_results_links_list.append(x['href'])
        # print(self.events_names_list)
        # print(self.events_results_links_list)

    def get_competitions_urls(self):
        self.competitions_lists_list = []
        for i in range(0, len(self.events_results_links_list)):
            self.prefix = self.events_results_links_list[i].partition('.')
            self.competition_html = requests.get(self.events_results_links_list[i])
            self.competition_html.encoding = 'utf-8'
            self.competition_html_text = self.competition_html.text
            self.competitions = BeautifulSoup(self.competition_html_text, 'lxml')

            self.competitions_list = []
            for y in self.competitions.find_all('td', align=False, width=False):
                self.men = str(y).find('src="grafika/men_resize.jpg"')
                self.women = str(y).find('src="grafika/women_resize.jpg"')
                if self.men > 0:
                    for z in y.find_all('a', class_="konkur_przycisk2_wyniki", href=True):
                        if self.prefix[0] != 'https://online':
                            self.competitions_list.append([f'{z.text} M', f'{self.prefix[0]}.domtel-sport.pl/{z["href"]}'])
                        else:
                            self.competitions_list.append([
                                f'{z.text} M', f'{self.prefix[0]}.domtel-sport.pl/index2.php{z["href"]}'])
                elif self.women > 0:
                    for z in y.find_all('a', class_="konkur_przycisk2_wyniki", href=True):
                        if self.prefix[0] != 'https://online':
                            self.competitions_list.append([f'{z.text} K', f'{self.prefix[0]}.domtel-sport.pl/{z["href"]}'])
                        else:
                            self.competitions_list.append([
                                f'{z.text} K', f'{self.prefix[0]}.domtel-sport.pl/index2.php{z["href"]}'])
            # print(len(self.competitions_list))
            self.competitions_lists_list.append(self.competitions_list)
        # print(self.competitions_lists_list)

# hmp2023 = Links_Generator()
# hmp2023.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
# hmp2023.get_events_results_links()
# hmp2023.get_competitions_urls()
