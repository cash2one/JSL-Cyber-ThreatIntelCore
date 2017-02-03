#Seraphina Anderson, John Snow Labs, 16/1/2016

#Spider for generating WhoIs URLs and scraping the corresponding data

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
    name = "toripres8a"
    #create list of keywords, and loop through searches here
    def start_requests(self):
        #loop through different urls, for IP addresses
        urls = ['https://torstatus.blutmagie.de']
        #https://check.torproject.org/exit-addresses  #start with this one
        i = 0
        while i < len(urls):
            url = urls[i]
            yield Request(url, callback=self.parse_startingpoint)
            i += 1
        

    def parse_startingpoint(self, response):
        ###CREATE ITEM CONTAINER###
        dataRow = response.xpath('//tr[@class="r"]').extract()
        dataRow.remove(dataRow[0])


        ###generate item containers#################
        dataRow = [e.split('<td ') for e in dataRow]

        ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
        routerName = [re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]).group(1) if re.match('.*>(.*?)<\/a><\/td>', dataRow[k][1]) else '' for k, e in enumerate(dataRow)]
        #bandwidth
        bandwidth = [re.match('.*title="(.*?)">', dataRow[k][2]).group(1) if re.match('.*title="(.*?)">', dataRow[k][2]) else '' for k, e in enumerate(dataRow)]
        
        #upTimeSeconds
        uptime = [re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) if re.match('.*>(.*?)<\/td>', dataRow[k][4]).group(1) else '' for k, e in enumerate(dataRow)]
        nums = [re.match('.*?(\d+).*', e).group(1) for e in uptime]
        units = [re.match('\d+\s*?(\w+).*', e).group(1) if re.match('\d+\s*?(\w+).*', e) else '' for e in uptime]
        d = int(24*60*60)
        h = int(60*60)
        #test for units
        upTimeSeconds = [int(nums[i])*d if units[i] == 'd' else int(nums[i])*h for i, e in enumerate(uptime)]

        #hostName
        hostName = [re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]).group(1) if re.match('.*?class="iT">(.*?)\s*\[.*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
        #ip
        ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else '' for k, e in enumerate(dataRow)]
        #orPort
        orPort = ['' if dataRow[k][7] is None else re.match('.*>(\d+)<\/.*', dataRow[k][7]).group(1) for k, e in enumerate(dataRow)]
        #dirPort
        dirPort = ['' if not re.match('.*?(\d+).*', dataRow[k][8]) else re.match('.*?(\d+).*', dataRow[k][8]).group(1) for k, e in enumerate(dataRow)]
        #firstSeen
        firstSeen = [re.match('.*?>(\d{4}-\d{2}-\d{2}).*', dataRow[k][10]).group(1) if re.match('.*?>(\d{4}-\d{2}-\d{2}).*', dataRow[k][10]) else  '' for k, e in enumerate(dataRow)]
        #asName
        asName = [re.match('.*>(.*?)(?:<\/b>)?\/td>', dataRow[k][11]).group(1) if re.match('.*>(.*?)(?:<\/b>)?\/td>', dataRow[k][11]) else '' for k, e in enumerate(dataRow)]
        #asNumber
        asNumber = [re.match('.*?(\d+).*', dataRow[k][12]).group(1) if re.match('.*?(\d+).*', dataRow[k][12]) else '' for k, e in enumerate(dataRow)]
        #consensusBandwidth
        consensusBandwidth = [re.match('.*?(\d+).*', dataRow[k][13]).group(1) if re.match('.*?(\d+).*', dataRow[k][13]) else '' for k, e in enumerate(dataRow)]
        #orAddress
        orAddress = [re.match('.*?(\[.*?\]\s*:\s*\d+).*', dataRow[k][14]).group(1) if re.match('.*?(\[.*?\]\s*:\s*\d+).*', dataRow[k][14]) else '' for k, e in enumerate(dataRow)]

        ###LOOP THROUGH DATA FIELDS TO POPULATE ROWS FOR EACH DATA ITEM###
        i = 0
        while i < len(ip):
            item = TorIpResolutionItem()
            ###GENERATE WHOIS URLS###
            url = 'http://whois.ipchecker.info/' + str(ip[i])
            item['ip'] = ip[i] #parse this itemfield
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
            yield Request(url, callback=self.parse_whois_data, meta=dict(item=item))
            i += 1
        

    def parse_whois_data(self, response):
        item = response.meta['item']
        
##        ###TEST FUNCTIONALITY - return corresponding url###
##        get_url = response #this gets us current URL crawling!
##        url = re.match('<200\s*(.*?)>', str(get_url)).group(1) #some tidying up
##        item['whoIs'] = url
        ###TEST FOR "INTERNAL SERVER ERROR"###
        #<h1>Internal Server Error</h1>
        
        #get LHS data
        results = response.xpath('//pre1').extract()
        if response.xpath('//pre1').re('.*?inetnum:\s*(.*)'):
            item['inetNum'] = response.xpath('//pre1').re('.*?inetnum:\s*(.*)')
            #inetNum = str(inetNum[0])

        if response.xpath('//pre1').re('.*?netname:\s*(.*)'):
            item['netName'] = response.xpath('//pre1').re('.*?netname:\s*(.*)')
            #netName = str(netName[0])

        if response.xpath('//pre1').re('.*?descr:\s*(.*)'):
            item['description'] = response.xpath('//pre1').re('.*?descr:\s*(.*)')
            #description = str(description[0])

        if response.xpath('//pre1').re('.*?admin-?c:\s*(.*)'):
            item['adminc'] = response.xpath('//pre1').re('.*?admin-?c:\s*(.*)')
            #adminc = str(adminc[0])

        if response.xpath('//pre1').re('.*?tech-?c:\s*(.*)'):
            item['techc'] = response.xpath('//pre1').re('.*?tech-?c:\s*(.*)')
            #techc = str(techc[0])

        if response.xpath('//pre1').re('.*?status:\s*(.*)'):
            item['status'] = response.xpath('//pre1').re('.*?status:\s*(.*)')
            #status = str(status[0])

        if response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)'):
            item['mntby'] = response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)')
            #mntby = str(mntby[0])

        if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['datePublished'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
            #datePublished = str(datePublished[0])

        if response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['timePublished'] = response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #timePublished = str(timePublished[0])

        if response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['lastStatusDate'] = response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*') #last-modified
            #lastStatusDate = str(lastStatusDate[0])

        if response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['lastStatusTime'] = response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #lastStatusTime = str(lastStatusTime[0])

        if response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)'):
            item['organisation'] = response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)')
            #organisation = str(organisation[0])

        if response.xpath('//pre1').re('.*?org-name:\s*(.*)'):
            orgName = response.xpath('//pre1').re('.*?org-?name:\s*(.*)')
            item['orgName'] = orgName #str(orgName[0])

        if response.xpath('//pre1').re('.*?org-type:\s*(.*)'):
            orgType = response.xpath('//pre1').re('.*?org-?type:\s*(.*)')
            item['orgType'] = orgType#str(orgType[0])

        if response.xpath('//pre1').re('.*?remarks:\s*(.*)'):
            remarks = response.xpath('//pre1').re('.*?remarks:\s*(.*)')
            item['remarks'] = remarks #str(remarks[0])

        if response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)'):
            mntRef = response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)')
            item['mntRef'] = mntRef#str(mntRef[0])

        if response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)'):
            abuseC = response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)')
            item['abuseC'] = abuseC #str(abuseC[0])

        if response.xpath('//pre1').re('.*?person:\s*(.*)'):
            person = response.xpath('//pre1').re('.*?person:\s*(.*)')
            item['person'] = person#str(person[0])

        if response.xpath('//pre1').re('.*?address:\s*(.*)'):
            postalAddress = response.xpath('//pre1').re('.*?address:\s*(.*)')
            item['postalAddress'] = [str(e) for e in postalAddress]

        if response.xpath('//pre1').re('.*?phone:\s*(.*)'):
            phone = response.xpath('//pre1').re('.*?phone:\s*(.*)')
            item['phone'] = [str(e) for e in phone]

        if response.xpath('//pre1').re('.*?fax-?no:\s*(.*)'):
            faxNo = response.xpath('//pre1').re('.*?fax-?no:\s*(.*)')
            item['faxNo'] = [str(e) for e in faxNo]

        if response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)'):
            nicHdl = response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)')
            item['nicHdl'] = [str(e) for e in nicHdl]

        if response.xpath('//pre1').re('.*?route:\s*(.*)'):
            route = response.xpath('//pre1').re('.*?route:\s*(.*)')
            item['route'] = route#str(route[0])

        if response.xpath('//pre1').re('.*?origin:\s*(.*)'):
            origin = response.xpath('//pre1').re('.*?origin:\s*(.*)')
            item['origin'] = origin#str(origin[0])

        if response.xpath('//pre1').re('.*?member-?of:\s*(.*)'):
            memberOf = response.xpath('//pre1').re('.*?member-?of:\s*(.*)')
            item['memberOf'] = memberOf#str(memberOf[0])



        ###IP LOCATION###
        #get all location info
        location = response.xpath('//div[@class="span6"]//p//text()').extract()
        #populate data fields
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)'):
            item['country'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)')

        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)'):
            latitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)')
            item['latitude'] = str(latitude[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)'):
            longitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)')
            item['longitude'] = str(longitude[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)'):
            callingCode = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)')
            item['callingCode'] = str(callingCode[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)'):
            currency = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)')
            item['currency'] = str(currency[0])

        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)'):
            item['capital'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)')

        if response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)'):
            item['region'] = response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)')

        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)'):
            item['language'] = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)')


        item['sourceName'] = 'tordata5'
            
        yield item




###LIST OF ASSOCIATED CSVs###
#1 scrapy crawl toripres8a -o TOR_IP_RESOLUTION_08c2.csv


#debugging:
###ascii problems: country, address###
        




        
        

