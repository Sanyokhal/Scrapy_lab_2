import scrapy
from bs4 import BeautifulSoup
from lab2.items import Faculty, Kafedra, DetailedKafedra


class KarazinSpider(scrapy.Spider):
    name = "karazinCss"
    allowed_domains = ["start.karazin.ua"]
    start_urls = ["https://start.karazin.ua/programs"]

    def parse(self, response):
        faculties_list = response.css('ul.specialitys').css('a.flex-item')
        print(faculties_list)
        for faculty in faculties_list:
            link = ''
            faculty_name = faculty.css('div.text').text.replace(' ', ' ')
            print(faculty_name)
            yield Faculty(
                name=faculty_name,
                url=link
            )
            # yield scrapy.Request(
            #     url=link,
            #     callback=self.parse_faculty,
            #     meta={
            #         "faculty": faculty_name
            #     }
            # )

    # def parse_faculty(self, response):
    #     soup = BeautifulSoup(response.body, "html.parser")
    #     rows = soup.find('tbody', {'class': 'table-body'}).find_all('tr', {'class': 'row'})
    #     for row in rows:
    #         speciality = row.find('td', {'class': 'cell title'}).find('div', {'class': 'spec--title'}).text.split(': ')[
    #             1]
    #         url = row.find('td', {'class': 'cell title'}).find('a', {'class': 'program--link'})['href']
    #         url = f"https://start.karazin.ua{url}"
    #         name = row.find('td', {'class': 'cell title'}).find('a', {'class': 'program--link'}).text
    #         yield Kafedra(
    #             name=f"Кафедра | {name.capitalize()}",
    #             url=url,
    #             faculty=response.meta.get("faculty"),
    #             speciality=speciality
    #         )
    #         yield scrapy.Request(
    #             url=url,
    #             callback=self.parse_kafedra,
    #             meta={
    #                 "kafedra": name.capitalize()
    #             }
    #         )

    # def parse_kafedra(self, response):
    #     soup = BeautifulSoup(response.body, "html.parser")
    #     form = soup.find('div', {'class': 'training-program-container'}).find('div',
    #                                                                           {'class': 'stats table-cell'}).find(
    #         'label', {'class': 'pointer'}).text
    #     training_program = soup.find('div', {'class': 'training-program-container'})
    #     points = 'Не вказано'
    #     if training_program is not None:
    #         values = training_program.find('div', {'id': 'education-form--container-1'}).find_all('div',
    #                                                                                               {'class': 'value'})
    #         for value in values:
    #             if 'ECTS' in value.text:
    #                 points = value.text
    #
    #     yield DetailedKafedra(
    #         name=f"Детальна інформація по факультету | {response.meta.get('kafedra')}",
    #         learn_form=form,
    #         ects_credits=points
    #     )
