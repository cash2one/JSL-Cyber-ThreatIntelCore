###mayhem data, Seraphina Anderson, John Snow Labs, 26/2/2016###

#test for errors: http://stackoverflow.com/questions/22851609/python-errno-11001-getaddrinfo-failed


# try:
#     print gi.country_code_by_name('specificdownload.com')
# except Exception, e:
#     print type(e)
#     print e



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
    name = "mayhem"

    def start_requests(self):
        url  = 'http://secure.mayhemiclabs.com/malhosts/malhosts.txt'
        yield Request(url, callback=self.parse_mayhem)

      
    def parse_mayhem(self, response):
        get_url = response #this gets us current URL crawling!
        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up

        getall = response.xpath('//body').extract()
        getrows = getall[0].split('\n')
        #filter out unwanted rows
        clean = [e for e in getrows if '#' not in e]
        clean = [e for e in clean if re.match('^.*?\w+.*$', e)]
        separate_columns = [e.split('\t') for e in clean]
        clean_blank_rows = [e for e in separate_columns if '' not in e]
        data = clean_blank_rows

        #data fields
        #sample data item:  [u'039b1ee.netsolhost.com', u'ZeuS/WNSPoem/ZBot', u'ZT', u'0']
        
        for i, e in enumerate(data):
            item = MayhemListItem()
            domain_name = data[i][0]

            try:
                ip_address = socket.gethostbyname(str(domain_name))
            except socket.gaierror:
                ip_address = ''

                
            item['Address_IP'] = ip_address
            item['Domain_Name'] = data[i][0]
            item['Malware_Types_List'] = data[i][1]
            blacklist_type = data[i][2]
            if blacklist_type == 'ZT':
                blacklist_type = 'Zeus Tracker Domain Blocklist (ZT)'
            if blacklist_type == 'MDL':
                blacklist_type = 'Malware Domain List Hosts List (MDL)'
            if blacklist_type == 'PT':
                blacklist_type = 'Palevo Tracker Domain Blocklist (PT)'

            item['Blacklist_Type_Text'] = blacklist_type
        

            yield item

            #scrapy crawl mayhem -o mayhem2_SA.csv



            #map blackists as follows:
    #Zeus Tracker Domain Blocklist (ZT)                                         #
    # - https://zeustracker.abuse.ch/blocklist.php                               #
    # MalwareDomainList.com Hosts List (MDL)                                     #
    # - http://www.malwaredomainlist.com/hostslist/hosts.txt                     #
    # Palevo Tracker Domain Blocklis (PT)                                        #
    # - https://palevotracker.abuse.ch/blocklists.php                            #
    # Palevo Tracker Domain Blocklis (PT)                                        #
    # - https://palevotracker.abuse.ch/blocklists.php     