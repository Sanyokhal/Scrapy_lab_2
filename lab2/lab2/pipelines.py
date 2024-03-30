# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from re import search
from scrapy.exceptions import DropItem
import mysql.connector
from lab2.items import Faculty, Kafedra, DetailedKafedra
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Lab2Pipeline:
    def process_item(self, item, spider):
        if isinstance(item, Faculty):
            return item
        if isinstance(item, Kafedra):
            kafedra = item.get('name')
            kafera = kafedra.replace("Кафедра | ", "")
            item['name'] = kafera
            return item
        if isinstance(item, DetailedKafedra):
            kafedra_name = item.get('name')
            kafedra_name = kafedra_name.replace('Детальна інформація по факультету | ', '')
            points = item.get('ects_credits')
            points = int(points.replace(' ECTS', ''))
            item['name'] = kafedra_name
            item['ects_credits'] = points
            return item


class MySqlPipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="scrapy_lab"
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        cafedry (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(255) NOT NULL,
            faculty VARCHAR(255) NOT NULL,
            speciality VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        detailed_info (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            faculty VARCHAR(255) NOT NULL,
            learn_form VARCHAR(255) NOT NULL,
            ects_credits VARCHAR(255) NOT NULL
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        faculties (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL
        )""")
        spider.logger.info("DB is ready ")

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL ")

    def process_item(self, item, spider):
        if isinstance(item, Kafedra):
            self.cursor.execute(
                "INSERT INTO cafedry (name, faculty,speciality,url) VALUES (%s, %s, %s, %s);",
                [item.get("name"), item.get("faculty"), item.get('speciality'), item.get('url')])
        if isinstance(item, Faculty):
            self.cursor.execute(
                "INSERT INTO faculties (name, url) VALUES (%s, %s);",
                [item.get("name"), item.get("url")])
        if isinstance(item, DetailedKafedra):
            self.cursor.execute(
                "INSERT INTO detailed_info (faculty, learn_form, ects_credits) VALUES (%s, %s, %s);",
                [item.get("name"), item.get('learn_form'), item.get("ects_credits")])
        self.connection.commit()
        return item
