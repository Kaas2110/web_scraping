from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import json


class Parser_hh:
    def __init__(self, start_url,params, headers ):
        self.start_url = start_url
        self.params = params
        self.headers = headers
        self.info_vacancy = []

    def get_html_string(self, start_url, params, headers):
        try:
            response = requests.get(start_url, headers=headers, params=params)
            if response.ok:
                return response.text
        except Exception as e:
           sleep(1)
           print(e)
           return None

    @staticmethod
    def get_dom(get_html_string):

        return bs(get_html_string, "html.parser")

    def run(self):

        paginate = ''
        while paginate != None:
            if paginate == '':
                html_string = self.get_html_string(self.start_url + '/search/vacancy', self.headers, self.params)
            else:
                html_string = self.get_html_string(paginate)


            soup = Parser_hh.get_dom(html_string)
            vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
            self.get_info_from_element(vacancy_list)
            try:
                paginate = self.start_url + soup.find('a', attrs={'data-qa': 'pager-next'}).attrs['href']
            except Exception as e:
                print(e)
                paginate = None

    def get_info_from_element(self, vacancy_list):

        for vacance in vacancy_list:
            vacance_data = {}
            vacance_name = vacance.find('a', {'class': 'bloko-link'}).getText()
            vacance_link = vacance.find('a', {'class': 'bloko-link'}).attrs['href']
            vacance_data['Название вакансии'] = vacance_name
            vacance_data['Ссылка'] = vacance_link
            vacance_data['Источник'] = self.start_url
            self.get_salary(vacance_data, vacance)
            self.info_vacance.append(vacance_data)

    def get_salary(self, vacance_data, vacance):
        try:
            vacance_salary = vacance.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            vacance_salary = vacance_salary.replace('\u202f', '').spilit()
            if '-' in vacance_salary:
                vacance_data['мин. зарплата'] = float(vacance_salary[0])
                vacance_data['макс зарплата'] = float(vacance_salary[2])
                vacance_data['валюта'] = vacance_salary[-1]
            elif 'от' in vacance_salary:
                vacance_data['мин зарплата'] = float(vacance_salary[1])
                vacance_data['валюта'] = vacance_salary[-1]
            elif 'до' in vacance_salary:
                vacance_data['макс зарплата'] = float(vacance_salary[1])
                vacance_data['валюта'] = vacance_salary[-1]
        except Exception as e:
            vacance_data['зарплата'] = None

    def save_info_vacance(self):
        with open('vacance_hh.json', 'w', encoding='utf-8') as file:
            json.dump(self.info_vacancy, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_find = input('Введите вакансию:\n')
    main_link_hh = 'https://kemerovo.hh.ru/'
    params_main_hh = {'area': '4',
                      'fromSearchLine': 'true',
                      'st': 'searchVacancy',
                      'text': user_find,
                      'page': '0'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    scrapper = Parser_hh(main_link_hh, params_main_hh, headers)
    scrapper.run()
    scrapper.save_info_vacance()