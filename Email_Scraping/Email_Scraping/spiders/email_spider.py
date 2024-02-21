
# web scraping framework
import scrapy
# for regular expression
import re
# for selenium request
from scrapy_selenium import SeleniumRequest
# for link extraction
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class EmailSpider(scrapy.Spider):

    name = 'email'

    def start_requests(self):
        

    def parse(scrapy, spider):
        pass