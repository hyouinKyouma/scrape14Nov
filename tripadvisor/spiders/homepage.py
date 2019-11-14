# -*- coding: utf-8 -*-
import scrapy


class HomepageSpider(scrapy.Spider):
    name = 'homepage'
    allowed_domains = ['https://www.tripadvisor.in/']
    start_urls = ['https://www.tripadvisor.in/']
    
    def __init__(self):
       self.city_no = 0
       self.hotel_no = 1
    
    def saveFiles(self,name,html_page):
        file = open(name,'w',encoding="utf-8")
        file.write(html_page)
        file.close()
        
    def hotelsHtml(self,response):
        file_name = "city"+str(self.city_no)+"hotel"+str(self.hotel_no)+'.html'
        self.saveFiles(file_name,response.text)
        
    def moveCity(self,response):
        hotel_links = response.xpath('//div[@class="listing_title"]/a/@href').extract()
        for hotel in hotel_links:
            yield scrapy.http.Request(url = response.urljoin(hotel),callback=self.hotelsHtml)
            self.hotel_no += 1
            
    
    def parse(self, response):
        all_hotels_in_cities = response.xpath('//div[@class="ui_columns"]/ul[@class="lst ui_column is-4"]/li[@class="item"]/a/@href')
        for cityHot in all_hotels_in_cities:
            yield scrapy.http.Request(url = response.urljoin(cityHot),callback=self.moveCity)
            self.city_no += 1
    
    
