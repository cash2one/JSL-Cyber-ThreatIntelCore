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

#Note:
#'https://check.torproject.org/exit-addresses' => torProject4.py
#'https://torstatus.blutmagie.de' => whoIs2a.py


class ExitNodes(CrawlSpider):
    name = "tortest1"
   
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #url = 'https://check.torproject.org/exit-addresses'
        #yield Request(url, callback=self.parse_exitUrl)
        #test urls - feed all data sources here
        #Do we want to process one URL at a time, or loop through them here?
        urls = ['https://check.torproject.org/exit-addresses', 'https://torstatus.blutmagie.de']
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_Url)
            i += 1

    #tot. no. of data items: 1156
    def parse_Url(self, response):
        #get url, so we can test where to go...
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        if 'https://check.torproject.org/exit-addresses' in url:
            data = response.xpath('//body//text()').extract()
        
            ###CREATE ITEM CONTAINER###
            entries = data[0].split('ExitNode')  
            entries.remove(entries[0])

            ###COLLECT DATA FOR EACH DATA FIELD###
            fingerPrints = [re.match('\s*(.*?)\\nPublished.*', str(e)).group(1) for e in entries if re.match('\s*(.*?)\\nPublished.*', e)]
            i = 0
            while i < len(fingerPrints):
                item = TorIpResolutionItem()
                #generate URLs here, from fingerprints
                url = 'http://torstatus.rueckgr.at/router_detail.php?FP=' + str(fingerPrints[i])
                item['fingerPrint'] = fingerPrints[i]
                item['sourceName'] = "routeA"
                print "testing: ", url
                yield Request(url, callback=self.parse_data1, meta=dict(item=item))
                i += 1
                
        else:
            item = TorIpResolutionItem()
            url = 'https://torstatus.blutmagie.de'
            item['fingerPrint'] = ''
            item['sourceName'] = "routeB"
            print "testing: ", url
            yield Request(url, callback=self.parse_data1, meta=dict(item=item))


    def parse_data1(self, response):
        item = response.meta['item']
        #get url for testing where to go
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        if 'http://torstatus.rueckgr.at/router_detail.php' in url:
            info1 = response.xpath('//td[@class="TRSB"]/text()').extract()
            item['orgName'] = "routeA"
            ip = str(info1[3])
            item['ip'] = str(info1[3])
            url = 'http://whois.ipchecker.info/' + str(ip)
            print "testing: ", url
            yield Request(url, callback=self.parse_whois_data, meta=dict(item=item))
        else:
            dataRow = response.xpath('//tr[@class="r"]').extract()
            dataRow.remove(dataRow[0])
            dataRow = [e.split('<td ') for e in dataRow]
            ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
            i = 0
            while i < len(ip):
                item['ip'] = ip[i]
                url = 'http://whois.ipchecker.info/' + str(ip[i])
                item['orgName'] = "routeB"
                print "testing: ", url
                yield Request(url, callback=self.parse_whois_data, meta=dict(item=item))
                i += 1


    def parse_whois_data(self, response):
        item = response.meta['item']
        get = response
        url = re.match('<200\s*(.*?)>', str(get)).group(1)
        item['orgType'] = "we made it!!!!"
        print "testing: ", url
        yield item
