import PySimpleGUI as sg
from request_func import get_request


class Links_Generator():
    def get_events_links(self, events_calendar_url):
        self.bigos = get_request(events_calendar_url, 'utf-8')
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
            self.bowl = get_request(self.events_links_list[j], 'utf-8')
            for i in self.bowl.find_all('h1', class_='small bold'):
                self.events_names_list.append(i.text)
            if self.bowl.find_all('a', class_='roundbutton2x font-12 yellowbut', href=True) != []:
                for x in self.bowl.find_all('a', class_='roundbutton2x font-12 yellowbut', href=True):
                    self.events_results_links_list.append(x['href'])
            else:
                self.events_results_links_list.append('')
        self.events_dict = {key: value for key, value in zip(self.events_results_links_list, self.events_names_list)}
        # print(self.events_dict)

    def get_competitions_urls(self):
        self.competitions_lists_list = []
        for i in range(0, len(self.events_results_links_list)):
            self.prefix = self.events_results_links_list[i].partition('.')
            if self.events_results_links_list[i] != '':
                self.competitions = get_request(self.events_results_links_list[i], 'utf-8')
                self.competitions_list = []
                for y in self.competitions.find_all('td', align=False, width=False):
                    self.men = str(y).find('src="grafika/men_resize.jpg"')
                    self.women = str(y).find('src="grafika/women_resize.jpg"')
                    if self.men > 0:
                        for z in y.find_all('a', class_="konkur_przycisk2_wyniki", href=True):
                            if self.prefix[0] != 'https://online':
                                self.competitions_list.append(
                                    [f'{z.text} M', f'{self.prefix[0]}.domtel-sport.pl/{z["href"]}'])
                            else:
                                self.competitions_list.append([
                                    f'{z.text} M', f'{self.prefix[0]}.domtel-sport.pl/index2.php{z["href"]}'])
                    elif self.women > 0:
                        for z in y.find_all('a', class_="konkur_przycisk2_wyniki", href=True):
                            if self.prefix[0] != 'https://online':
                                self.competitions_list.append(
                                    [f'{z.text} K', f'{self.prefix[0]}.domtel-sport.pl/{z["href"]}'])
                            else:
                                self.competitions_list.append([
                                    f'{z.text} K', f'{self.prefix[0]}.domtel-sport.pl/index2.php{z["href"]}'])
            else:
                self.competitions_list = []
            self.competitions_lists_list.append(self.competitions_list)


# test = Links_Generator()
# test.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
# test.get_events_results_links()
# test.get_competitions_urls()


