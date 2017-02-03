#Seraphina Anderson, John Snow Labs, 9/1/2016

#General spider for crawling exit nodes

# -*- coding: utf-8 -*-
import scrapy
import re
import json
import csv
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from toripresbot.items import TorIpResolutionItem



class ExitNodes(CrawlSpider):
    name = "test1"
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        #url = 'https://torstatus.blutmagie.de/'
        #yield Request(url, callback=self.parse_exitnode_url)
        urls = ['https://torstatus.blutmagie.de/']
        #https://check.torproject.org/exit-addresses  #start with this one
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_exitnode_url)
            i += 1
        
    #length of each data column must be the same!
    #collect data [https://torstatus.blutmagie.de/: 7275]
    def parse_exitnode_url(self, response):
        item = TorIpResolutionItem()
        ###CREATE ITEM CONTAINER###
        dataRow = response.xpath('//tr[@class="r"]').extract()   #tot. 7105 data entries
        dataRow.remove(dataRow[0])


        ###GENERATE ITEM DETAILS###
        dataRow = [e.split('<td ') for e in dataRow]

        routerName = [re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]).group(1) if re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]) else 'Null' for k, e in enumerate(dataRow)]
        bandwidth = [re.match('.*title="(.*?)">', dataRow[k][2]).group(1) if re.match('.*title="(.*?)">', dataRow[k][2]) else 'Null' for k, e in enumerate(dataRow)]
        upTime = [re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) if re.match('.*>(.*?)<\/td>', dataRow[k][4]) else 'Null' for k, e in enumerate(dataRow)]
        hostName = [re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]).group(1) if re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]) else 'Null' for k, e in enumerate(dataRow)]
        

        ###LOOP THROUGH DATA FIELDS TO POPULATE ROWS FOR EACH DATA ITEM###
        i = 0
        while i < len(dataRow):
            #check length of all data fields to make sure consistent
            item['routerName'] = routerName[i]
            i += 1
            yield item







        
