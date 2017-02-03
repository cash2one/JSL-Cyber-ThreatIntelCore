#Seraphina Anderson,   John Snow Labs,    19/1/2016


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
    name = "platform"
   
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

        
    
        i = 0
        while i < len(fingerPrints):
            #generate URLs here, from fingerprints
            url = 'http://torstatus.rueckgr.at/router_detail.php?FP=' + str(fingerPrints[i])

            #item['exitUrl'] = 'https://globe.torproject.org/#/relay/' + str(fingerPrints[i]) #decision is to keep this hidden
            yield Request(url, callback=self.parse_fingerprints)
            i += 1

    def parse_fingerprints(self, response):
        item = TorIpResolutionItem()

        #get info container
        info1 = response.xpath('//td[@class="TRSB"]/text()').extract()
        
        ###GET LIST OF UNIQUE PLATFORMS###

        platformVersion = str(info1[8])

        item['platform']= str(info1[8])
        
        #platform = re.match('\s*(?:Tor\s*\d+\.\d+\.\d+\.\d+)\s*on\s*(.*)', info1[8]).group(1)

        #test for these...

        #Bitrig = 1
        #Windows Server Vista = 2
        #Windows Server 2003 = 3
        #Windows Server 2008 = 4
        #Windows Server 8 = 5
        #Windows Server 7 = 6
        #Windows Vista = 7
        #FreeBSD = 8
        #Windows XP = 9
        #OpenBSD = 10
        #Linux = 11
        #Windows 7 = 12
        #Windows 8 = 13
        #Mac OS X = 14

        if re.match('.*?(?:B|b)itrig.*', platformVersion):  #Bitrig = 1
            item['platformVersion'] = 1
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*V?v?ista|W?w?indows\s*V?v?ista\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server Vista = 2
            item['platformVersion'] = 2
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*2003|W?w?indows\s*2003\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 2003 = 3
            item['platformVersion'] = 3
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*2008|W?w?indows\s*2008\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 2008 = 4
            item['platformVersion'] = 4
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*8|W?w?indows\s*8\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 8 = 5
            item['platformVersion'] = 5
        elif re.match('.*?(?:W?w?indows\s*S?s?erver\s*7|W?w?indows\s*7\s*\[\s*?S?s?erver\s*.*\]?).*', platformVersion):  #Windows Server 7 = 6
            item['platformVersion'] =  6
        elif re.match('.*?W?w?indows\s*V?v?ista.*', platformVersion):  #Windows Vista = 7
            item['platformVersion'] = 7
        elif re.match('.*?(?:FreeBSD|Freebsd|freebsd|freeBSD|freeBsd).*', platformVersion):  #FreeBSD = 8
            item['platformVersion'] = 8
        elif re.match('.*?W?w?indows\s*(?:XP|Xp|xP|xp).*', platformVersion):  #Windows XP = 9
            item['platformVersion'] = 9
        elif re.match('.*?o?O?pen(?:BSD|bSD|bsD|bsd|Bsd).*', platformVersion):  #OpenBSD = 10
            item['platformVersion'] = 10
        elif re.match('.*(?:L?l?inux|LINUX).*', platformVersion):  #Linux = 11
            item['platformVersion'] = 11
        elif re.match('.*?W?w?indows\s*7.*', platformVersion):  #Windows 7 = 12
            item['platformVersion'] = 12
        elif re.match('.*?W?w?indows\s*8.*', platformVersion):  #Windows 8 = 13
            item['platformVersion'] = 13
        elif re.match('.*?(?:M?m?ac\s*OS\s*(?:x|X)|MAC\s*OS\s*(?:X|x)).*', platformVersion):  #Mac OS X = 14
            item['platformVersion'] = 14
        else:
            item['platformVersion'] = 15  #miscellaneous


        uptime = str(info1[10])

        ###WORK OUT UPTIME IN SECONDS###
        uptime = uptime.split(',')
        uptime = [re.match('.*?(\d+).*', e).group(1) for e in uptime if re.match('.*?(\d+).*', e)]
    
        #test: print "initially we get: " + "days: " + str(uptime[0]) + ", hours: " + str(uptime[1]) + ", minutes: " + str(uptime[2]) + ", seconds: " + str(uptime[3])

        a = int(uptime[0])
        b = int(uptime[1])
        c = int(uptime[2])
        d = int(uptime[3])

        days = 24*60*60
        hrs = 60*60
        mins = 60
        secs = 1

        time_in_seconds = (days*a) + (hrs*b) + (mins*c) + (secs*d)

        #test:
        #print "test: " + "days: " + str((days*a)) + " / " + str((days*a)/(days)), ", hrs: " + str((hrs*b)) + " / " + str((hrs*b)/hrs) + ", mins: " + str((mins*c)) + " / " + str((mins*c)/mins) + ", secs: " + str((secs*d)) + " / " + str((secs*d)/secs)


        item['upTimeSeconds'] = time_in_seconds

        
        yield item





        #dataset:
        #scrapy crawl platform -o platforms2a.csv