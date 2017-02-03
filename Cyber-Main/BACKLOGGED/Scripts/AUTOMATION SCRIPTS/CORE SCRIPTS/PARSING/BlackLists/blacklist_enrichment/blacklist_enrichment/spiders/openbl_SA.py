# -*- coding: utf-8 -*-

import scrapy
import re
import json
import csv
import socket
from socket import getaddrinfo  #use to check for valid domain   => i.e. result = getaddrinfo("www.google.com", None)
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from blacklist_enrichment.items import MayhemListItem



class MayhemSpider(CrawlSpider):
    name = "openbl"

    def start_requests(self):
        url  = 'http://www.openbl.org/lists/base_all.txt'
        yield Request(url, callback=self.parse_sagadc)

      
    def parse_sagadc(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

        getall = response.xpath('//body').extract()
        getrows = getall[0].split('\n')
        
        ips = [re.match('\d+\.\d+\.\d+\.\d+', e).group(0) for e in getrows if re.match('\d+\.\d+\.\d+\.\d+', e)]
        

        
        
        for i, e in enumerate(ips):
            item = MayhemListItem()
            
            item['Address_IP'] = ips[i]

            yield item

            #scrapy crawl openbl -o openbl_SA.csv