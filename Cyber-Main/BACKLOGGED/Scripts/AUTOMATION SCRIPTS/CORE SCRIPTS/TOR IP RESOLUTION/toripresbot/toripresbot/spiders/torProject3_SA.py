#Seraphina Anderson, John Snow Labs, 13/1/2016

#Spider for generating for just scraping https://check.torproject.org/exit-addresses data


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
    name = "toripre5a"
   
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #url = 'https://check.torproject.org/exit-addresses'
        #yield Request(url, callback=self.parse_exitUrl)
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        urls = ['https://check.torproject.org/exit-addresses']
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_torProjectUrl)
            i += 1

    #tot. no. of data items: 1156
    def parse_torProjectUrl(self, response):
        #item = ExitNodesItem()
        data = response.xpath('//body//text()').extract()
        
        ###CREATE ITEM CONTAINER###
        entries = data[0].split('ExitNode')  
        entries.remove(entries[0])

        ###COLLECT DATA FOR EACH DATA FIELD###
        fingerPrints = [re.match('\s*(.*?)\\nPublished.*', str(e)).group(1) for e in entries if re.match('\s*(.*?)\\nPublished.*', e)]
        datepublished = [re.match('\s*.*?\\nPublished\s*(\d{4}-\d{2}-\d{2})\s*.*', str(e)).group(1) for e in entries if re.match('\s*.*?\\nPublished\s*(\d{4}-\d{2}-\d{2})\s*.*', e)]
        timepublished = [re.match('\s*.*?\\nPublished\s*\d{4}-\d{2}-\d{2}\s*?(\d{2}:\d{2}:\d{2}).*', str(e)).group(1) for e in entries if re.match('\s*.*?\\nPublished\s*\d{4}-\d{2}-\d{2}\s*?(\d{2}:\d{2}:\d{2}).*', e)]
        laststatusdate = [re.match('.*?\\n.*?\\nLastStatus\s*?(\d{4}-\d{2}-\d{2}).*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\nLastStatus\s*?(\d{4}-\d{2}-\d{2}).*', e)]
        laststatustime = [re.match('.*?\\n.*?\\nLastStatus\s*?\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\nLastStatus\s*?\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', e)]
        exitaddress = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*(\d+\.\d+\.\d+\.\d+)\s*.*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*(\d+\.\d+\.\d+\.\d+)\s*.*', e)]
        exitaddressdate = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*(\d{4}-\d{2}-\d{2})\s*.*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*(\d{4}-\d{2}-\d{2})\s*.*', e)]
        exitaddresstime = [re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', str(e)).group(1) for e in entries if re.match('.*?\\n.*?\\n.*?\\nExitAddress\s*\d+\.\d+\.\d+\.\d+\s*\d{4}-\d{2}-\d{2}\s*(\d{2}:\d{2}:\d{2}).*', e)]


        
    
        i = 0
        while i < len(fingerPrints):
            item = TorIpResolutionItem()
            #generate URLs here, from fingerprints
            url = 'http://torstatus.rueckgr.at/router_detail.php?FP=' + str(fingerPrints[i])
            item['fingerPrint'] = fingerPrints[i]
            #item['whoIs'] = urls[i]
            item['datePublished'] = datepublished[i]
            item['timePublished'] = timepublished[i]
            item['lastStatusDate'] = laststatusdate[i]
            item['lastStatusTime'] = laststatustime[i]
            item['exitAddress'] = exitaddress[i]
            item['exitAddressDate'] = exitaddressdate[i]
            item['exitAddressTime'] = exitaddresstime[i]
            #item['exitUrl'] = 'https://globe.torproject.org/#/relay/' + str(fingerPrints[i]) #decision is to keep this hidden
            yield item
            i += 1




#scrapy crawl exitnodes4 -o tor_exit_addresses2a.csv




            
