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
    name = "toripres7b"
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


        ###GENERATE WHOIS URLS###
        dataRow = [e.split('<td ') for e in dataRow]
        ip = [re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]).group(1) if re.match('.*?whois.pl\?ip=(.*?)?".*', dataRow[k][6]) else 'Null' for k, e in enumerate(dataRow)]
        i = 0
        while i < len(ip):
            item = TorIpResolutionItem()
            url = 'http://whois.ipchecker.info/' + str(ip[i])
            item['ip'] = ip[i] #parse this itemfield
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
        else:
            item['inetNum'] = 'Null'
        if response.xpath('//pre1').re('.*?netname:\s*(.*)'):
            item['netName'] = response.xpath('//pre1').re('.*?netname:\s*(.*)')
            #netName = str(netName[0])
        else:
            item['netName'] = 'Null'
        if response.xpath('//pre1').re('.*?descr:\s*(.*)'):
            item['description'] = response.xpath('//pre1').re('.*?descr:\s*(.*)')
            #description = str(description[0])
        else:
            item['description'] = 'Null'
        if response.xpath('//pre1').re('.*?admin-?c:\s*(.*)'):
            item['adminc'] = response.xpath('//pre1').re('.*?admin-?c:\s*(.*)')
            #adminc = str(adminc[0])
        else:
            item['adminc'] = 'Null'
        if response.xpath('//pre1').re('.*?tech-?c:\s*(.*)'):
            item['techc'] = response.xpath('//pre1').re('.*?tech-?c:\s*(.*)')
            #techc = str(techc[0])
        else:
            item['techc'] = 'Null'
        if response.xpath('//pre1').re('.*?status:\s*(.*)'):
            item['status'] = response.xpath('//pre1').re('.*?status:\s*(.*)')
            #status = str(status[0])
        else:
            item['status'] = 'Null'
        if response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)'):
            item['mntby'] = response.xpath('//pre1').re('.*?mnt-?by:\s*(.*)')
            #mntby = str(mntby[0])
        else:
            item['mntby'] = 'Null'
        if response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['datePublished'] = response.xpath('//pre1').re('.*?created:\s*(\d{4}-\d{2}-\d{2}).*')  #created
            #datePublished = str(datePublished[0])
        else:
            item['datePublished'] = 'Null'
        if response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['timePublished'] = response.xpath('//pre1').re('.*?created:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #timePublished = str(timePublished[0])
        else:
            item['timePublished'] = 'Null'
        if response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*'):
            item['lastStatusDate'] = response.xpath('//pre1').re('.*?last-?modified:\s*(\d{4}-\d{2}-\d{2}).*') #last-modified
            #lastStatusDate = str(lastStatusDate[0])
        else:
            item['lastStatusDate'] = 'Null'
        if response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)'):
            item['lastStatusTime'] = response.xpath('//pre1').re('.*?last-?modified:\s*\d{4}-\d{2}-\d{2}(.\d+:\d+:\d+.)')
            #lastStatusTime = str(lastStatusTime[0])
        else:
            item['lastStatusTime'] = 'Null'
        if response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)'):
            item['organisation'] = response.xpath('//pre1').re('.*?org(:?anisation)?\s*(.*)')
            #organisation = str(organisation[0])
        else:
            item['organisation'] = 'Null'
        if response.xpath('//pre1').re('.*?org-name:\s*(.*)'):
            orgName = response.xpath('//pre1').re('.*?org-?name:\s*(.*)')
            item['orgName'] = orgName #str(orgName[0])
        else:
            item['orgName'] = 'Null'
        if response.xpath('//pre1').re('.*?org-type:\s*(.*)'):
            orgType = response.xpath('//pre1').re('.*?org-?type:\s*(.*)')
            item['orgType'] = orgType#str(orgType[0])
        else:
            item['orgType'] = 'Null'
        if response.xpath('//pre1').re('.*?remarks:\s*(.*)'):
            remarks = response.xpath('//pre1').re('.*?remarks:\s*(.*)')
            item['remarks'] = remarks #str(remarks[0])
        else:
            item['remarks'] = 'Null'
        if response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)'):
            mntRef = response.xpath('//pre1').re('.*?mnt-ref:\s*(.*)')
            item['mntRef'] = mntRef#str(mntRef[0])
        else:
            item['mntRef'] = 'Null'
        if response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)'):
            abuseC = response.xpath('//pre1').re('.*?abuse-?c:\s*(.*)')
            item['abuseC'] = abuseC #str(abuseC[0])
        else:
            item['abuseC'] = 'Null'
        if response.xpath('//pre1').re('.*?person:\s*(.*)'):
            person = response.xpath('//pre1').re('.*?person:\s*(.*)')
            item['person'] = person#str(person[0])
        else:
            item['person'] = 'Null'
        if response.xpath('//pre1').re('.*?address:\s*(.*)'):
            postalAddress = response.xpath('//pre1').re('.*?address:\s*(.*)')
            item['postalAddress'] = [str(e) for e in postalAddress]
        else:
            item['postalAddress'] = 'Null'
        if response.xpath('//pre1').re('.*?phone:\s*(.*)'):
            phone = response.xpath('//pre1').re('.*?phone:\s*(.*)')
            item['phone'] = [str(e) for e in phone]
        else:
            item['phone'] = 'Null'
        if response.xpath('//pre1').re('.*?fax-?no:\s*(.*)'):
            faxNo = response.xpath('//pre1').re('.*?fax-?no:\s*(.*)')
            item['faxNo'] = [str(e) for e in faxNo]
        else:
            item['faxNo'] = 'Null'
        if response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)'):
            nicHdl = response.xpath('//pre1').re('.*?nic-?hdl:\s*(.*)')
            item['nicHdl'] = [str(e) for e in nicHdl]
        else:
            item['nicHdl'] = 'Null'
        if response.xpath('//pre1').re('.*?route:\s*(.*)'):
            route = response.xpath('//pre1').re('.*?route:\s*(.*)')
            item['route'] = route#str(route[0])
        else:
            item['route'] = 'Null'
        if response.xpath('//pre1').re('.*?origin:\s*(.*)'):
            origin = response.xpath('//pre1').re('.*?origin:\s*(.*)')
            item['origin'] = origin#str(origin[0])
        else:
            item['origin'] = 'Null'
        if response.xpath('//pre1').re('.*?member-?of:\s*(.*)'):
            memberOf = response.xpath('//pre1').re('.*?member-?of:\s*(.*)')
            item['memberOf'] = memberOf#str(memberOf[0])
        else:
            item['memberOf'] = 'Null'


        ###IP LOCATION###
        #get all location info
        location = response.xpath('//div[@class="span6"]//p//text()').extract()
        #populate data fields
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)'):
            item['country'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?ountry:\s*(.*)')
        else:
            item['country'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)'):
            latitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?atitude:\s*(.*)')
            item['latitude'] = str(latitude[0])
        else:
            item['latitude'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)'):
            longitude = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?ongitude:\s*(.*)')
            item['longitude'] = str(longitude[0])
        else:
            item['longitude'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)'):
            callingCode = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?alling\s*Code:\s*(.*)')
            item['callingCode'] = str(callingCode[0])
        else:
            item['callingCode'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)'):
            currency = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?urrency:\s*(.*)')
            item['currency'] = str(currency[0])
        else:
            item['currency'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)'):
            item['capital'] = response.xpath('//div[@class="span6"]//p//text()').re('.*C?c?apital:\s*(.*)')
        else:
            item['capital'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)'):
            item['region'] = response.xpath('//div[@class="span6"]//p//text()').re('.*R?r?egion:\s*(.*)')
        else:
            item['region'] = 'Null'
        if response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)'):
            item['language'] = response.xpath('//div[@class="span6"]//p//text()').re('.*L?l?anguage:\s*(.*)')
        else:
            item['language'] = 'Null'
            

        ########################################################
        ###CURRENTLY EMPTY DATA FIELDS - POPULATE WITH "NULL"###
        ########################################################
            
        item['routerName'] = 'Null'
        item['bandwidth'] = 'Null'
        item['upTime'] = 'Null'
        item['hostName'] = 'Null'
        item['orPort'] = 'Null'
        item['dirPort'] = 'Null'
        item['badExit'] = 'Null'
        item['firstSeen'] = 'Null'
        item['asName'] = 'Null'
        item['asNumber'] = 'Null'
        item['consensusBandwidth'] = 'Null'
        item['orAddress'] = 'Null'
        item['platformVersion'] = 'Null'
        item['contactInfo'] = 'Null'

        ###torproject exitnodes###
        item['exitNode'] = 'Null'
        item['exitAddressDate'] = 'Null'
        item['exitAddressTime'] = 'Null'
        item['fingerPrint'] = 'Null'

        #######################
        ###FINGER PRINT INFO###
        #######################

        ###ROUTER FLAGS### #TRUE/FALSE VALUES
        item['authority'] = 'Null'
        item['badDirectory'] = 'Null'
        item['badExit'] = 'Null'
        item['exitTrueFalse'] = 'Null'
        item['fast'] = 'Null'
        item['guard'] = 'Null'
        item['hibernating'] = 'Null'
        item['named'] = 'Null'
        item['stable'] = 'Null'
        item['running'] = 'Null'
        item['valid'] = 'Null'
        item['v2Dir'] = 'Null'
        ####################################

    
        #Exit Policy info - ACCEPT/REJECT values
        item['exitAccept'] = 'Null'
        item['exitReject'] = 'Null'

        ###ROUTER KEYS###
        item['onionKey'] = 'Null'  #RSA public key
        item['signingKey'] = 'Null'  #RSA public key
    
        ###CONTACT INFORMATION###
        item['nameIndividual'] = 'Null' #name of person associated with fingerprint
        item['emailIndividual'] = 'Null' #email of person associated with fingerprint
        item['familyMembers'] = 'Null'  #related fingerprints


        item['descriptorPublishDate'] = 'Null'
        item['descriptorPublishTime'] = 'Null'
        item['bandwidthUnits'] = 'Null'
    

        item['siteOperator'] = 'Null' #name of person operating site
        item['sourceName'] = 'tordata4'
            
        yield item




###LIST OF ASSOCIATED CSVs###
#1 scrapy crawl whois1 -o tor_exit_addresses5a.csv

#debugging:
###ascii problems: country, address###
        




        
        

