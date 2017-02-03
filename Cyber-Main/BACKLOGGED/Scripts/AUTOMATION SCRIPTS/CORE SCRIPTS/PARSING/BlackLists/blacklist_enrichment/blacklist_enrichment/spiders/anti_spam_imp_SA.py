
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
from blacklist_enrichment.items import AntispamImpItem



class AntiSpamSpider(CrawlSpider):
    name = "antispam_imp"

    def start_requests(self):
        url  = 'http://antispam.imp.ch/spamlist'
        yield Request(url, callback=self.parse_antispam_imp)

      
    def parse_antispam_imp(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

       
        getall = response.xpath('//body').extract()
        getrows = getall[0].split('\n')
        cleanrows = [e for e in getrows if re.match('(\s*\d+).*', e)]
        getcells = [e.split('\t') for e in cleanrows]


        count = [e[0] for e in getcells] #[u'1',  => 0
        ip = [e[1] for e in getcells]    #u'1.0.252.96',  => 1
        unixtime = [e[2] for e in getcells]   #u'1456830327:',   => 2
        timestamp = [e[3] for e in getcells]   #u'Tue Mar  1 12:05:27 2016',  => 3
        hits = [re.match('\((.*?)\).*', e[4]).group(1) for e in getcells]       #u'(16.326)      => 4  
        host = [re.match('\((?:.*?)\)\s+(.*)', e[4]).group(1) for e in getcells]      #node-okg.pool-1-0.dynamic.totbb.net.',  => 4
  		

        
        for i, e in enumerate(count):
            item = AntispamImpItem()
            
            item['Count_Number'] = count[i]
            item['Address_IP'] = ip[i]
            item['Unix_Time'] = unixtime[i]
            item['Local_Timestamp'] = timestamp[i]
            item['Hits_Number'] = hits[i]
            item['Host_Name_Text'] = host[i]
			

            yield item

            #scrapy crawl antispam_imp -o antispam_imp_SA.csv

	
