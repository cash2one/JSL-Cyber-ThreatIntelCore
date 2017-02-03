#Seraphina Anderson, John Snow Labs, 9/1/2016

#General spider for crawling exit node data embedded in awkward/inconsistent html code

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
    name = "toripres1a"
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        urls = ['https://torstatus.blutmagie.de']
        #https://check.torproject.org/exit-addresses  #start with this one
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_everything)
            i += 1
        
    #length of each data column must be the same!
    #collect data [https://torstatus.blutmagie.de/]
    def parse_everything(self, response):
        item = TorIpResolutionItem()
        ###CREATE ITEM CONTAINER###
        dataRow = response.xpath('//tr[@class="r"]').extract()
        dataRow.remove(dataRow[0])


        ###GENERATE ITEM DETAILS###
        dataRow = [e.split('<td ') for e in dataRow]



        #########version 2#######################################################################

        #routerName   #7125 - check length of each data field
        #can make into string afterwards,i.e. str(routername[0])
        routerName = [re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]).group(1) if re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]) else 'Null' for k, e in enumerate(dataRow)]
        #bandwidth
        bandwidth = [re.match('.*title="(.*?)">', dataRow[k][2]).group(1) if re.match('.*title="(.*?)">', dataRow[k][2]) else 'Null' for k, e in enumerate(dataRow)]
        
        #upTimeSeconds
        uptime = [re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) if re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) else '' for k, e in enumerate(dataRow)]
        nums = [re.match('.*?(\d+).*', e).group(1) for e in uptime]
        units = [re.match('\d+\s*?(\w+).*', e).group(1) for e in uptime]
        d = int(24*60*60)
        h = int(60*60)
        upTimeSeconds = [int(nums[i])*d if units[i] == 'd' else int(nums[i])*h for i, e in enumerate(uptime)]
        

        #hostName
        hostName = [re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]).group(1) if re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]) else 'Null' for k, e in enumerate(dataRow)]
        #ip
        ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else 'Null' for k, e in enumerate(dataRow)]
        #orPort
        orPort = ['Null' if dataRow[k][7] is None else re.match('.*>(\d+)<\/.*', dataRow[k][7]).group(1) for k, e in enumerate(dataRow)]
        #dirPort
        dirPort = ['Null' if not re.match('.*?(\d+).*', dataRow[k][8]) else re.match('.*?(\d+).*', dataRow[k][8]).group(1) for k, e in enumerate(dataRow)]
        #firstSeen
        firstSeen = [re.match('.*?>(\d{4}-\d{2}-\d{2}).*', dataRow[k][10]).group(1) if re.match('.*?>(\d{4}-\d{2}-\d{2}).*', dataRow[k][10]) else  'Null' for k, e in enumerate(dataRow)]
        #asName
        asName = [re.match('.*>(.*?)(?:<\/b>)?\/td>', dataRow[k][11]).group(1) if re.match('.*>(.*?)(?:<\/b>)?\/td>', dataRow[k][11]) else 'Null' for k, e in enumerate(dataRow)]
        #asNumber
        asNumber = [re.match('.*?(\d+).*', dataRow[k][12]).group(1) if re.match('.*?(\d+).*', dataRow[k][12]) else 'Null' for k, e in enumerate(dataRow)]
        #consensusBandwidth
        consensusBandwidth = [re.match('.*?(\d+).*', dataRow[k][13]).group(1) if re.match('.*?(\d+).*', dataRow[k][13]) else 'Null' for k, e in enumerate(dataRow)]
        #orAddress
        orAddress = [re.match('.*?(\[.*?\]\s*:\s*\d+).*', dataRow[k][14]).group(1) if re.match('.*?(\[.*?\]\s*:\s*\d+).*', dataRow[k][14]) else 'Null' for k, e in enumerate(dataRow)]

        ###LOOP THROUGH DATA FIELDS TO POPULATE ROWS FOR EACH DATA ITEM###
        i = 0
        for e in routerName:
            #check length of all data fields to make sure consistent
            item['routerName'] = routerName[i]
            item['bandwidth'] = bandwidth[i]
            item['upTimeSeconds'] = upTimeSeconds[i]
            item['hostName'] = hostName[i]
            item['orPort'] = orPort[i]
            item['dirPort'] = dirPort[i]
            item['firstSeen'] = firstSeen[i]
            item['asName'] = asName[i]
            item['asNumber'] = asNumber[i]
            item['consensusBandwidth'] = consensusBandwidth[i]
            item['orAddress'] = orAddress[i]
            #item['whoIs'] = 'https://who.is/whois-ip/ip-address/' + str(ip[i])
            item['ip'] = ip[i]
            item['sourceName'] = 'tordata2'
            yield item
            i += 1
            
###CSV files generated###
            
#scrapy crawl exitnodes1 -o tor_exit_addresses1a.csv  #https://torstatus.blutmagie.de
